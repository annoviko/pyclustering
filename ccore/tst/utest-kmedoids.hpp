#ifndef TST_UTEST_KMEDOIDS_HPP_
#define TST_UTEST_KMEDOIDS_HPP_


#include "gtest/gtest.h"

#include "cluster/kmedoids.hpp"

#include "samples.hpp"
#include "utest-cluster.hpp"


using namespace cluster_analysis;


static void
template_length_process_data(const std::shared_ptr<dataset> & p_data,
        const medoid_sequence & p_start_medians,
        const std::vector<size_t> & p_expected_cluster_length) {

    kmedoids_data output_result;
    kmedoids solver(p_start_medians, 0.0001);
    solver.process(*p_data, output_result);

    const dataset & data = *p_data;
    const cluster_sequence & actual_clusters = *(output_result.clusters());
    ASSERT_CLUSTER_SIZES(data, actual_clusters, p_expected_cluster_length);
}


TEST(utest_kmedoids, allocation_sample_simple_01) {
    const medoid_sequence start_medoids = { 1, 5 };
    const std::vector<size_t> expected_clusters_length = { 5, 5 };
    template_length_process_data(simple_sample_factory::create_sample(SAMPLE_SIMPLE::SAMPLE_SIMPLE_01), start_medoids, expected_clusters_length);
}


TEST(utest_kmedoids, allocation_sample_one_allocation_simple_01) {
    const medoid_sequence start_medoids = { 1 };
    const std::vector<size_t> expected_clusters_length = { 10 };
    template_length_process_data(simple_sample_factory::create_sample(SAMPLE_SIMPLE::SAMPLE_SIMPLE_01), start_medoids, expected_clusters_length);
}


TEST(utest_kmedoids, allocation_sample_simple_02) {
    const medoid_sequence start_medoids = { 3, 12, 20 };
    const std::vector<size_t> expected_clusters_length = { 10, 5, 8 };
    template_length_process_data(simple_sample_factory::create_sample(SAMPLE_SIMPLE::SAMPLE_SIMPLE_02), start_medoids, expected_clusters_length);
}


TEST(utest_kmedoids, allocation_one_allocation_sample_simple_02) {
    const medoid_sequence start_medoids = { 10 };
    const std::vector<size_t> expected_clusters_length = { 23 };
    template_length_process_data(simple_sample_factory::create_sample(SAMPLE_SIMPLE::SAMPLE_SIMPLE_02), start_medoids, expected_clusters_length);
}


TEST(utest_kmedoids, allocation_sample_simple_03) {
    const medoid_sequence start_medoids = { 4, 12, 25, 37 };
    const std::vector<size_t> expected_clusters_length = { 10, 10, 10, 30 };
    template_length_process_data(simple_sample_factory::create_sample(SAMPLE_SIMPLE::SAMPLE_SIMPLE_03), start_medoids, expected_clusters_length);
}


TEST(utest_kmedoids, allocation_sample_simple_04) {
    const medoid_sequence start_medoids = { 7, 22, 37, 52, 67 };
    const std::vector<size_t> expected_clusters_length = { 15, 15, 15, 15, 15 };
    template_length_process_data(simple_sample_factory::create_sample(SAMPLE_SIMPLE::SAMPLE_SIMPLE_04), start_medoids, expected_clusters_length);
}


TEST(utest_kmedoids, allocation_sample_simple_05) {
    const medoid_sequence start_medoids = { 7, 22, 37, 52 };
    const std::vector<size_t> expected_clusters_length = { 15, 15, 15, 15 };
    template_length_process_data(simple_sample_factory::create_sample(SAMPLE_SIMPLE::SAMPLE_SIMPLE_05), start_medoids, expected_clusters_length);
}


TEST(utest_kmedoids, allocation_sample_simple_07) {
    const medoid_sequence start_medoids = { 5, 15 };
    const std::vector<size_t> expected_clusters_length = { 10, 10 };
    template_length_process_data(simple_sample_factory::create_sample(SAMPLE_SIMPLE::SAMPLE_SIMPLE_07), start_medoids, expected_clusters_length);
}


TEST(utest_kmedoids, allocation_sample_simple_08) {
    const medoid_sequence start_medoids = { 5, 35, 50, 100 };
    const std::vector<size_t> expected_clusters_length = { 15, 30, 20, 80 };
    template_length_process_data(simple_sample_factory::create_sample(SAMPLE_SIMPLE::SAMPLE_SIMPLE_08), start_medoids, expected_clusters_length);
}


TEST(utest_kmedoids, allocation_wrong_initial_medoids_sample_simple_03) {
    const medoid_sequence start_medoids = { 4, 7, 12, 20, 25, 30, 37 };
    const std::vector<size_t> expected_clusters_length;     /* empty - just check index point existence */
    template_length_process_data(simple_sample_factory::create_sample(SAMPLE_SIMPLE::SAMPLE_SIMPLE_03), start_medoids, expected_clusters_length);
}


TEST(utest_kmedoids, allocation_wrong_initial_medoids_sample_simple_04) {
    const medoid_sequence start_medoids = { 2, 7, 15, 22, 30, 37, 40, 52, 62, 67 };
    const std::vector<size_t> expected_clusters_length;     /* empty - just check index point existence */
    template_length_process_data(simple_sample_factory::create_sample(SAMPLE_SIMPLE::SAMPLE_SIMPLE_04), start_medoids, expected_clusters_length);
}


#endif
