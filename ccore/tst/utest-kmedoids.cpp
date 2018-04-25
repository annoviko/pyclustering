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

#include "cluster/kmedoids.hpp"

#include "utils/metric.hpp"

#include "samples.hpp"
#include "utenv_check.hpp"


using namespace ccore::clst;


static void
template_kmedoids_length_process_data(const dataset_ptr p_data,
        const medoid_sequence & p_start_medians,
        const std::vector<size_t> & p_expected_cluster_length,
        const distance_metric<point> & p_metric = distance_metric_factory<point>::euclidean_square()) {

    kmedoids_data output_result;
    kmedoids solver(p_start_medians, 0.0001, p_metric);
    solver.process(*p_data, output_result);

    const dataset & data = *p_data;
    const cluster_sequence & actual_clusters = output_result.clusters();

    ASSERT_EQ(p_start_medians.size(), actual_clusters.size());
    ASSERT_CLUSTER_SIZES(data, actual_clusters, p_expected_cluster_length);
}


static void
template_kmedoids_length_process_distance_matrix(const dataset_ptr p_data,
        const medoid_sequence & p_start_medians,
        const std::vector<size_t> & p_expected_cluster_length,
        const distance_metric<point> & p_metric = distance_metric_factory<point>::euclidean_square()) {

    dataset matrix;
    distance_matrix(*p_data, matrix);

    kmedoids_data output_result;
    kmedoids solver(p_start_medians, 0.0001, p_metric);
    solver.process(matrix, kmedoids_data_t::DISTANCE_MATRIX, output_result);

    const dataset & data = *p_data;
    const cluster_sequence & actual_clusters = output_result.clusters();

    ASSERT_EQ(p_start_medians.size(), actual_clusters.size());
    ASSERT_CLUSTER_SIZES(data, actual_clusters, p_expected_cluster_length);
}


TEST(utest_kmedoids, allocation_sample_simple_01) {
    const medoid_sequence start_medoids = { 1, 5 };
    const std::vector<size_t> expected_clusters_length = { 5, 5 };
    template_kmedoids_length_process_data(simple_sample_factory::create_sample(SAMPLE_SIMPLE::SAMPLE_SIMPLE_01), start_medoids, expected_clusters_length);
}


TEST(utest_kmedoids, allocation_sample_simple_01_distance_matrix) {
    const medoid_sequence start_medoids = { 1, 5 };
    const std::vector<size_t> expected_clusters_length = { 5, 5 };
    template_kmedoids_length_process_distance_matrix(simple_sample_factory::create_sample(SAMPLE_SIMPLE::SAMPLE_SIMPLE_01), start_medoids, expected_clusters_length);
}


TEST(utest_kmedoids, allocation_sample_simple_01_euclidean) {
    const medoid_sequence start_medoids = { 1, 5 };
    const std::vector<size_t> expected_clusters_length = { 5, 5 };
    template_kmedoids_length_process_data(simple_sample_factory::create_sample(SAMPLE_SIMPLE::SAMPLE_SIMPLE_01), start_medoids, expected_clusters_length, distance_metric_factory<point>::euclidean());
}


TEST(utest_kmedoids, allocation_sample_simple_01_euclidean_distance_matrix) {
    const medoid_sequence start_medoids = { 1, 5 };
    const std::vector<size_t> expected_clusters_length = { 5, 5 };
    template_kmedoids_length_process_distance_matrix(simple_sample_factory::create_sample(SAMPLE_SIMPLE::SAMPLE_SIMPLE_01), start_medoids, expected_clusters_length, distance_metric_factory<point>::euclidean());
}


TEST(utest_kmedoids, allocation_sample_simple_01_euclidean_square) {
    const medoid_sequence start_medoids = { 1, 5 };
    const std::vector<size_t> expected_clusters_length = { 5, 5 };
    template_kmedoids_length_process_data(simple_sample_factory::create_sample(SAMPLE_SIMPLE::SAMPLE_SIMPLE_01), start_medoids, expected_clusters_length, distance_metric_factory<point>::euclidean_square());
}


TEST(utest_kmedoids, allocation_sample_simple_01_euclidean_square_distance_matrix) {
    const medoid_sequence start_medoids = { 1, 5 };
    const std::vector<size_t> expected_clusters_length = { 5, 5 };
    template_kmedoids_length_process_distance_matrix(simple_sample_factory::create_sample(SAMPLE_SIMPLE::SAMPLE_SIMPLE_01), start_medoids, expected_clusters_length, distance_metric_factory<point>::euclidean_square());
}


TEST(utest_kmedoids, allocation_sample_simple_01_manhattan) {
    const medoid_sequence start_medoids = { 1, 5 };
    const std::vector<size_t> expected_clusters_length = { 5, 5 };
    template_kmedoids_length_process_data(simple_sample_factory::create_sample(SAMPLE_SIMPLE::SAMPLE_SIMPLE_01), start_medoids, expected_clusters_length, distance_metric_factory<point>::manhattan());
}


TEST(utest_kmedoids, allocation_sample_simple_01_manhattan_distance_matrix) {
    const medoid_sequence start_medoids = { 1, 5 };
    const std::vector<size_t> expected_clusters_length = { 5, 5 };
    template_kmedoids_length_process_distance_matrix(simple_sample_factory::create_sample(SAMPLE_SIMPLE::SAMPLE_SIMPLE_01), start_medoids, expected_clusters_length, distance_metric_factory<point>::manhattan());
}


TEST(utest_kmedoids, allocation_sample_simple_01_chebyshev) {
    const medoid_sequence start_medoids = { 1, 5 };
    const std::vector<size_t> expected_clusters_length = { 5, 5 };
    template_kmedoids_length_process_data(simple_sample_factory::create_sample(SAMPLE_SIMPLE::SAMPLE_SIMPLE_01), start_medoids, expected_clusters_length, distance_metric_factory<point>::chebyshev());
}


TEST(utest_kmedoids, allocation_sample_simple_01_chebyshev_distance_matrix) {
    const medoid_sequence start_medoids = { 1, 5 };
    const std::vector<size_t> expected_clusters_length = { 5, 5 };
    template_kmedoids_length_process_distance_matrix(simple_sample_factory::create_sample(SAMPLE_SIMPLE::SAMPLE_SIMPLE_01), start_medoids, expected_clusters_length, distance_metric_factory<point>::chebyshev());
}


TEST(utest_kmedoids, allocation_sample_simple_01_minkowski) {
    const medoid_sequence start_medoids = { 1, 5 };
    const std::vector<size_t> expected_clusters_length = { 5, 5 };
    template_kmedoids_length_process_data(simple_sample_factory::create_sample(SAMPLE_SIMPLE::SAMPLE_SIMPLE_01), start_medoids, expected_clusters_length, distance_metric_factory<point>::minkowski(2.0));
}


TEST(utest_kmedoids, allocation_sample_simple_01_minkowski_distance_matrix) {
    const medoid_sequence start_medoids = { 1, 5 };
    const std::vector<size_t> expected_clusters_length = { 5, 5 };
    template_kmedoids_length_process_distance_matrix(simple_sample_factory::create_sample(SAMPLE_SIMPLE::SAMPLE_SIMPLE_01), start_medoids, expected_clusters_length, distance_metric_factory<point>::minkowski(2.0));
}


TEST(utest_kmedoids, allocation_sample_simple_01_user_defined) {
    const medoid_sequence start_medoids = { 1, 5 };
    const std::vector<size_t> expected_clusters_length = { 5, 5 };

    auto user_metric = [](const point & p1, const point & p2) { return euclidean_distance(p1, p2); };

    template_kmedoids_length_process_data(simple_sample_factory::create_sample(SAMPLE_SIMPLE::SAMPLE_SIMPLE_01), start_medoids, expected_clusters_length, distance_metric_factory<point>::user_defined(user_metric));
}


TEST(utest_kmedoids, allocation_sample_simple_01_user_defined_distance_matrix) {
    const medoid_sequence start_medoids = { 1, 5 };
    const std::vector<size_t> expected_clusters_length = { 5, 5 };

    auto user_metric = [](const point & p1, const point & p2) { return euclidean_distance(p1, p2); };

    template_kmedoids_length_process_distance_matrix(simple_sample_factory::create_sample(SAMPLE_SIMPLE::SAMPLE_SIMPLE_01), start_medoids, expected_clusters_length, distance_metric_factory<point>::user_defined(user_metric));
}


TEST(utest_kmedoids, allocation_sample_one_allocation_simple_01) {
    const medoid_sequence start_medoids = { 1 };
    const std::vector<size_t> expected_clusters_length = { 10 };
    template_kmedoids_length_process_data(simple_sample_factory::create_sample(SAMPLE_SIMPLE::SAMPLE_SIMPLE_01), start_medoids, expected_clusters_length);
}


TEST(utest_kmedoids, allocation_sample_one_allocation_simple_01_distance_matrix) {
    const medoid_sequence start_medoids = { 1 };
    const std::vector<size_t> expected_clusters_length = { 10 };
    template_kmedoids_length_process_distance_matrix(simple_sample_factory::create_sample(SAMPLE_SIMPLE::SAMPLE_SIMPLE_01), start_medoids, expected_clusters_length);
}


TEST(utest_kmedoids, allocation_sample_simple_02) {
    const medoid_sequence start_medoids = { 3, 12, 20 };
    const std::vector<size_t> expected_clusters_length = { 10, 5, 8 };
    template_kmedoids_length_process_data(simple_sample_factory::create_sample(SAMPLE_SIMPLE::SAMPLE_SIMPLE_02), start_medoids, expected_clusters_length);
}


TEST(utest_kmedoids, allocation_sample_simple_02_distance_matrix) {
    const medoid_sequence start_medoids = { 3, 12, 20 };
    const std::vector<size_t> expected_clusters_length = { 10, 5, 8 };
    template_kmedoids_length_process_distance_matrix(simple_sample_factory::create_sample(SAMPLE_SIMPLE::SAMPLE_SIMPLE_02), start_medoids, expected_clusters_length);
}


TEST(utest_kmedoids, allocation_one_allocation_sample_simple_02) {
    const medoid_sequence start_medoids = { 10 };
    const std::vector<size_t> expected_clusters_length = { 23 };
    template_kmedoids_length_process_data(simple_sample_factory::create_sample(SAMPLE_SIMPLE::SAMPLE_SIMPLE_02), start_medoids, expected_clusters_length);
}


TEST(utest_kmedoids, allocation_one_allocation_sample_simple_02_distance_matrix) {
    const medoid_sequence start_medoids = { 10 };
    const std::vector<size_t> expected_clusters_length = { 23 };
    template_kmedoids_length_process_distance_matrix(simple_sample_factory::create_sample(SAMPLE_SIMPLE::SAMPLE_SIMPLE_02), start_medoids, expected_clusters_length);
}


TEST(utest_kmedoids, allocation_sample_simple_03) {
    const medoid_sequence start_medoids = { 4, 12, 25, 37 };
    const std::vector<size_t> expected_clusters_length = { 10, 10, 10, 30 };
    template_kmedoids_length_process_data(simple_sample_factory::create_sample(SAMPLE_SIMPLE::SAMPLE_SIMPLE_03), start_medoids, expected_clusters_length);
}


TEST(utest_kmedoids, allocation_sample_simple_04) {
    const medoid_sequence start_medoids = { 7, 22, 37, 52, 67 };
    const std::vector<size_t> expected_clusters_length = { 15, 15, 15, 15, 15 };
    template_kmedoids_length_process_data(simple_sample_factory::create_sample(SAMPLE_SIMPLE::SAMPLE_SIMPLE_04), start_medoids, expected_clusters_length);
}


TEST(utest_kmedoids, allocation_sample_simple_05) {
    const medoid_sequence start_medoids = { 7, 22, 37, 52 };
    const std::vector<size_t> expected_clusters_length = { 15, 15, 15, 15 };
    template_kmedoids_length_process_data(simple_sample_factory::create_sample(SAMPLE_SIMPLE::SAMPLE_SIMPLE_05), start_medoids, expected_clusters_length);
}


TEST(utest_kmedoids, allocation_sample_simple_07) {
    const medoid_sequence start_medoids = { 5, 15 };
    const std::vector<size_t> expected_clusters_length = { 10, 10 };
    template_kmedoids_length_process_data(simple_sample_factory::create_sample(SAMPLE_SIMPLE::SAMPLE_SIMPLE_07), start_medoids, expected_clusters_length);
}


TEST(utest_kmedoids, allocation_sample_simple_08) {
    const medoid_sequence start_medoids = { 5, 35, 50, 100 };
    const std::vector<size_t> expected_clusters_length = { 15, 30, 20, 80 };
    template_kmedoids_length_process_data(simple_sample_factory::create_sample(SAMPLE_SIMPLE::SAMPLE_SIMPLE_08), start_medoids, expected_clusters_length);
}


TEST(utest_kmedoids, allocation_wrong_initial_medoids_sample_simple_03) {
    const medoid_sequence start_medoids = { 4, 7, 12, 20, 25, 30, 37 };
    const std::vector<size_t> expected_clusters_length;     /* empty - just check index point existence */
    template_kmedoids_length_process_data(simple_sample_factory::create_sample(SAMPLE_SIMPLE::SAMPLE_SIMPLE_03), start_medoids, expected_clusters_length);
}


TEST(utest_kmedoids, allocation_wrong_initial_medoids_sample_simple_04) {
    const medoid_sequence start_medoids = { 2, 7, 15, 22, 30, 37, 40, 52, 62, 67 };
    const std::vector<size_t> expected_clusters_length;     /* empty - just check index point existence */
    template_kmedoids_length_process_data(simple_sample_factory::create_sample(SAMPLE_SIMPLE::SAMPLE_SIMPLE_04), start_medoids, expected_clusters_length);
}


TEST(utest_kmedoids, totally_similar_data) {
    const dataset_ptr dataset = simple_sample_factory::create_sample(SAMPLE_SIMPLE::SAMPLE_SIMPLE_12);
    const std::vector<size_t> expected_clusters_length;     /* empty - just check index point existence */

    medoid_sequence start_medoids = { 0, 2, 5, 7, 10, 12 };
    template_kmedoids_length_process_data(dataset, start_medoids, expected_clusters_length);

    start_medoids = { 0, 2, 4, 5, 7, 9, 10, 12, 14 };
    template_kmedoids_length_process_data(dataset, start_medoids, expected_clusters_length);

    start_medoids = { 0, 1, 2, 3, 4 };
    template_kmedoids_length_process_data(dataset, start_medoids, expected_clusters_length);
}
