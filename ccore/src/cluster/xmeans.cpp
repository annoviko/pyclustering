/**
*
* @authors Andrei Novikov (pyclustering@yandex.ru)
* @date 2014-2019
* @copyright GNU Public License
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

#include <pyclustering/cluster/xmeans.hpp>

#include <pyclustering/cluster/kmeans.hpp>
#include <pyclustering/cluster/kmeans_plus_plus.hpp>

#include <pyclustering/parallel/parallel.hpp>

#include <pyclustering/utils/math.hpp>
#include <pyclustering/utils/metric.hpp>


using namespace pyclustering::parallel;
using namespace pyclustering::utils::metric;


namespace pyclustering {

namespace clst {


const double             xmeans::DEFAULT_SPLIT_DIFFERENCE                = 0.001;

const std::size_t        xmeans::AMOUNT_CENTER_CANDIDATES                = 5;


xmeans::xmeans(const dataset & p_initial_centers, const std::size_t p_kmax, const double p_tolerance, const splitting_type p_criterion, std::size_t p_repeat) :
    m_initial_centers(p_initial_centers),
    m_ptr_result(nullptr),
    m_ptr_data(nullptr),
    m_maximum_clusters(p_kmax),
    m_tolerance(p_tolerance * p_tolerance),
    m_criterion(p_criterion),
    m_repeat(p_repeat)
{ }


void xmeans::process(const dataset & data, cluster_data & output_result) {
    m_ptr_data = &data;

    output_result = xmeans_data();
    m_ptr_result = (xmeans_data *)&output_result;

    m_ptr_result->centers() = m_initial_centers;
    dataset & centers = m_ptr_result->centers();
    cluster_sequence & clusters = m_ptr_result->clusters();

    std::size_t current_number_clusters = centers.size();
    const index_sequence dummy;

    while (current_number_clusters <= m_maximum_clusters) {
        improve_parameters(clusters, centers, dummy);
        improve_structure();

        if (current_number_clusters == centers.size()) {
            break;
        }

        current_number_clusters = centers.size();
    }

    m_ptr_result->wce() = improve_parameters(clusters, centers, dummy);
}


double xmeans::improve_parameters(cluster_sequence & improved_clusters, dataset & improved_centers, const index_sequence & available_indexes) const {
    kmeans_data result;
    kmeans(improved_centers, m_tolerance).process((*m_ptr_data), available_indexes, result);

    improved_centers = result.centers();
    improved_clusters = result.clusters();

    return result.wce();
}


double xmeans::search_optimal_parameters(cluster_sequence & improved_clusters, dataset & improved_centers, const index_sequence & available_indexes) const {
    double optimal_wce = std::numeric_limits<double>::max();

    for (std::size_t attempt = 0; attempt < m_repeat; attempt++) {
        /* initialize initial center using k-means++ */
        dataset candidate_centers;
        const std::size_t candidates = available_indexes.size() < AMOUNT_CENTER_CANDIDATES ?  available_indexes.size() : AMOUNT_CENTER_CANDIDATES;
        kmeans_plus_plus(2U, candidates).initialize(*m_ptr_data, available_indexes, candidate_centers);

        /* perform cluster analysis and update optimum if results became better */
        cluster_sequence candidate_clusters;
        double candidate_wce = improve_parameters(candidate_clusters, candidate_centers, available_indexes);

        if (candidate_wce < optimal_wce) {
            improved_clusters = std::move(candidate_clusters);
            improved_centers = std::move(candidate_centers);
            optimal_wce = candidate_wce;
        }
    }

    return optimal_wce;
}


void xmeans::improve_structure() {
    cluster_sequence & clusters = m_ptr_result->clusters();
    dataset & current_centers = m_ptr_result->centers();

    std::vector<dataset> region_allocated_centers(m_ptr_result->clusters().size(), dataset());

    parallel_for(std::size_t(0), m_ptr_result->clusters().size(), [this, &clusters, &current_centers, &region_allocated_centers](const std::size_t p_index) {
        improve_region_structure(clusters[p_index], current_centers[p_index], region_allocated_centers[p_index]);
    });

    /* update current centers */
    dataset allocated_centers = { };
    std::size_t amount_free_centers = m_maximum_clusters - clusters.size();

    for (const auto & centers : region_allocated_centers) {
        if ( (centers.size() > 1) && (amount_free_centers > 0) ) {
            /* separate cluster */
            allocated_centers.push_back(centers[0]);
            allocated_centers.push_back(centers[1]);

            amount_free_centers--;
        }
        else {
            allocated_centers.push_back(centers[0]);
        }
    }

    current_centers = allocated_centers;
}


void xmeans::improve_region_structure(const cluster & p_cluster, const point & p_center, dataset & p_allocated_centers) const {
    /* in case of cluster with one object */
    if (p_cluster.size() == 1) {
        std::size_t index_center = p_cluster[0];
        p_allocated_centers.push_back((*m_ptr_data)[index_center]);
        return;
    }

    /* solve k-means problem for children where data of parent are used */
    dataset parent_child_centers;
    cluster_sequence parent_child_clusters;
    search_optimal_parameters(parent_child_clusters, parent_child_centers, p_cluster);

    if (parent_child_clusters.size() == 1) {
        /* real situation when all points in cluster are identical */
        p_allocated_centers.push_back(p_center);
        return;
    }

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


double xmeans::bayesian_information_criterion(const cluster_sequence & analysed_clusters, const dataset & analysed_centers) const {
    double score = std::numeric_limits<double>::max();
    double dimension = (double) analysed_centers[0].size();
    double sigma = 0.0;
    std::size_t K = analysed_centers.size();
    std::size_t N = 0;

    for (std::size_t index_cluster = 0; index_cluster < analysed_clusters.size(); index_cluster++) {
        for (auto & index_object : analysed_clusters[index_cluster]) {
            sigma += euclidean_distance_square( (*m_ptr_data)[index_object], analysed_centers[index_cluster] );
        }

        N += analysed_clusters[index_cluster].size();
    }

    if (N != K) {
        std::vector<double> scores(analysed_centers.size(), 0.0);

        sigma /= (double) (N - K);
        double p = (K - 1) + dimension * K + 1;

        /* splitting criterion */
        for (std::size_t index_cluster = 0; index_cluster < analysed_centers.size(); index_cluster++) {
            double n = (double) analysed_clusters[index_cluster].size();
            double L = n * std::log(n) - n * std::log(N) - n * std::log(2.0 * utils::math::pi) / 2.0 - n * dimension * std::log(sigma) / 2.0 - (n - K) / 2.0;

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
            /* euclidean_distance_square should be used in line with paper, but in this case results are
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

}
