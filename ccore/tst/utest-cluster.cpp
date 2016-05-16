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

#include "utest-cluster.hpp"


void ASSERT_CLUSTER_SIZES(const dataset & p_data, const cluster_sequence & p_actual_clusters, const std::vector<size_t> & p_expected_cluster_length) {
    std::vector<size_t> obtained_cluster_length;
    std::vector<bool> unique_objects(p_data.size(), false);
    size_t total_size = 0;
    for (size_t i = 0; i < p_actual_clusters.size(); i++) {
        size_t cluster_length = p_actual_clusters[i].size();

        obtained_cluster_length.push_back(cluster_length);
        total_size += cluster_length;

        for (size_t j = 0; j < cluster_length; j++) {
            size_t index_object = p_actual_clusters[i][j];

            ASSERT_EQ(false, unique_objects[index_object]);

            unique_objects[index_object] = true;
        }
    }

    ASSERT_EQ(p_data.size(), total_size);

    if (!p_expected_cluster_length.empty()) {
        std::sort(obtained_cluster_length.begin(), obtained_cluster_length.end());

        std::vector<size_t> sorted_expected_cluster_length(p_expected_cluster_length);
        std::sort(sorted_expected_cluster_length.begin(), sorted_expected_cluster_length.end());

        for (size_t i = 0; i < obtained_cluster_length.size(); i++) {
            ASSERT_EQ(obtained_cluster_length[i], sorted_expected_cluster_length[i]);
        }
    }
}
