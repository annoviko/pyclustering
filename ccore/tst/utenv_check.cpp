/**
*
* Copyright (C) 2014-2018    Andrei Novikov (pyclustering@yandex.ru)
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


#include "utenv_check.hpp"

#include <algorithm>
#include <numeric>
#include <unordered_map>


using namespace ccore::clst;


void ASSERT_CLUSTER_SIZES(const dataset & p_data, 
                          const cluster_sequence & p_actual_clusters, 
                          const std::vector<size_t> & p_expected_cluster_length,
                          const index_sequence & p_indexes) {
    if (p_expected_cluster_length.empty() && p_actual_clusters.empty()) {
        return;
    }

    std::size_t total_size = 0;
    std::unordered_map<std::size_t, bool> unique_objects;
    std::vector<std::size_t> obtained_cluster_length;

    for (auto & cluster : p_actual_clusters) {
        total_size += cluster.size();

        obtained_cluster_length.push_back(cluster.size());

        for (auto index_object : cluster) {
            unique_objects[index_object] = false;
        }
    }

    ASSERT_EQ(total_size, unique_objects.size());

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
    else
    {
        if (!p_indexes.empty()) {
            ASSERT_EQ(p_indexes.size(), unique_objects.size());

            for (auto index : p_indexes) {
                ASSERT_TRUE( unique_objects.find(index) != unique_objects.cend() );
            }
        }
        else {
            ASSERT_EQ(p_data.size(), total_size);
        }
    }
}
