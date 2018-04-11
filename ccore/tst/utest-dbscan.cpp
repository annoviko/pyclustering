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


#include "gtest/gtest.h"

#include "cluster/dbscan.hpp"

#include "utils/metric.hpp"

#include "samples.hpp"

#include "utenv_check.hpp"


using namespace ccore::clst;
using namespace ccore::utils::metric;


static std::shared_ptr<dbscan_data>
template_length_process_data(const std::shared_ptr<dataset> & p_data,
        const double p_radius,
        const size_t p_neighbors,
        const std::vector<size_t> & p_expected_cluster_length)
{
    std::shared_ptr<dbscan_data> ptr_output_result = std::make_shared<dbscan_data>();
    dbscan solver(p_radius, p_neighbors);
    solver.process(*p_data, *ptr_output_result);

    const dataset & data = *p_data;
    const cluster_sequence & actual_clusters = ptr_output_result->clusters();

    ASSERT_CLUSTER_SIZES(data, actual_clusters, p_expected_cluster_length);

    return ptr_output_result;
}


static std::shared_ptr<dbscan_data>
template_length_process_distance_matrix(const std::shared_ptr<dataset> & p_data,
        const double p_radius,
        const size_t p_neighbors,
        const std::vector<size_t> & p_expected_cluster_length)
{
    std::shared_ptr<dbscan_data> ptr_output_result = std::make_shared<dbscan_data>();
    dbscan solver(p_radius, p_neighbors);

    dataset matrix;
    distance_matrix(*p_data, matrix);

    solver.process(matrix, dbscan_data_t::DISTANCE_MATRIX, *ptr_output_result);

    const dataset & data = *p_data;
    const cluster_sequence & actual_clusters = ptr_output_result->clusters();

    ASSERT_CLUSTER_SIZES(data, actual_clusters, p_expected_cluster_length);

    return ptr_output_result;
}


TEST(utest_dbscan, allocation_sample_simple_01) {
    const std::vector<size_t> expected_clusters_length = { 5, 5 };
    template_length_process_data(simple_sample_factory::create_sample(SAMPLE_SIMPLE::SAMPLE_SIMPLE_01), 0.5, 2, expected_clusters_length);
}


TEST(utest_dbscan, allocation_sample_simple_01_distance_matrix) {
    const std::vector<size_t> expected_clusters_length = { 5, 5 };
    template_length_process_distance_matrix(simple_sample_factory::create_sample(SAMPLE_SIMPLE::SAMPLE_SIMPLE_01), 0.5, 2, expected_clusters_length);
}


TEST(utest_dbscan, allocation_sample_one_allocation_simple_01) {
    const std::vector<size_t> expected_clusters_length = { 10 };
    template_length_process_data(simple_sample_factory::create_sample(SAMPLE_SIMPLE::SAMPLE_SIMPLE_01), 10.0, 2, expected_clusters_length);
}


TEST(utest_dbscan, allocation_sample_one_allocation_simple_01_distance_matrix) {
    const std::vector<size_t> expected_clusters_length = { 10 };
    template_length_process_distance_matrix(simple_sample_factory::create_sample(SAMPLE_SIMPLE::SAMPLE_SIMPLE_01), 10.0, 2, expected_clusters_length);
}


TEST(utest_dbscan, allocation_sample_simple_02) {
    const std::vector<size_t> expected_clusters_length = { 10, 5, 8 };
    template_length_process_data(simple_sample_factory::create_sample(SAMPLE_SIMPLE::SAMPLE_SIMPLE_02), 1.0, 2, expected_clusters_length);
}


TEST(utest_dbscan, allocation_sample_simple_02_distance_matrix) {
    const std::vector<size_t> expected_clusters_length = { 10, 5, 8 };
    template_length_process_distance_matrix(simple_sample_factory::create_sample(SAMPLE_SIMPLE::SAMPLE_SIMPLE_02), 1.0, 2, expected_clusters_length);
}


TEST(utest_dbscan, allocation_one_allocation_sample_simple_02) {
    const std::vector<size_t> expected_clusters_length = { 23 };
    template_length_process_data(simple_sample_factory::create_sample(SAMPLE_SIMPLE::SAMPLE_SIMPLE_02), 5.0, 2, expected_clusters_length);
}


TEST(utest_dbscan, allocation_one_allocation_sample_simple_02_distance_matrix) {
    const std::vector<size_t> expected_clusters_length = { 23 };
    template_length_process_distance_matrix(simple_sample_factory::create_sample(SAMPLE_SIMPLE::SAMPLE_SIMPLE_02), 5.0, 2, expected_clusters_length);
}


TEST(utest_dbscan, allocation_sample_simple_03) {
    const std::vector<size_t> expected_clusters_length = { 10, 10, 10, 30 };
    template_length_process_data(simple_sample_factory::create_sample(SAMPLE_SIMPLE::SAMPLE_SIMPLE_03), 0.7, 3, expected_clusters_length);
}


TEST(utest_dbscan, allocation_sample_simple_03_distance_matrix) {
    const std::vector<size_t> expected_clusters_length = { 10, 10, 10, 30 };
    template_length_process_distance_matrix(simple_sample_factory::create_sample(SAMPLE_SIMPLE::SAMPLE_SIMPLE_03), 0.7, 3, expected_clusters_length);
}


TEST(utest_dbscan, allocation_sample_simple_04) {
    const std::vector<size_t> expected_clusters_length = { 15, 15, 15, 15, 15 };
    template_length_process_data(simple_sample_factory::create_sample(SAMPLE_SIMPLE::SAMPLE_SIMPLE_04), 0.7, 3, expected_clusters_length);
}


TEST(utest_dbscan, allocation_sample_simple_04_distance_matrix) {
    const std::vector<size_t> expected_clusters_length = { 15, 15, 15, 15, 15 };
    template_length_process_distance_matrix(simple_sample_factory::create_sample(SAMPLE_SIMPLE::SAMPLE_SIMPLE_04), 0.7, 3, expected_clusters_length);
}


TEST(utest_dbscan, allocation_sample_simple_05) {
    const std::vector<size_t> expected_clusters_length = { 15, 15, 15, 15 };
    template_length_process_data(simple_sample_factory::create_sample(SAMPLE_SIMPLE::SAMPLE_SIMPLE_05), 0.7, 3, expected_clusters_length);
}


TEST(utest_dbscan, allocation_sample_simple_05_distance_matrix) {
    const std::vector<size_t> expected_clusters_length = { 15, 15, 15, 15 };
    template_length_process_distance_matrix(simple_sample_factory::create_sample(SAMPLE_SIMPLE::SAMPLE_SIMPLE_05), 0.7, 3, expected_clusters_length);
}


TEST(utest_dbscan, allocation_sample_simple_07) {
    const std::vector<size_t> expected_clusters_length = { 10, 10 };
    template_length_process_data(simple_sample_factory::create_sample(SAMPLE_SIMPLE::SAMPLE_SIMPLE_07), 0.5, 3, expected_clusters_length);
}


TEST(utest_dbscan, allocation_sample_simple_07_distance_matrix) {
    const std::vector<size_t> expected_clusters_length = { 10, 10 };
    template_length_process_distance_matrix(simple_sample_factory::create_sample(SAMPLE_SIMPLE::SAMPLE_SIMPLE_07), 0.5, 3, expected_clusters_length);
}


TEST(utest_dbscan, allocation_sample_simple_08) {
    const std::vector<size_t> expected_clusters_length = { 15, 30, 20, 80 };
    template_length_process_data(simple_sample_factory::create_sample(SAMPLE_SIMPLE::SAMPLE_SIMPLE_08), 0.5, 3, expected_clusters_length);
}


TEST(utest_dbscan, allocation_sample_simple_08_distance_matrix) {
    const std::vector<size_t> expected_clusters_length = { 15, 30, 20, 80 };
    template_length_process_distance_matrix(simple_sample_factory::create_sample(SAMPLE_SIMPLE::SAMPLE_SIMPLE_08), 0.5, 3, expected_clusters_length);
}


static std::shared_ptr<dbscan_data>
template_noise_allocation(const std::shared_ptr<dataset> & p_data,
        const double p_radius,
        const size_t p_neighbors,
        const std::vector<size_t> & p_expected_cluster_length,
        const std::size_t p_noise_length) {

    std::shared_ptr<dbscan_data> ptr_output_result = template_length_process_data(p_data, p_radius, p_neighbors, p_expected_cluster_length);
    EXPECT_EQ(p_noise_length, ptr_output_result->noise().size());

    return ptr_output_result;
}


static std::shared_ptr<dbscan_data>
template_noise_allocation_distance_matrix(const std::shared_ptr<dataset> & p_data,
        const double p_radius,
        const size_t p_neighbors,
        const std::vector<size_t> & p_expected_cluster_length,
        const std::size_t p_noise_length) {

    std::shared_ptr<dbscan_data> ptr_output_result = template_length_process_distance_matrix(p_data, p_radius, p_neighbors, p_expected_cluster_length);
    EXPECT_EQ(p_noise_length, ptr_output_result->noise().size());

    return ptr_output_result;
}


TEST(utest_dbscan, noise_allocation_sample_simple_01) {
    const std::vector<size_t> expected_clusters_length = { };
    template_noise_allocation(simple_sample_factory::create_sample(SAMPLE_SIMPLE::SAMPLE_SIMPLE_01), 10.0, 20, expected_clusters_length, 10);
}


TEST(utest_dbscan, noise_allocation_sample_simple_01_distance_matrix) {
    const std::vector<size_t> expected_clusters_length = { };
    template_noise_allocation_distance_matrix(simple_sample_factory::create_sample(SAMPLE_SIMPLE::SAMPLE_SIMPLE_01), 10.0, 20, expected_clusters_length, 10);
}


TEST(utest_dbscan, noise_allocation_sample_simple_02) {
    const std::vector<size_t> expected_clusters_length = { };
    template_noise_allocation(simple_sample_factory::create_sample(SAMPLE_SIMPLE::SAMPLE_SIMPLE_02), 0.5, 20, expected_clusters_length, 23);
}


TEST(utest_dbscan, noise_allocation_sample_simple_02_distance_matrix) {
    const std::vector<size_t> expected_clusters_length = { };
    template_noise_allocation_distance_matrix(simple_sample_factory::create_sample(SAMPLE_SIMPLE::SAMPLE_SIMPLE_02), 0.5, 20, expected_clusters_length, 23);
}


TEST(utest_dbscan, noise_cluster_allocation_sample_simple_02) {
    const std::vector<size_t> expected_clusters_length = { 10 };
    template_noise_allocation(simple_sample_factory::create_sample(SAMPLE_SIMPLE::SAMPLE_SIMPLE_02), 2.0, 9, expected_clusters_length, 13);
}


TEST(utest_dbscan, noise_cluster_allocation_sample_simple_02_distance_matrix) {
    const std::vector<size_t> expected_clusters_length = { 10 };
    template_noise_allocation_distance_matrix(simple_sample_factory::create_sample(SAMPLE_SIMPLE::SAMPLE_SIMPLE_02), 2.0, 9, expected_clusters_length, 13);
}
