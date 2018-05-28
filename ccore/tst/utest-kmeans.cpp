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

#include "samples.hpp"

#include "cluster/kmeans.hpp"

#include "utils/metric.hpp"

#include "utenv_check.hpp"


using namespace ccore::clst;
using namespace ccore::utils::metric;


static void
template_kmeans_length_process_data_common(const dataset_ptr & p_data,
                                           const dataset & p_start_centers,
                                           const std::vector<size_t> & p_expected_cluster_length,
                                           const index_sequence & p_indexes,
                                           const bool p_observe,
                                           const std::size_t p_parallel_processing_trigger,
                                           const distance_metric<point> & p_metric = distance_metric_factory<point>::euclidean_square())
{
    kmeans_data output_result(p_observe);
    kmeans solver(p_start_centers, 0.0001, p_metric);

    solver.set_parallel_processing_trigger(p_parallel_processing_trigger);

    if (p_indexes.empty()) {
        solver.process(*p_data, output_result);
    }
    else {
        solver.process(*p_data, p_indexes, output_result);
    }

    const dataset & data = *p_data;
    const std::size_t dimension = data[0].size();
    const cluster_sequence & actual_clusters = output_result.clusters();
    const dataset & centers = output_result.centers();

    ASSERT_CLUSTER_SIZES(data, actual_clusters, p_expected_cluster_length, p_indexes);

    for (auto center : centers) {
        ASSERT_EQ(dimension, center.size());
    }

    ASSERT_EQ(centers.size(), actual_clusters.size());

    ASSERT_EQ(p_observe, output_result.is_observed());
    if (output_result.is_observed()) {
        ASSERT_LE(1U, output_result.evolution_centers().size());
        ASSERT_LE(1U, output_result.evolution_clusters().size());

        for (auto & cluster : output_result.evolution_clusters()) {
            ASSERT_CLUSTER_SIZES(data, cluster, { }, p_indexes);
        }
    }
}


static void
template_kmeans_length_process_data_range(const dataset_ptr & p_data,
                                          const dataset & p_start_centers,
                                          const std::vector<size_t> & p_expected_cluster_length,
                                          const index_sequence & p_indexes,
                                          const std::size_t p_parallel_processing_trigger = kmeans::DEFAULT_DATA_SIZE_PARALLEL_PROCESSING)
{
    template_kmeans_length_process_data_common(p_data, p_start_centers, p_expected_cluster_length, p_indexes, false, p_parallel_processing_trigger);
}


static void
template_kmeans_length_process_data(const dataset_ptr & p_data,
                                    const dataset & p_start_centers,
                                    const std::vector<size_t> & p_expected_cluster_length,
                                    const std::size_t parallel_processing_trigger = kmeans::DEFAULT_DATA_SIZE_PARALLEL_PROCESSING)
{
    template_kmeans_length_process_data_range(p_data, p_start_centers, p_expected_cluster_length, { }, parallel_processing_trigger);
}


static void
template_kmeans_observer(const dataset_ptr & p_data,
                         const dataset & p_start_centers,
                         const index_sequence & p_indexes,
                         const std::vector<size_t> & p_expected_cluster_length)
{
    template_kmeans_length_process_data_common(p_data, p_start_centers, p_expected_cluster_length, p_indexes, true, kmeans::DEFAULT_DATA_SIZE_PARALLEL_PROCESSING);
}


static void
template_kmeans_metric(const dataset_ptr & p_data,
                       const dataset & p_start_centers,
                       const std::vector<size_t> & p_expected_cluster_length,
                       const distance_metric<point> & p_metric)
{
  template_kmeans_length_process_data_common(p_data, p_start_centers, p_expected_cluster_length, { }, false, kmeans::DEFAULT_DATA_SIZE_PARALLEL_PROCESSING, p_metric);
}



TEST(utest_kmeans, allocation_sample_simple_01) {
    dataset start_centers = { { 3.7, 5.5 },{ 6.7, 7.5 } };
    std::vector<size_t> expected_clusters_length = { 5, 5 };
    template_kmeans_length_process_data(simple_sample_factory::create_sample(SAMPLE_SIMPLE::SAMPLE_SIMPLE_01), start_centers, expected_clusters_length);
}

TEST(utest_kmeans, allocation_sample_simple_01_range) {
    dataset start_centers = { { 3.7, 5.5 },{ 6.7, 7.5 } };
    std::vector<size_t> expected_clusters_length = { 3, 3 };
    index_sequence range = { 0, 1, 2, 5, 6, 7 };
    template_kmeans_length_process_data_range(simple_sample_factory::create_sample(SAMPLE_SIMPLE::SAMPLE_SIMPLE_01), start_centers, expected_clusters_length, range);
}

TEST(utest_kmeans, one_cluster_allocation_sample_simple_01) {
    dataset start_centers = { { 1.0, 2.5 } };
    std::vector<size_t> expected_clusters_length = { 10 };
    template_kmeans_length_process_data(simple_sample_factory::create_sample(SAMPLE_SIMPLE::SAMPLE_SIMPLE_01), start_centers, expected_clusters_length);
}

TEST(utest_kmeans, one_cluster_allocation_sample_simple_01_range) {
    dataset start_centers = { { 1.0, 2.5 } };
    std::vector<size_t> expected_clusters_length = { 6 };
    index_sequence range = { 0, 1, 2, 5, 6, 7 };
    template_kmeans_length_process_data_range(simple_sample_factory::create_sample(SAMPLE_SIMPLE::SAMPLE_SIMPLE_01), start_centers, expected_clusters_length, range);
}

TEST(utest_kmeans, allocation_sample_simpl_01_euclidean) {
    dataset start_centers = { { 3.7, 5.5 },{ 6.7, 7.5 } };
    std::vector<size_t> expected_clusters_length = { 5, 5 };
    auto metric = distance_metric_factory<point>::euclidean();
    template_kmeans_metric(simple_sample_factory::create_sample(SAMPLE_SIMPLE::SAMPLE_SIMPLE_01), start_centers, expected_clusters_length, metric);
}

TEST(utest_kmeans, allocation_sample_simpl_01_euclidean_square) {
    dataset start_centers = { { 3.7, 5.5 },{ 6.7, 7.5 } };
    std::vector<size_t> expected_clusters_length = { 5, 5 };
    auto metric = distance_metric_factory<point>::euclidean_square();
    template_kmeans_metric(simple_sample_factory::create_sample(SAMPLE_SIMPLE::SAMPLE_SIMPLE_01), start_centers, expected_clusters_length, metric);
}

TEST(utest_kmeans, allocation_sample_simpl_01_manhattan) {
    dataset start_centers = { { 3.7, 5.5 },{ 6.7, 7.5 } };
    std::vector<size_t> expected_clusters_length = { 5, 5 };
    auto metric = distance_metric_factory<point>::manhattan();
    template_kmeans_metric(simple_sample_factory::create_sample(SAMPLE_SIMPLE::SAMPLE_SIMPLE_01), start_centers, expected_clusters_length, metric);
}

TEST(utest_kmeans, allocation_sample_simpl_01_chebyshev) {
    dataset start_centers = { { 3.7, 5.5 },{ 6.7, 7.5 } };
    std::vector<size_t> expected_clusters_length = { 5, 5 };
    auto metric = distance_metric_factory<point>::chebyshev();
    template_kmeans_metric(simple_sample_factory::create_sample(SAMPLE_SIMPLE::SAMPLE_SIMPLE_01), start_centers, expected_clusters_length, metric);
}

TEST(utest_kmeans, allocation_sample_simpl_01_minkowski) {
    dataset start_centers = { { 3.7, 5.5 },{ 6.7, 7.5 } };
    std::vector<size_t> expected_clusters_length = { 5, 5 };
    auto metric = distance_metric_factory<point>::minkowski(2.0);
    template_kmeans_metric(simple_sample_factory::create_sample(SAMPLE_SIMPLE::SAMPLE_SIMPLE_01), start_centers, expected_clusters_length, metric);
}

TEST(utest_kmeans, allocation_sample_simpl_01_user_defined) {
    dataset start_centers = { { 3.7, 5.5 },{ 6.7, 7.5 } };
    std::vector<size_t> expected_clusters_length = { 5, 5 };

    auto user_metric = [](const point & p1, const point & p2) { return euclidean_distance(p1, p2); };
    auto metric = distance_metric_factory<point>::user_defined(user_metric);

    template_kmeans_metric(simple_sample_factory::create_sample(SAMPLE_SIMPLE::SAMPLE_SIMPLE_01), start_centers, expected_clusters_length, metric);
}

TEST(utest_kmeans, allocation_sample_simple_02) {
    dataset start_centers = { { 3.5, 4.8 },{ 6.9, 7.0 },{ 7.5, 0.5 } };
    std::vector<size_t> expected_clusters_length = { 10, 5, 8 };
    template_kmeans_length_process_data(simple_sample_factory::create_sample(SAMPLE_SIMPLE::SAMPLE_SIMPLE_02), start_centers, expected_clusters_length);
}

TEST(utest_kmeans, allocation_sample_simple_02_range) {
    dataset start_centers = { { 3.5, 4.8 },{ 6.9, 7.0 },{ 7.5, 0.5 } };
    std::vector<size_t> expected_clusters_length = { 5, 3, 4 };
    index_sequence range = { 0, 1, 2, 3, 4, 10, 11, 12, 15, 16, 17, 18 };
    template_kmeans_length_process_data_range(simple_sample_factory::create_sample(SAMPLE_SIMPLE::SAMPLE_SIMPLE_02), start_centers, expected_clusters_length,range);
}

TEST(utest_kmeans, one_cluster_allocation_sample_simple_02) {
    dataset start_centers = { { 0.5, 0.2 } };
    std::vector<size_t> expected_clusters_length = { 23 };
    template_kmeans_length_process_data(simple_sample_factory::create_sample(SAMPLE_SIMPLE::SAMPLE_SIMPLE_02), start_centers, expected_clusters_length);
}

TEST(utest_kmeans, allocation_sample_simple_03) {
    dataset start_centers = { { 0.2, 0.1 },{ 4.0, 1.0 },{ 2.0, 2.0 },{ 2.3, 3.9 } };
    std::vector<size_t> expected_clusters_length = { 10, 10, 10, 30 };
    template_kmeans_length_process_data(simple_sample_factory::create_sample(SAMPLE_SIMPLE::SAMPLE_SIMPLE_03), start_centers, expected_clusters_length);
}

TEST(utest_kmeans, large_number_centers_sample_simple_01) {
    dataset start_centers = { { 1.7, 2.6 },{ 3.7, 4.5 },{ 4.5, 1.6 },{ 6.4, 5.0 },{ 2.2, 2.2 } };
    std::vector<size_t> expected_clusters_length;   /* pass empty */
    template_kmeans_length_process_data(simple_sample_factory::create_sample(SAMPLE_SIMPLE::SAMPLE_SIMPLE_01), start_centers, expected_clusters_length);
}

TEST(utest_kmeans, large_number_centers_sample_simple_02) {
    dataset start_centers = { { -1.5, 0.8 },{ -4.9, 5.0 },{ 2.3, 3.2 },{ -1.2, -0.8 },{ 2.5, 2.9 },{ 6.8, 7.9 } };
    std::vector<size_t> expected_clusters_length;   /* pass empty */
    template_kmeans_length_process_data(simple_sample_factory::create_sample(SAMPLE_SIMPLE::SAMPLE_SIMPLE_02), start_centers, expected_clusters_length);
}


TEST(utest_kmeans, large_number_centers_sample_simple_03) {
    dataset start_centers = { { -8.1, 2.3 },{ -4.9, 5.5 },{ 1.3, 8.3 },{ -2.6, -1.7 },{ 5.3, 4.2 },{ 2.1, 0.0 },{ 1.7, 0.4 } };
    std::vector<size_t> expected_clusters_length;   /* pass empty */
    template_kmeans_length_process_data(simple_sample_factory::create_sample(SAMPLE_SIMPLE::SAMPLE_SIMPLE_03), start_centers, expected_clusters_length);
}


TEST(utest_kmeans, one_dimension_sample_simple_07) {
    dataset start_centers = { { -2.0 },{ 4.0 } };
    std::vector<size_t> expected_clusters_length = { 10, 10 };
    template_kmeans_length_process_data(simple_sample_factory::create_sample(SAMPLE_SIMPLE::SAMPLE_SIMPLE_07), start_centers, expected_clusters_length);
}


TEST(utest_kmeans, one_dimension_sample_simple_08) {
    dataset start_centers = { { -4.0 },{ 3.0 },{ 6.0 },{ 10.0 } };
    std::vector<size_t> expected_clusters_length = { 15, 30, 20, 80 };
    template_kmeans_length_process_data(simple_sample_factory::create_sample(SAMPLE_SIMPLE::SAMPLE_SIMPLE_08), start_centers, expected_clusters_length);
}


TEST(utest_kmeans, parallel_processing) {
    dataset start_centers = { {0.25, 0.25}, {0.75, 0.65}, {0.95, 0.5} };
    std::size_t parallel_processing_trigger = 100;

    std::shared_ptr<dataset> trigger_parallel_data = simple_sample_factory::create_random_sample(parallel_processing_trigger, 5);

    template_kmeans_length_process_data(trigger_parallel_data, start_centers, { }, parallel_processing_trigger);
}


TEST(utest_kmeans, parallel_processing_sample_simple_01) {
    dataset start_centers = { { 3.7, 5.5 },{ 6.7, 7.5 } };
    std::vector<size_t> expected_clusters_length = { 5, 5 };
    template_kmeans_length_process_data(simple_sample_factory::create_sample(SAMPLE_SIMPLE::SAMPLE_SIMPLE_01), start_centers, expected_clusters_length, 0);
}


TEST(utest_kmeans, parallel_processing_sample_simple_02) {
    dataset start_centers = { { 3.5, 4.8 },{ 6.9, 7.0 },{ 7.5, 0.5 } };
    std::vector<size_t> expected_clusters_length = { 10, 5, 8 };
    template_kmeans_length_process_data(simple_sample_factory::create_sample(SAMPLE_SIMPLE::SAMPLE_SIMPLE_02), start_centers, expected_clusters_length, 0);
}


TEST(utest_kmeans, collect_evolution_sample_simple_01) {
    dataset start_centers = { { 3.7, 5.5 },{ 6.7, 7.5 } };
    std::vector<size_t> expected_clusters_length = { 5, 5 };
    template_kmeans_observer(simple_sample_factory::create_sample(SAMPLE_SIMPLE::SAMPLE_SIMPLE_01), start_centers, { }, expected_clusters_length);
}


TEST(utest_kmeans, collect_evolution_sample_simple_01_one_cluster) {
    dataset start_centers = { { 1.0, 2.5 } };
    std::vector<size_t> expected_clusters_length = { 10 };
    template_kmeans_observer(simple_sample_factory::create_sample(SAMPLE_SIMPLE::SAMPLE_SIMPLE_01), start_centers, { }, expected_clusters_length);
}


TEST(utest_kmeans, collect_evolution_sample_simple_01_range) {
    dataset start_centers = { { 3.7, 5.5 },{ 6.7, 7.5 } };
    std::vector<size_t> expected_clusters_length = { 3, 3 };
    index_sequence range = { 0, 1, 2, 5, 6, 7 };
    template_kmeans_observer(simple_sample_factory::create_sample(SAMPLE_SIMPLE::SAMPLE_SIMPLE_01), start_centers, range, expected_clusters_length);
}


TEST(utest_kmeans, collect_evolution_sample_simple_02) {
    dataset start_centers = { { 3.5, 4.8 },{ 6.9, 7.0 },{ 7.5, 0.5 } };
    std::vector<size_t> expected_clusters_length = { 10, 5, 8 };
    template_kmeans_observer(simple_sample_factory::create_sample(SAMPLE_SIMPLE::SAMPLE_SIMPLE_02), start_centers, { }, expected_clusters_length);
}