/*!

@authors Andrei Novikov (pyclustering@yandex.ru)
@date 2014-2020
@copyright BSD-3-Clause

*/


#include <gtest/gtest.h>

#include "samples.hpp"

#include <pyclustering/cluster/somsc.hpp>
#include "utenv_check.hpp"


using namespace pyclustering::clst;


static void
template_kmeans_length_process_data(const dataset_ptr & p_data,
    const std::size_t p_amout_clusters,
    const std::vector<size_t> & p_expected_cluster_length)
{
    somsc_data output_result;
    somsc solver(p_amout_clusters);
    solver.process(*p_data, output_result);

    const dataset & data = *p_data;
    const cluster_sequence & actual_clusters = output_result.clusters();
    ASSERT_CLUSTER_SIZES(data, actual_clusters, p_expected_cluster_length);
}


TEST(utest_somsc, allocation_sample_simple_01) {
    std::vector<size_t> expected_clusters_length = { 5, 5 };
    template_kmeans_length_process_data(simple_sample_factory::create_sample(SAMPLE_SIMPLE::SAMPLE_SIMPLE_01), 2, expected_clusters_length);
}

TEST(utest_somsc, one_cluster_allocation_sample_simple_01) {
    std::vector<size_t> expected_clusters_length = { 10 };
    template_kmeans_length_process_data(simple_sample_factory::create_sample(SAMPLE_SIMPLE::SAMPLE_SIMPLE_01), 1, expected_clusters_length);
}

TEST(utest_somsc, allocation_sample_simple_02) {
    std::vector<size_t> expected_clusters_length = { 10, 5, 8 };
    template_kmeans_length_process_data(simple_sample_factory::create_sample(SAMPLE_SIMPLE::SAMPLE_SIMPLE_02), 3, expected_clusters_length);
}

TEST(utest_somsc, one_cluster_allocation_sample_simple_02) {
    std::vector<size_t> expected_clusters_length = { 23 };
    template_kmeans_length_process_data(simple_sample_factory::create_sample(SAMPLE_SIMPLE::SAMPLE_SIMPLE_02), 1, expected_clusters_length);
}

TEST(utest_somsc, allocation_sample_simple_03) {
    std::vector<size_t> expected_clusters_length = { 10, 10, 10, 30 };
    template_kmeans_length_process_data(simple_sample_factory::create_sample(SAMPLE_SIMPLE::SAMPLE_SIMPLE_03), 4, expected_clusters_length);
}

TEST(utest_somsc, large_number_centers_sample_simple_01) {
    std::vector<size_t> expected_clusters_length;   /* pass empty */
    template_kmeans_length_process_data(simple_sample_factory::create_sample(SAMPLE_SIMPLE::SAMPLE_SIMPLE_01), 5, expected_clusters_length);
}

TEST(utest_somsc, large_number_centers_sample_simple_02) {
    std::vector<size_t> expected_clusters_length;   /* pass empty */
    template_kmeans_length_process_data(simple_sample_factory::create_sample(SAMPLE_SIMPLE::SAMPLE_SIMPLE_02), 6, expected_clusters_length);
}


TEST(utest_somsc, large_number_centers_sample_simple_03) {
    std::vector<size_t> expected_clusters_length;   /* pass empty */
    template_kmeans_length_process_data(simple_sample_factory::create_sample(SAMPLE_SIMPLE::SAMPLE_SIMPLE_03), 7, expected_clusters_length);
}


TEST(utest_somsc, one_dimension_sample_simple_07) {
    std::vector<size_t> expected_clusters_length = { 10, 10 };
    template_kmeans_length_process_data(simple_sample_factory::create_sample(SAMPLE_SIMPLE::SAMPLE_SIMPLE_07), 2, expected_clusters_length);
}


TEST(utest_somsc, one_dimension_sample_simple_08) {
    std::vector<size_t> expected_clusters_length;
    template_kmeans_length_process_data(simple_sample_factory::create_sample(SAMPLE_SIMPLE::SAMPLE_SIMPLE_08), 4, expected_clusters_length);
}
