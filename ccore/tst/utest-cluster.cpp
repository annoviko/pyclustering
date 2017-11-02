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

#include "utest-cluster.hpp"

#include <numeric>


void ASSERT_CLUSTER_SIZES(const dataset & p_data, const cluster_sequence & p_actual_clusters, const std::vector<size_t> & p_expected_cluster_length) {
    if (p_expected_cluster_length.empty() && p_actual_clusters.empty()) {
        return;
    }

    std::vector<size_t> obtained_cluster_length;
    std::vector<bool> unique_objects(p_data.size(), false);
    size_t total_size = 0;
    for (size_t i = 0; i < p_actual_clusters.size(); i++) {
        size_t cluster_length = p_actual_clusters[i].size();

        obtained_cluster_length.push_back(cluster_length);
        total_size += cluster_length;

        for (size_t j = 0; j < cluster_length; j++) {
            size_t index_object = p_actual_clusters[i][j];

            ASSERT_FALSE(unique_objects[index_object]);

            unique_objects[index_object] = true;
        }
    }

    if (!p_expected_cluster_length.empty()) {
        std::size_t expected_total_size = std::accumulate(p_expected_cluster_length.cbegin(), p_expected_cluster_length.cend(), (std::size_t) 0);

        ASSERT_EQ(expected_total_size, total_size);

        std::sort(obtained_cluster_length.begin(), obtained_cluster_length.end());

        std::vector<size_t> sorted_expected_cluster_length(p_expected_cluster_length);
        std::sort(sorted_expected_cluster_length.begin(), sorted_expected_cluster_length.end());

        for (size_t i = 0; i < obtained_cluster_length.size(); i++) {
            ASSERT_EQ(obtained_cluster_length[i], sorted_expected_cluster_length[i]);
        }
    }
    else {
        ASSERT_EQ(p_data.size(), total_size);
    }
}
