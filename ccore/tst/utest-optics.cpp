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


#include "gtest/gtest.h"

#include "cluster/optics.hpp"
#include "cluster/ordering_analyser.hpp"

#include "samples.hpp"
#include "utest-cluster.hpp"


static std::shared_ptr<optics_data>
template_optics_length_process_data(const std::shared_ptr<dataset> & p_data,
        const double p_radius,
        const size_t p_neighbors,
        const size_t p_amount_clusters,
        const std::vector<size_t> & p_expected_cluster_length) {

    std::shared_ptr<optics_data> ptr_output_result = std::make_shared<optics_data>();
    optics solver(p_radius, p_neighbors, p_amount_clusters);
    solver.process(*p_data, *ptr_output_result);

    const dataset & data = *p_data;
    const cluster_sequence & actual_clusters = *(ptr_output_result->clusters());

    ASSERT_CLUSTER_SIZES(data, actual_clusters, p_expected_cluster_length);
    if (p_amount_clusters > 0) {
        ordering_analyser analyser(ptr_output_result->ordering());
        EXPECT_EQ(p_expected_cluster_length.size(), analyser.extract_cluster_amount(ptr_output_result->get_radius()));
    }

    return ptr_output_result;
}


TEST(utest_optics, allocation_sample_simple_01) {
    const std::vector<size_t> expected_clusters_length = { 5, 5 };
    template_optics_length_process_data(simple_sample_factory::create_sample(SAMPLE_SIMPLE::SAMPLE_SIMPLE_01), 0.4, 2, 0, expected_clusters_length);
}


TEST(utest_optics, allocation_one_allocation_simple_01) {
    const std::vector<size_t> expected_clusters_length = { 10 };
    template_optics_length_process_data(simple_sample_factory::create_sample(SAMPLE_SIMPLE::SAMPLE_SIMPLE_01), 10.0, 1, 0, expected_clusters_length);
}


TEST(utest_optics, allocation_sample_simple_02) {
    const std::vector<size_t> expected_clusters_length = { 10, 5, 8 };
    template_optics_length_process_data(simple_sample_factory::create_sample(SAMPLE_SIMPLE::SAMPLE_SIMPLE_02), 1.0, 2, 0, expected_clusters_length);
}


TEST(utest_optics, allocation_one_allocation_sample_simple_02) {
    const std::vector<size_t> expected_clusters_length = { 23 };
    template_optics_length_process_data(simple_sample_factory::create_sample(SAMPLE_SIMPLE::SAMPLE_SIMPLE_02), 5.0, 1, 0, expected_clusters_length);
}


TEST(utest_optics, allocation_sample_simple_03) {
    const std::vector<size_t> expected_clusters_length = { 10, 10, 10, 30 };
    template_optics_length_process_data(simple_sample_factory::create_sample(SAMPLE_SIMPLE::SAMPLE_SIMPLE_03), 0.7, 3, 0, expected_clusters_length);
}


TEST(utest_optics, allocation_sample_simple_04) {
    const std::vector<size_t> expected_clusters_length = { 15, 15, 15, 15, 15 };
    template_optics_length_process_data(simple_sample_factory::create_sample(SAMPLE_SIMPLE::SAMPLE_SIMPLE_04), 0.7, 3, 0, expected_clusters_length);
}


TEST(utest_optics, allocation_sample_simple_05) {
    const std::vector<size_t> expected_clusters_length = { 15, 15, 15, 15 };
    template_optics_length_process_data(simple_sample_factory::create_sample(SAMPLE_SIMPLE::SAMPLE_SIMPLE_05), 0.7, 3, 0, expected_clusters_length);
}


TEST(utest_optics, allocation_sample_lsun) {
    const std::vector<size_t> expected_clusters_length = { 100, 101, 202 };
    template_optics_length_process_data(fcps_sample_factory::create_sample(FCPS_SAMPLE::LSUN), 0.5, 3, 0, expected_clusters_length);
}



TEST(utest_optics, allocation_sample_simple_02_large_radius) {
    const std::vector<size_t> expected_clusters_length = { 10, 5, 8 };
    template_optics_length_process_data(simple_sample_factory::create_sample(SAMPLE_SIMPLE::SAMPLE_SIMPLE_02), 5.0, 2, 3, expected_clusters_length);
}


TEST(utest_optics, allocation_sample_simple_03_large_radius) {
    const std::vector<size_t> expected_clusters_length = { 10, 10, 10, 30 };
    template_optics_length_process_data(simple_sample_factory::create_sample(SAMPLE_SIMPLE::SAMPLE_SIMPLE_03), 7.0, 4, 4, expected_clusters_length);
}


TEST(utest_optics, allocation_sample_simple_04_large_radius) {
    const std::vector<size_t> expected_clusters_length = { 15, 15, 15, 15, 15 };
    template_optics_length_process_data(simple_sample_factory::create_sample(SAMPLE_SIMPLE::SAMPLE_SIMPLE_04), 50.0, 5, 5, expected_clusters_length);
}


TEST(utest_optics, allocation_sample_simple_05_large_radius) {
    const std::vector<size_t> expected_clusters_length = { 15, 15, 15, 15 };
    template_optics_length_process_data(simple_sample_factory::create_sample(SAMPLE_SIMPLE::SAMPLE_SIMPLE_05), 10.0, 10, 4, expected_clusters_length);
}


TEST(utest_optics, allocation_sample_lsun_large_radius_10) {
    const std::vector<size_t> expected_clusters_length = { 99, 100, 202 };
    template_optics_length_process_data(fcps_sample_factory::create_sample(FCPS_SAMPLE::LSUN), 1.0, 3, 3, expected_clusters_length);
}


TEST(utest_optics, allocation_sample_lsun_large_radius_19) {
    const std::vector<size_t> expected_clusters_length = { 99, 100, 202 };
    template_optics_length_process_data(fcps_sample_factory::create_sample(FCPS_SAMPLE::LSUN), 1.9, 3, 3, expected_clusters_length);
}


static std::shared_ptr<optics_data>
template_optics_noise_allocation(const std::shared_ptr<dataset> & p_data,
        const double p_radius,
        const size_t p_neighbors,
        const size_t p_amount_clusters,
        const std::vector<size_t> & p_expected_cluster_length,
        const std::size_t p_noise_length) {

    std::shared_ptr<optics_data> ptr_output_result = template_optics_length_process_data(p_data, p_radius, p_neighbors, p_amount_clusters, p_expected_cluster_length);
    EXPECT_EQ(p_noise_length, ptr_output_result->noise()->size());

    return ptr_output_result;
}


TEST(utest_optics, noise_allocation_sample_simple_01) {
    const std::vector<size_t> expected_clusters_length = { };
    template_optics_noise_allocation(simple_sample_factory::create_sample(SAMPLE_SIMPLE::SAMPLE_SIMPLE_01), 10.0, 20, 0, expected_clusters_length, 10);
}


TEST(utest_optics, noise_allocation_sample_simple_02) {
    const std::vector<size_t> expected_clusters_length = { };
    template_optics_noise_allocation(simple_sample_factory::create_sample(SAMPLE_SIMPLE::SAMPLE_SIMPLE_02), 0.5, 20, 0, expected_clusters_length, 23);
}


TEST(utest_optics, noise_cluster_allocation_sample_simple_02) {
    const std::vector<size_t> expected_clusters_length = { 10 };
    template_optics_noise_allocation(simple_sample_factory::create_sample(SAMPLE_SIMPLE::SAMPLE_SIMPLE_02), 2.0, 9, 0, expected_clusters_length, 13);
}
