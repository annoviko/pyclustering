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
#include <iostream>
#include <limits>
#include <numeric>

#include "cluster/xmeans.hpp"

#include "utils.hpp"


xmeans::xmeans(const dataset & data, const dataset & initial_centers, const unsigned int kmax, const double minimum_change, const splitting_type criterion) :
    m_dataset((dataset *) &data),
    m_clusters(initial_centers.size(), std::vector<unsigned int>()),
    m_centers(initial_centers),
    m_maximum_clusters(kmax),
    m_tolerance(minimum_change * minimum_change),
    m_criterion(criterion)
{ }


xmeans::~xmeans(void) { }


void xmeans::process(void) {
    size_t current_number_clusters = m_clusters.size();
    const std::vector<unsigned int> dummy;

    while (current_number_clusters < m_maximum_clusters) {
        improve_parameters(m_clusters, m_centers, dummy);
        improve_structure();

        if (current_number_clusters == m_centers.size()) {
            break;
        }

        current_number_clusters = m_centers.size();
    }
}

void xmeans::improve_parameters(std::vector<std::vector<unsigned int> > & improved_clusters, dataset & improved_centers, const std::vector<unsigned int> & available_indexes) {
    double current_change = std::numeric_limits<double>::max();

    while(current_change > m_tolerance) {
        update_clusters(improved_clusters, improved_centers, available_indexes);
        current_change = update_centers(improved_clusters, improved_centers);
    }
}


void xmeans::improve_structure() {
    const double difference = 0.001;
    std::vector<std::vector<double> > allocated_centers;

    for (unsigned int index = 0; index < m_clusters.size(); index++) {
        std::vector<std::vector<double> > parent_child_centers;
        parent_child_centers.push_back( m_centers[index] );	/* the first child		*/
        parent_child_centers.push_back( m_centers[index] );	/* the second child		*/

        /* change location of each child (total number of children is two) */
        for (unsigned int dimension = 0; dimension < parent_child_centers[0].size(); dimension++) {
            parent_child_centers[0][dimension] -= difference;
            parent_child_centers[1][dimension] += difference;
        }

        /* solve k-means problem for children where data of parent are used */
        std::vector<std::vector<unsigned int> > parent_child_clusters(2, std::vector<unsigned int>());

        improve_parameters(parent_child_clusters, parent_child_centers, m_clusters[index]);

        /* splitting criterion */
        std::vector<std::vector<unsigned int> > parent_cluster(1, m_clusters[index]);
        std::vector<std::vector<double> > parent_center(1, m_centers[index]);

        double parent_scores = splitting_criterion(parent_cluster, parent_center);
        double child_scores = splitting_criterion(parent_child_clusters, parent_child_centers);

        if (m_criterion == splitting_type::BAYESIAN_INFORMATION_CRITERION) {
            /* take the best representation of the considered data */
            if (parent_scores > child_scores) {
                allocated_centers.push_back(m_centers[index]);
            }
            else {
                allocated_centers.push_back(parent_child_centers[0]);
                allocated_centers.push_back(parent_child_centers[1]);
            }
        }
        else if (m_criterion == splitting_type::MINIMUM_NOISELESS_DESCRIPTION_LENGTH) {
            if (parent_scores < child_scores) {
                allocated_centers.push_back(m_centers[index]);
            }
            else {
                allocated_centers.push_back(parent_child_centers[0]);
                allocated_centers.push_back(parent_child_centers[1]);
            }
        }
    }

    /* update current centers */
    m_centers.clear();
    for (unsigned int index = 0; index < allocated_centers.size(); index++) {
        m_centers.push_back(allocated_centers[index]);
    }
}


double xmeans::splitting_criterion(const std::vector<std::vector<unsigned int> > & analysed_clusters, const dataset & analysed_centers) const {
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


void xmeans::update_clusters(std::vector<std::vector<unsigned int> > & analysed_clusters, const dataset & analysed_centers, const std::vector<unsigned int> & available_indexes) {
    analysed_clusters.clear();
    analysed_clusters.resize(analysed_centers.size(), std::vector<unsigned int>());

    if (available_indexes.empty()) {
        for (unsigned int index_object = 0; index_object < m_dataset->size(); index_object++) {
            unsigned int index_cluster = find_proper_cluster(analysed_centers, (*m_dataset)[index_object]);
            analysed_clusters[index_cluster].push_back(index_object);
        }
    }
    else {
        for (std::vector<unsigned int>::const_iterator index_object = available_indexes.begin(); index_object != available_indexes.end(); index_object++) {
            unsigned int index_cluster = find_proper_cluster(analysed_centers, (*m_dataset)[*index_object]);
            analysed_clusters[index_cluster].push_back(*index_object);
        }
    }
}


unsigned int xmeans::find_proper_cluster(const dataset & analysed_centers, const point & p_point) const {
    unsigned int index_optimum = 0;
    double distance_optimum = std::numeric_limits<double>::max();

    for (unsigned int index_cluster = 0; index_cluster < analysed_centers.size(); index_cluster++) {
        double distance = euclidean_distance_sqrt( &p_point, &(analysed_centers[index_cluster]) );

        if (distance < distance_optimum) {
            index_optimum = index_cluster;
            distance_optimum = distance;
        }
    }

    return index_optimum;
}


double xmeans::update_centers(const std::vector<std::vector<unsigned int> > & analysed_clusters, dataset & analysed_centers) {
    double maximum_change = 0;

    /* for each cluster */
    for (unsigned int index_cluster = 0; index_cluster < analysed_clusters.size(); index_cluster++) {
        std::vector<double> total(analysed_centers[index_cluster].size(), 0);

        /* for each object in cluster */
        for (std::vector<unsigned int>::const_iterator object_index_iterator = analysed_clusters[index_cluster].begin(); object_index_iterator < analysed_clusters[index_cluster].end(); object_index_iterator++) {
            /* for each dimension */
            for (unsigned int dimension = 0; dimension < total.size(); dimension++) {
                total[dimension] += (*m_dataset)[*object_index_iterator][dimension];
            }
        }

        /* average for each dimension */
        for (std::vector<double>::iterator dimension_iterator = total.begin(); dimension_iterator != total.end(); dimension_iterator++) {
            *dimension_iterator = *dimension_iterator / analysed_clusters[index_cluster].size();
        }

        double distance = euclidean_distance_sqrt( &(analysed_centers[index_cluster]), &total );

        if (distance > maximum_change) {
            maximum_change = distance;
        }

        std::copy(total.begin(), total.end(), analysed_centers[index_cluster].begin());
    }

    return maximum_change;
}


double xmeans::bayesian_information_criterion(const std::vector<std::vector<unsigned int> > & analysed_clusters, const dataset & analysed_centers) const {
    std::vector<double> scores(analysed_centers.size(), 0.0);

    double score = std::numeric_limits<double>::max();
    double dimension = (double) analysed_centers[0].size();
    double sigma = 0.0;
    size_t K = analysed_centers.size();
    size_t N = 0;

    for (unsigned int index_cluster = 0; index_cluster < analysed_clusters.size(); index_cluster++) {
        for (std::vector<unsigned int>::const_iterator index_object = analysed_clusters[index_cluster].begin(); index_object != analysed_clusters[index_cluster].end(); index_object++) {
            sigma += euclidean_distance_sqrt( &(*m_dataset)[*index_object], &(analysed_centers[index_cluster]) );
        }

        N += analysed_clusters[index_cluster].size();
    }

    if (N - K > 0) {
        sigma /= (double) (N - K);
        double p = (K - 1) + dimension * K + 1;

        /* splitting criterion */
        for (unsigned int index_cluster = 0; index_cluster < analysed_centers.size(); index_cluster++) {
            double n = (double) analysed_clusters[index_cluster].size();
            double L = n * std::log(n) - n * std::log(N) - n * std::log(2.0 * pi()) / 2.0 - n * dimension * std::log(sigma) / 2.0 - (n - K) / 2.0;

            scores[index_cluster] = L - p * 0.5 * std::log(N);
        }

        score = std::accumulate(scores.begin(), scores.end(), 0.0);
    }

    return score;
}


double xmeans::minimum_noiseless_description_length(const std::vector<std::vector<unsigned int> > & clusters, const dataset & centers) const {
    double score = std::numeric_limits<double>::max();

    double W = 0.0;
    double K = clusters.size();
    double N = 0.0;

    double sigma_sqrt = 0.0;
    const double alpha = 0.9;
    const double betta = 0.9;

    for (std::size_t index_cluster = 0; index_cluster < clusters.size(); index_cluster++) {
        if (clusters[index_cluster].empty()) {
            return std::numeric_limits<double>::max();
        }

        double Ni = clusters[index_cluster].size();
        double Wi = 0.0;
        for (auto & index_object : clusters[index_cluster]) {
            /* euclidean_distance_sqrt should be used in line with paper, but in this case results are
             * very poor, therefore square root is used to improved. */
            Wi += euclidean_distance((*m_dataset)[index_object], centers[index_cluster]);
        }

        sigma_sqrt += Wi;
        W += Wi / Ni;
        N += Ni;
    }

    if (N - K > 0) {
        sigma_sqrt /= (N - K);
        double sigma = std::sqrt(sigma_sqrt);

        double Kw = (1.0 - K / N) * sigma_sqrt;
        double Ks = ( 2.0 * alpha * sigma / std::sqrt(N) ) * std::sqrt( (std::pow(alpha, 2)) * sigma_sqrt / N + W - Kw / 2.0 );

        score = sigma_sqrt * std::sqrt(2 * K) * (std::sqrt(2 * K) + betta) / N + W - sigma_sqrt + Ks + 2 * std::sqrt(alpha) * sigma_sqrt / N;
    }

    return score;
}
