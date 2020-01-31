/**
*
* @authors Andrei Novikov (pyclustering@yandex.ru)
* @date 2014-2020
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


#include <gtest/gtest.h>

#include <pyclustering/cluster/clique.hpp>

#include "samples.hpp"

#include "utenv_check.hpp"


using namespace pyclustering;
using namespace pyclustering::clst;


static void
template_clique_length_process_data(
    const dataset_ptr p_data,
    const std::size_t p_intervals,
    const std::size_t p_threshold,
    const std::vector<std::size_t> & p_expected_cluster_length,
    const std::size_t p_expected_noise_length) 
{
    clique_data output_result;
    clique solver(p_intervals, p_threshold);
    solver.process(*p_data, output_result);

    const dataset & data = *p_data;
    const cluster_sequence & actual_clusters = output_result.clusters();
    const noise & noise = output_result.noise();
    const clique_block_sequence & blocks = output_result.blocks();

    for (auto & block : blocks) {
        ASSERT_TRUE(block.is_visited());
    }

    ASSERT_CLUSTER_NOISE_SIZES(data, actual_clusters, p_expected_cluster_length, noise, p_expected_noise_length);
}

TEST(utest_clique, allocation_sample_simple_01) {
    const std::vector<std::size_t> expected_clusters_length = { 5, 5 };
    template_clique_length_process_data(simple_sample_factory::create_sample(SAMPLE_SIMPLE::SAMPLE_SIMPLE_01), 8, 0, expected_clusters_length, 0);
    template_clique_length_process_data(simple_sample_factory::create_sample(SAMPLE_SIMPLE::SAMPLE_SIMPLE_01), 7, 0, expected_clusters_length, 0);
    template_clique_length_process_data(simple_sample_factory::create_sample(SAMPLE_SIMPLE::SAMPLE_SIMPLE_01), 6, 0, expected_clusters_length, 0);
    template_clique_length_process_data(simple_sample_factory::create_sample(SAMPLE_SIMPLE::SAMPLE_SIMPLE_01), 5, 0, expected_clusters_length, 0);
}

TEST(utest_clique, allocation_sample_simple_01_one_cluster) {
    const std::vector<std::size_t> expected_clusters_length = { 10 };
    template_clique_length_process_data(simple_sample_factory::create_sample(SAMPLE_SIMPLE::SAMPLE_SIMPLE_01), 1, 0, expected_clusters_length, 0);
}

TEST(utest_clique, allocation_sample_simple_01_only_noise) {
    template_clique_length_process_data(simple_sample_factory::create_sample(SAMPLE_SIMPLE::SAMPLE_SIMPLE_01), 6, 1000, { }, 10);
    template_clique_length_process_data(simple_sample_factory::create_sample(SAMPLE_SIMPLE::SAMPLE_SIMPLE_01), 6, 10, { }, 10);
    template_clique_length_process_data(simple_sample_factory::create_sample(SAMPLE_SIMPLE::SAMPLE_SIMPLE_01), 2, 5, { }, 10);
}

TEST(utest_clique, allocation_sample_simple_02) {
    const std::vector<std::size_t> expected_clusters_length = { 5, 8, 10 };
    template_clique_length_process_data(simple_sample_factory::create_sample(SAMPLE_SIMPLE::SAMPLE_SIMPLE_02), 7, 0, expected_clusters_length, 0);
    template_clique_length_process_data(simple_sample_factory::create_sample(SAMPLE_SIMPLE::SAMPLE_SIMPLE_02), 6, 0, expected_clusters_length, 0);
}

TEST(utest_clique, allocation_sample_simple_02_one_cluster) {
    const std::vector<std::size_t> expected_clusters_length = { 23 };
    template_clique_length_process_data(simple_sample_factory::create_sample(SAMPLE_SIMPLE::SAMPLE_SIMPLE_02), 1, 0, expected_clusters_length, 0);
}

TEST(utest_clique, allocation_sample_simple_02_only_noise) {
    template_clique_length_process_data(simple_sample_factory::create_sample(SAMPLE_SIMPLE::SAMPLE_SIMPLE_02), 6, 20, { }, 23);
}

TEST(utest_clique, allocation_sample_simple_03) {
    const std::vector<std::size_t> expected_clusters_length = { 10, 10, 10, 30 };
    template_clique_length_process_data(simple_sample_factory::create_sample(SAMPLE_SIMPLE::SAMPLE_SIMPLE_03), 9, 0, expected_clusters_length, 0);
    template_clique_length_process_data(simple_sample_factory::create_sample(SAMPLE_SIMPLE::SAMPLE_SIMPLE_03), 8, 0, expected_clusters_length, 0);
}

TEST(utest_clique, allocation_sample_simple_03_one_cluster) {
    const std::vector<std::size_t> expected_clusters_length = { 60 };
    template_clique_length_process_data(simple_sample_factory::create_sample(SAMPLE_SIMPLE::SAMPLE_SIMPLE_03), 1, 0, expected_clusters_length, 0);
}

TEST(utest_clique, allocation_sample_simple_03_only_noise) {
    template_clique_length_process_data(simple_sample_factory::create_sample(SAMPLE_SIMPLE::SAMPLE_SIMPLE_03), 6, 20, { }, 60);
}

TEST(utest_clique, allocation_sample_simple_03_one_point_noise) {
    const std::vector<std::size_t> expected_clusters_length = { 59 };
    template_clique_length_process_data(simple_sample_factory::create_sample(SAMPLE_SIMPLE::SAMPLE_SIMPLE_03), 2, 9, expected_clusters_length, 1);
}

TEST(utest_clique, allocation_sample_simple_04_one_cluster) {
    const std::vector<std::size_t> expected_clusters_length = { 75 };
    template_clique_length_process_data(simple_sample_factory::create_sample(SAMPLE_SIMPLE::SAMPLE_SIMPLE_04), 1, 0, expected_clusters_length, 0);
}

TEST(utest_clique, allocation_sample_simple_05) {
    const std::vector<std::size_t> expected_clusters_length = { 15, 15, 15, 15 };
    template_clique_length_process_data(simple_sample_factory::create_sample(SAMPLE_SIMPLE::SAMPLE_SIMPLE_05), 8, 0, expected_clusters_length, 0);
    template_clique_length_process_data(simple_sample_factory::create_sample(SAMPLE_SIMPLE::SAMPLE_SIMPLE_05), 7, 0, expected_clusters_length, 0);
    template_clique_length_process_data(simple_sample_factory::create_sample(SAMPLE_SIMPLE::SAMPLE_SIMPLE_05), 6, 0, expected_clusters_length, 0);
    template_clique_length_process_data(simple_sample_factory::create_sample(SAMPLE_SIMPLE::SAMPLE_SIMPLE_05), 5, 0, expected_clusters_length, 0);
}

TEST(utest_clique, allocation_sample_simple_05_one_cluster) {
    const std::vector<std::size_t> expected_clusters_length = { 60 };
    template_clique_length_process_data(simple_sample_factory::create_sample(SAMPLE_SIMPLE::SAMPLE_SIMPLE_05), 1, 0, expected_clusters_length, 0);
}

TEST(utest_clique, allocation_one_dimensional_data1) {
    template_clique_length_process_data(simple_sample_factory::create_sample(SAMPLE_SIMPLE::SAMPLE_SIMPLE_07), 4, 0, { 10, 10 }, 0);
    template_clique_length_process_data(simple_sample_factory::create_sample(SAMPLE_SIMPLE::SAMPLE_SIMPLE_07), 2, 0, { 20 }, 0);
}

TEST(utest_clique, allocation_one_dimensional_data2) {
    template_clique_length_process_data(simple_sample_factory::create_sample(SAMPLE_SIMPLE::SAMPLE_SIMPLE_08), 15, 0, { 15, 20, 30, 80 }, 0);
    template_clique_length_process_data(simple_sample_factory::create_sample(SAMPLE_SIMPLE::SAMPLE_SIMPLE_08), 2, 0, { 145 }, 0);
}

TEST(utest_clique, allocation_one_dimensional_data3_similar) {
    template_clique_length_process_data(simple_sample_factory::create_sample(SAMPLE_SIMPLE::SAMPLE_SIMPLE_09), 7, 0, { 10, 20 }, 0);
    template_clique_length_process_data(simple_sample_factory::create_sample(SAMPLE_SIMPLE::SAMPLE_SIMPLE_09), 2, 0, { 30 }, 0);
}

TEST(utest_clique, allocation_sample_simple_10) {
    template_clique_length_process_data(simple_sample_factory::create_sample(SAMPLE_SIMPLE::SAMPLE_SIMPLE_10), 8, 0, { 11, 11, 11 }, 0);
    template_clique_length_process_data(simple_sample_factory::create_sample(SAMPLE_SIMPLE::SAMPLE_SIMPLE_10), 7, 0, { 11, 11, 11 }, 0);
    template_clique_length_process_data(simple_sample_factory::create_sample(SAMPLE_SIMPLE::SAMPLE_SIMPLE_10), 2, 0, { 33 }, 0);
    template_clique_length_process_data(simple_sample_factory::create_sample(SAMPLE_SIMPLE::SAMPLE_SIMPLE_10), 1, 0, { 33 }, 0);
}

TEST(utest_clique, allocation_three_dimensional_data1) {
    template_clique_length_process_data(simple_sample_factory::create_sample(SAMPLE_SIMPLE::SAMPLE_SIMPLE_11), 6, 0, { 10, 10 }, 0);
    template_clique_length_process_data(simple_sample_factory::create_sample(SAMPLE_SIMPLE::SAMPLE_SIMPLE_11), 5, 0, { 10, 10 }, 0);
    template_clique_length_process_data(simple_sample_factory::create_sample(SAMPLE_SIMPLE::SAMPLE_SIMPLE_11), 1, 0, { 20 }, 0);
}

TEST(utest_clique, allocation_similar_points) {
    template_clique_length_process_data(simple_sample_factory::create_sample(SAMPLE_SIMPLE::SAMPLE_SIMPLE_12), 8, 0, { 5, 5, 5 }, 0);
    template_clique_length_process_data(simple_sample_factory::create_sample(SAMPLE_SIMPLE::SAMPLE_SIMPLE_12), 7, 0, { 5, 5, 5 }, 0);
    template_clique_length_process_data(simple_sample_factory::create_sample(SAMPLE_SIMPLE::SAMPLE_SIMPLE_12), 5, 0, { 5, 5, 5 }, 0);
    template_clique_length_process_data(simple_sample_factory::create_sample(SAMPLE_SIMPLE::SAMPLE_SIMPLE_12), 2, 0, { 15 }, 0);
}

TEST(utest_clique, allocation_zero_column) {
    template_clique_length_process_data(simple_sample_factory::create_sample(SAMPLE_SIMPLE::SAMPLE_SIMPLE_13), 3, 0, { 5, 5 }, 0);
    template_clique_length_process_data(simple_sample_factory::create_sample(SAMPLE_SIMPLE::SAMPLE_SIMPLE_13), 2, 0, { 5, 5 }, 0);
    template_clique_length_process_data(simple_sample_factory::create_sample(SAMPLE_SIMPLE::SAMPLE_SIMPLE_13), 1, 0, { 10 }, 0);
}

TEST(utest_clique, allocation_fcps_lsun) {
    template_clique_length_process_data(fcps_sample_factory::create_sample(FCPS_SAMPLE::LSUN), 15, 0, { 100, 101, 202 }, 0);
}

TEST(utest_clique, allocation_fcps_hepta) {
    template_clique_length_process_data(fcps_sample_factory::create_sample(FCPS_SAMPLE::HEPTA), 9, 0, { 30, 30, 30, 30, 30, 30, 32 }, 0);
}

TEST(utest_clique, allocation_fcps_wingnut) {
    template_clique_length_process_data(fcps_sample_factory::create_sample(FCPS_SAMPLE::WING_NUT), 15, 0, { 508, 508 }, 0);
}

TEST(utest_clique, allocation_fcps_target) {
    template_clique_length_process_data(fcps_sample_factory::create_sample(FCPS_SAMPLE::TARGET), 10, 0, { 3, 3, 3, 3, 363, 395 }, 0);
}
