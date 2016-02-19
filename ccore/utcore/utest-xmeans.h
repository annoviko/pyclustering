#ifndef _UTEST_XMEANS_
#define _UTEST_XMEANS_

#include "samples.h"
#include "ccore/xmeans.h"

#include "gtest/gtest.h"

#include <algorithm>

static void
template_length_process_data(const std::shared_ptr<dataset_t> & data,
                             const std::vector<std::vector<double> > & start_centers,
                             const unsigned int kmax,
                             const std::vector<unsigned int> & expected_cluster_length) {
    xmeans solver(*data.get(), start_centers, kmax, 0.0001);
    solver.process();

    std::vector<std::vector<unsigned int> > results;
    solver.get_clusters(results);

    /* Check number of clusters */
    ASSERT_EQ(expected_cluster_length.size(), results.size());

    /* Check cluster sizes */
    std::vector<size_t> obtained_cluster_length;
    for (size_t i = 0; i < results.size(); i++) {
        obtained_cluster_length.push_back(results[i].size());
    }

    std::sort(obtained_cluster_length.begin(), obtained_cluster_length.end());

    std::vector<unsigned int> sorted_expected_cluster_length(expected_cluster_length);
    std::sort(sorted_expected_cluster_length.begin(), sorted_expected_cluster_length.end());

    for (size_t i = 0; i < obtained_cluster_length.size(); i++) {
        ASSERT_EQ(obtained_cluster_length[i], sorted_expected_cluster_length[i]);
    }
}


TEST(utest_xmeans, allocation_sample_simple_01) {
    std::vector<std::vector<double> > start_centers = { {3.7, 5.5}, {6.7, 7.5} };
    std::vector<unsigned int> expected_clusters_length = {5, 5};
    template_length_process_data(simple_sample_factory::create_sample(SAMPLE_SIMPLE::SAMPLE_SIMPLE_01), start_centers, 20, expected_clusters_length);
}

TEST(utest_xmeans, allocation_sample_simple_02) {
    std::vector<std::vector<double> > start_centers = { {3.5, 4.8}, {6.9, 7.0}, {7.5, 0.5} };
    std::vector<unsigned int> expected_clusters_length = {10, 5, 8};
    template_length_process_data(simple_sample_factory::create_sample(SAMPLE_SIMPLE::SAMPLE_SIMPLE_02), start_centers, 20, expected_clusters_length);
}

TEST(utest_xmeans, allocation_sample_simple_03) {
    std::vector<std::vector<double> > start_centers = { {0.2, 0.1}, {4.0, 1.0}, {2.0, 2.0}, {2.3, 3.9} };
    std::vector<unsigned int> expected_clusters_length = {10, 10, 10, 30};
    template_length_process_data(simple_sample_factory::create_sample(SAMPLE_SIMPLE::SAMPLE_SIMPLE_03), start_centers, 20, expected_clusters_length);
}

#endif
