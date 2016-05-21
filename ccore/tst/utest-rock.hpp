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

#ifndef TST_UTEST_ROCK_HPP_
#define TST_UTEST_ROCK_HPP_


#include "gtest/gtest.h"

#include "cluster/rock.hpp"

#include "samples.hpp"
#include "utest-cluster.hpp"


using namespace cluster_analysis;


static void
template_length_process_data(const std::shared_ptr<dataset> & p_data,
        const double p_radius,
        const size_t p_cluster_amount,
        const double p_threshold,
        const std::vector<size_t> & p_expected_cluster_length) {

    rock_data output_result;
    rock solver(p_radius, p_cluster_amount, p_threshold);
    solver.process(*p_data, output_result);

    const dataset & data = *p_data;
    const cluster_sequence & actual_clusters = *(output_result.clusters());
    ASSERT_CLUSTER_SIZES(data, actual_clusters, p_expected_cluster_length);
}


TEST(utest_rock, allocation_sample_simple_01) {
    const std::vector<size_t> expected_clusters_length = { 5, 5 };
    template_length_process_data(simple_sample_factory::create_sample(SAMPLE_SIMPLE::SAMPLE_SIMPLE_01), 1.0, 2, 0.5, expected_clusters_length);
}


TEST(utest_rock, allocation_sample_one_allocation_simple_01) {
    const std::vector<size_t> expected_clusters_length = { 10 };
    template_length_process_data(simple_sample_factory::create_sample(SAMPLE_SIMPLE::SAMPLE_SIMPLE_01), 5.0, 1, 0.5, expected_clusters_length);
}

TEST(utest_rock, allocation_sample_simple_02) {
    const std::vector<size_t> expected_clusters_length = { 10, 5, 8 };
    template_length_process_data(simple_sample_factory::create_sample(SAMPLE_SIMPLE::SAMPLE_SIMPLE_02), 1.0, 3, 0.5, expected_clusters_length);
}


TEST(utest_rock, allocation_one_allocation_sample_simple_02) {
    const std::vector<size_t> expected_clusters_length = { 23 };
    template_length_process_data(simple_sample_factory::create_sample(SAMPLE_SIMPLE::SAMPLE_SIMPLE_02), 5.0, 1, 0.5, expected_clusters_length);
}


TEST(utest_rock, allocation_sample_simple_03) {
    const std::vector<size_t> expected_clusters_length = { 10, 10, 10, 30 };
    template_length_process_data(simple_sample_factory::create_sample(SAMPLE_SIMPLE::SAMPLE_SIMPLE_03), 1.0, 4, 0.5, expected_clusters_length);
}


TEST(utest_rock, allocation_wrong_radius_sample_simple_03) {
    const std::vector<size_t> expected_clusters_length = { 10, 10, 10, 30 };
    template_length_process_data(simple_sample_factory::create_sample(SAMPLE_SIMPLE::SAMPLE_SIMPLE_03), 1.7, 4, 0.5, expected_clusters_length);
}


TEST(utest_rock, allocation_sample_simple_04) {
    const std::vector<size_t> expected_clusters_length = { 15, 15, 15, 15, 15 };
    template_length_process_data(simple_sample_factory::create_sample(SAMPLE_SIMPLE::SAMPLE_SIMPLE_04), 1.0, 5, 0.5, expected_clusters_length);
}


TEST(utest_rock, allocation_wrong_radius_sample_simple_04) {
    const std::vector<size_t> expected_clusters_length = { 15, 15, 15, 15, 15 };
    template_length_process_data(simple_sample_factory::create_sample(SAMPLE_SIMPLE::SAMPLE_SIMPLE_04), 1.5, 5, 0.5, expected_clusters_length);
}


TEST(utest_rock, allocation_sample_simple_05) {
    const std::vector<size_t> expected_clusters_length = { 15, 15, 15, 15 };
    template_length_process_data(simple_sample_factory::create_sample(SAMPLE_SIMPLE::SAMPLE_SIMPLE_05), 1.0, 4, 0.5, expected_clusters_length);
}


TEST(utest_rock, allocation_sample_simple_07) {
    const std::vector<size_t> expected_clusters_length = { 10, 10 };
    template_length_process_data(simple_sample_factory::create_sample(SAMPLE_SIMPLE::SAMPLE_SIMPLE_07), 1.0, 2, 0.5, expected_clusters_length);
}


TEST(utest_rock, allocation_sample_simple_08) {
    const std::vector<size_t> expected_clusters_length = { 15, 30, 20, 80 };
    template_length_process_data(simple_sample_factory::create_sample(SAMPLE_SIMPLE::SAMPLE_SIMPLE_08), 1.0, 4, 0.5, expected_clusters_length);
}


#endif
