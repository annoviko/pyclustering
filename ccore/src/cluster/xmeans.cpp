/**
*
* Copyright (C) 2014-2017    Andrei Novikov (pyclustering@yandex.ru)
*
* GNU_PUBLIC_LICENSE
*   pyclustering is free software: you can redistribute it and/or modify
*   it under the terms of the GNU General Public License as published by
*   the Free Software Foundation, either version 3 of the License, or
*   (at your option) any later version.
*
*   pyclustering is distributed in the hope that it will be useful,
*   but WITHOUT ANY WARRANTY; without even the implied warranty of
*   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
*   GNU General Public License for more details.
*
*   You should have received a copy of the GNU General Public License
*   along with this program.  If not, see <http://www.gnu.org/licenses/>.
*
*/



#include <cmath>
#include <future>
#include <iostream>
#include <limits>
#include <numeric>

#include "cluster/xmeans.hpp"

#include "utils.hpp"


namespace cluster_analysis {


const double             xmeans::DEFAULT_SPLIT_DIFFERENCE                = 0.001;

const std::size_t        xmeans::DEFAULT_DATA_SIZE_PARALLEL_PROCESSING   = 100000;

const std::size_t        xmeans::DEFAULT_THREAD_POOL_SIZE                = 15;


xmeans::xmeans(const dataset & p_centers, const std::size_t p_kmax, const double p_tolerance, const splitting_type p_criterion) :
    m_centers(p_centers),
    m_maximum_clusters(p_kmax),
    m_tolerance(p_tolerance * p_tolerance),
    m_criterion(p_criterion),
    m_parallel_trigger(DEFAULT_DATA_SIZE_PARALLEL_PROCESSING),
    m_parallel_processing(false),
    m_mutex(),
    m_pool(DEFAULT_THREAD_POOL_SIZE)
{ }


xmeans::~xmeans(void) { }


void xmeans::process(const dataset & data, cluster_data & output_result) {
    m_ptr_data = &data;

    m_parallel_processing = (m_ptr_data->size() >= m_parallel_trigger);

    output_result = xmeans_data();
    m_ptr_result = (xmeans_data *)&output_result;

    m_ptr_result->centers()->assign(m_centers.begin(), m_centers.end());

    size_t current_number_clusters = m_ptr_result->centers()->size();
    const index_sequence dummy;

    while (current_number_clusters <= m_maximum_clusters) {
        improve_parameters(*(m_ptr_result->clusters()), m_centers, dummy);
        improve_structure();

        if (current_number_clusters == m_centers.size()) {
            break;
        }

        current_number_clusters = m_centers.size();
    }

    *(m_ptr_result->centers().get()) = std::move(m_centers);
}


void xmeans::set_parallel_processing_trigger(const std::size_t p_data_size) {
    m_parallel_trigger = p_data_size;
}


void xmeans::improve_parameters(cluster_sequence & improved_clusters, dataset & improved_centers, const index_sequence & available_indexes) {
    double current_change = std::numeric_limits<double>::max();

    while(current_change > m_tolerance) {
        update_clusters(improved_clusters, improved_centers, available_indexes);
        current_change = update_centers(improved_clusters, improved_centers);
    }
}


void xmeans::improve_structure() {
    cluster_sequence & clusters = *(m_ptr_result->clusters());
    std::vector<dataset> region_allocated_centers(m_ptr_result->clusters()->size(), dataset());

    if (m_parallel_processing) {
        for (std::size_t index = 0; index < m_ptr_result->clusters()->size(); index++) {
            task::proc improve_proc = [this, index, &clusters, &region_allocated_centers](){
                    improve_region_structure(clusters[index], m_centers[index], region_allocated_centers[index]);
                };

            m_pool.add_task(improve_proc);
        }

        for (std::size_t i = 0; i < m_ptr_result->clusters()->size(); i++) {
            m_pool.pop_complete_task();
        }
    }
    else {
        dataset allocated_centers;

        for (std::size_t index = 0; index < m_ptr_result->clusters()->size(); index++) {
            improve_region_structure((*(m_ptr_result->clusters()))[index], m_centers[index], region_allocated_centers[index]);
        }
    }

    /* update current centers */
    dataset allocated_centers = { };
    std::size_t amount_free_centers = m_maximum_clusters - clusters.size();

    for (std::size_t index_cluster = 0; index_cluster < region_allocated_centers.size(); index_cluster++) {
        dataset & centers = region_allocated_centers[index_cluster];
        if ( (centers.size() > 1) && (amount_free_centers > 0) ) {
            /* separate cluster */
            allocated_centers.push_back(centers[0]);
            allocated_centers.push_back(centers[1]);

            amount_free_centers--;
        }
        else {
            allocated_centers.push_back(m_centers[index_cluster]);
        }
    }

    m_centers = std::move(allocated_centers);
}


void xmeans::improve_region_structure(const cluster & p_cluster, const point & p_center, dataset & p_allocated_centers) {
    dataset parent_child_centers;

    parent_child_centers.push_back( p_center );     /* the first child      */
    parent_child_centers.push_back( p_center );     /* the second child     */

    /* change location of each child (total number of children is two) */
    for (std::size_t dimension = 0; dimension < parent_child_centers[0].size(); dimension++) {
        parent_child_centers[0][dimension] -= DEFAULT_SPLIT_DIFFERENCE;
        parent_child_centers[1][dimension] += DEFAULT_SPLIT_DIFFERENCE;
    }

    /* solve k-means problem for children where data of parent are used */
    cluster_sequence parent_child_clusters(2, cluster());

    improve_parameters(parent_child_clusters, parent_child_centers, p_cluster);

    /* splitting criterion */
    cluster_sequence parent_cluster(1, p_cluster);
    dataset parent_center(1, p_center);

    double parent_scores = splitting_criterion(parent_cluster, parent_center);
    double child_scores = splitting_criterion(parent_child_clusters, parent_child_centers);

    bool divide_descision = false;

    if (m_criterion == splitting_type::BAYESIAN_INFORMATION_CRITERION) {
        divide_descision = (parent_scores <= child_scores);
    }
    else if (m_criterion == splitting_type::MINIMUM_NOISELESS_DESCRIPTION_LENGTH) {
        divide_descision = (parent_scores >= child_scores);
    }

    if (divide_descision) {
        p_allocated_centers.push_back(parent_child_centers[0]);
        p_allocated_centers.push_back(parent_child_centers[1]);
    }
    else {
        p_allocated_centers.push_back(p_center);
    }
}


double xmeans::splitting_criterion(const cluster_sequence & analysed_clusters, const dataset & analysed_centers) const {
    switch(m_criterion) {
        case splitting_type::BAYESIAN_INFORMATION_CRITERION:
            return bayesian_information_criterion(analysed_clusters, analysed_centers);

        case splitting_type::MINIMUM_NOISELESS_DESCRIPTION_LENGTH:
            return minimum_noiseless_description_length(analysed_clusters, analysed_centers);

        default:
            /* Unexpected state - return default */
            return bayesian_information_criterion(analysed_clusters, analysed_centers);
    }
}


void xmeans::update_clusters(cluster_sequence & analysed_clusters, const dataset & analysed_centers, const index_sequence & available_indexes) {
    analysed_clusters.clear();
    analysed_clusters.resize(analysed_centers.size(), cluster());

    if (available_indexes.empty()) {
        for (std::size_t index_object = 0; index_object < m_ptr_data->size(); index_object++) {
            std::size_t index_cluster = find_proper_cluster(analysed_centers, (*m_ptr_data)[index_object]);
            analysed_clusters[index_cluster].push_back(index_object);
        }
    }
    else {
        for (auto & index_object : available_indexes) {
            std::size_t index_cluster = find_proper_cluster(analysed_centers, (*m_ptr_data)[index_object]);
            analysed_clusters[index_cluster].push_back(index_object);
        }
    }
}


std::size_t xmeans::find_proper_cluster(const dataset & analysed_centers, const point & p_point) const {
    std::size_t index_optimum = 0;
    double distance_optimum = std::numeric_limits<double>::max();

    for (std::size_t index_cluster = 0; index_cluster < analysed_centers.size(); index_cluster++) {
        double distance = euclidean_distance_sqrt( &p_point, &(analysed_centers[index_cluster]) );

        if (distance < distance_optimum) {
            index_optimum = index_cluster;
            distance_optimum = distance;
        }
    }

    return index_optimum;
}


double xmeans::update_centers(const cluster_sequence & analysed_clusters, dataset & analysed_centers) {
    double maximum_change = 0;

    for (std::size_t index_cluster = 0; index_cluster < analysed_clusters.size(); index_cluster++) {
        double distance = update_center(analysed_clusters[index_cluster], analysed_centers[index_cluster]);

        if (distance > maximum_change) {
            maximum_change = distance;
        }
    }

    return maximum_change;
}


double xmeans::update_center(const cluster & p_cluster, point & p_center) {
    std::vector<double> total(p_center.size(), 0);

    /* for each object in cluster */
    for (auto & object_index : p_cluster) {
        /* for each dimension */
        for (std::size_t dimension = 0; dimension < total.size(); dimension++) {
            total[dimension] += (*m_ptr_data)[object_index][dimension];
        }
    }

    /* average for each dimension */
    for (auto & dimension : total) {
        dimension = dimension / p_cluster.size();
    }

    double distance = euclidean_distance_sqrt( &p_center, &total );

    std::copy(total.begin(), total.end(), p_center.begin());

    return distance;
}


double xmeans::bayesian_information_criterion(const cluster_sequence & analysed_clusters, const dataset & analysed_centers) const {
    std::vector<double> scores(analysed_centers.size(), 0.0);

    double score = std::numeric_limits<double>::max();
    double dimension = (double) analysed_centers[0].size();
    double sigma = 0.0;
    std::size_t K = analysed_centers.size();
    std::size_t N = 0;

    for (std::size_t index_cluster = 0; index_cluster < analysed_clusters.size(); index_cluster++) {
        for (auto & index_object : analysed_clusters[index_cluster]) {
            sigma += euclidean_distance_sqrt( &(*m_ptr_data)[index_object], &(analysed_centers[index_cluster]) );
        }

        N += analysed_clusters[index_cluster].size();
    }

    if (N - K > 0) {
        sigma /= (double) (N - K);
        double p = (K - 1) + dimension * K + 1;

        /* splitting criterion */
        for (std::size_t index_cluster = 0; index_cluster < analysed_centers.size(); index_cluster++) {
            double n = (double) analysed_clusters[index_cluster].size();
            double L = n * std::log(n) - n * std::log(N) - n * std::log(2.0 * pi()) / 2.0 - n * dimension * std::log(sigma) / 2.0 - (n - K) / 2.0;

            scores[index_cluster] = L - p * 0.5 * std::log(N);
        }

        score = std::accumulate(scores.begin(), scores.end(), 0.0);
    }

    return score;
}


double xmeans::minimum_noiseless_description_length(const cluster_sequence & clusters, const dataset & centers) const {
    double score = std::numeric_limits<double>::max();

    double W = 0.0;
    double K = (double) clusters.size();
    double N = 0.0;

    double sigma_sqrt = 0.0;

    for (std::size_t index_cluster = 0; index_cluster < clusters.size(); index_cluster++) {
        if (clusters[index_cluster].empty()) {
            return std::numeric_limits<double>::max();
        }

        double Ni = (double) clusters[index_cluster].size();
        double Wi = 0.0;
        for (auto & index_object : clusters[index_cluster]) {
            /* euclidean_distance_sqrt should be used in line with paper, but in this case results are
             * very poor, therefore square root is used to improved. */
            Wi += euclidean_distance((*m_ptr_data)[index_object], centers[index_cluster]);
        }

        sigma_sqrt += Wi;
        W += Wi / Ni;
        N += Ni;
    }

    if (N - K > 0) {
        const double alpha = 0.9;
        const double betta = 0.9;

        sigma_sqrt /= (N - K);
        double sigma = std::sqrt(sigma_sqrt);

        double Kw = (1.0 - K / N) * sigma_sqrt;
        double Ks = ( 2.0 * alpha * sigma / std::sqrt(N) ) * std::sqrt( (std::pow(alpha, 2)) * sigma_sqrt / N + W - Kw / 2.0 );

        score = sigma_sqrt * std::sqrt(2 * K) * (std::sqrt(2 * K) + betta) / N + W - sigma_sqrt + Ks + 2 * std::sqrt(alpha) * sigma_sqrt / N;
    }

    return score;
}


}
