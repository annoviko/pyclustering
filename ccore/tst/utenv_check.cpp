/*!

@authors Andrei Novikov (pyclustering@yandex.ru)
@date 2014-2020
@copyright BSD-3-Clause

*/


#include "utenv_check.hpp"

#include <algorithm>
#include <numeric>
#include <unordered_map>


using namespace pyclustering::clst;


void ASSERT_CLUSTER_SIZES(
    const dataset & p_data, 
    const cluster_sequence & p_actual_clusters, 
    const std::vector<size_t> & p_expected_cluster_length,
    const index_sequence & p_indexes)
{
    ASSERT_CLUSTER_NOISE_SIZES(p_data, p_actual_clusters, p_expected_cluster_length, { }, -1, p_indexes);
}


void ASSERT_CLUSTER_NOISE_SIZES(
    const dataset & p_data,
    const cluster_sequence & p_actual_clusters,
    const std::vector<std::size_t> & p_expected_cluster_length,
    const noise & p_actual_noise,
    const std::size_t & p_expected_noise_length,
    const index_sequence & p_indexes)
{
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

    total_size += p_actual_noise.size();
    for (auto index_object : p_actual_noise) {
        unique_objects[index_object] = false;
    }

    ASSERT_EQ(total_size, unique_objects.size());

    if (!p_expected_cluster_length.empty()) {
        std::size_t expected_total_size = std::accumulate(p_expected_cluster_length.cbegin(), p_expected_cluster_length.cend(), (std::size_t) 0);
        if (p_expected_noise_length != (std::size_t) -1) {
             expected_total_size += p_expected_noise_length;
        }

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

    if (p_expected_noise_length != (std::size_t) -1) {
        ASSERT_EQ(p_expected_noise_length, p_actual_noise.size());
    }
}