/**
*
* Copyright (C) 2014-2016    Andrei Novikov (pyclustering@yandex.ru)
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

#include "cluster/rock.hpp"

#include <cmath>
#include <climits>
#include <iostream>

#include "utils.hpp"


namespace cluster_analysis {


rock::rock(void) :
    m_adjacency_matrix(adjacency_matrix()),
    m_radius(0.0),
    m_degree_normalization(0.0),
    m_number_clusters(0)
{ }


rock::rock(const double radius, const size_t num_clusters, const double threshold) :
    m_adjacency_matrix(adjacency_matrix()),
    m_radius(radius * radius),
    m_degree_normalization(1.0 + 2.0 * ( (1.0 - threshold) / (1.0 + threshold) )),
    m_number_clusters(num_clusters)
{ }


rock::~rock(void) { }


void rock::process(const dataset & p_data, cluster_data & p_result) {
    create_adjacency_matrix(p_data);

    /* initialize first version of clusters */
    for (size_t index = 0; index < p_data.size(); index++) {
        m_clusters.push_back(cluster(1, index));
    }

    while( (m_number_clusters < m_clusters.size()) && (merge_cluster()) ) { }

    /* copy results to the output result (it much more optimal to store in list representation for ROCK algorithm) */
    p_result = rock_data();
    p_result.clusters()->insert(p_result.clusters()->begin(), m_clusters.begin(), m_clusters.end());

    m_clusters.clear();         /* no need it anymore - clear to save memory */
    m_adjacency_matrix.clear(); /* no need it anymore - clear to save memory */
}


void rock::create_adjacency_matrix(const dataset & p_data) {
    m_adjacency_matrix = adjacency_matrix(p_data.size());
    for (size_t i = 0; i < m_adjacency_matrix.size(); i++) {
        for (size_t j = i + 1; j < m_adjacency_matrix.size(); j++) {
            double distance = euclidean_distance_sqrt(&p_data[i], &p_data[j]);

            if (distance < m_radius) {
                m_adjacency_matrix.set_connection(i, j);
                m_adjacency_matrix.set_connection(j, i);
            }
        }
    }
}


bool rock::merge_cluster(void) {
    auto cluster1 = m_clusters.end();
    auto cluster2 = m_clusters.end();

    double maximum_goodness = 0;

    for (auto i = m_clusters.begin(); i != m_clusters.end(); i++) {
        auto next = i;
        for (auto j = ++next; j != m_clusters.end(); j++) {
            double goodness = calculate_goodness(*i, *j);
            if (goodness > maximum_goodness) {
                maximum_goodness = goodness;

                cluster1 = i;
                cluster2 = j;
            }
        }
    }

    if (cluster1 == cluster2) {
        return false;   /* clusters are totally separated (no links between them), it's impossible to made a desicion which of them should be merged */
    }

    (*cluster1).insert((*cluster1).end(), (*cluster2).begin(), (*cluster2).end());
    m_clusters.erase(cluster2);

    return true;
}

unsigned int rock::calculate_links(const cluster & cluster1, const cluster & cluster2) const {
    size_t number_links = 0;
    for (auto i : cluster1) {
        for (auto j : cluster2) {
            number_links += (size_t) m_adjacency_matrix.has_connection(i, j);
        }
    }

    return number_links;
}

double rock::calculate_goodness(const cluster & cluster1, const cluster & cluster2) const {
    const double number_links = calculate_links(cluster1, cluster2);

    const double size_cluster1 = cluster1.size();
    const double size_cluster2 = cluster2.size();

    return number_links / ( std::pow( size_cluster1 + size_cluster2, m_degree_normalization ) -
        std::pow( size_cluster1, m_degree_normalization ) -
        std::pow( size_cluster2, m_degree_normalization ) );
}


}
