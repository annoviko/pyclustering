#ifndef _UTEST_KMEDIANS_
#define _UTEST_KMEDIANS_

#include "ccore/kmedians.h"

#include "gtest/gtest.h"
#include "samples.h"

#include <algorithm>

extern dataset SIMPLE_SAMPLE_01;
extern dataset SIMPLE_SAMPLE_02;
extern dataset SIMPLE_SAMPLE_03;

static void
template_length_process_data(const dataset & data,
const std::vector<point> & start_medians,
const std::vector<unsigned int> & expected_cluster_length) 
{
    kmedians solver(start_medians, 0.0001);
    solver.process(data);

    std::vector<std::vector<unsigned int> > results;
    solver.get_clusters(results);

    /* Check number of clusters */
    if (!expected_cluster_length.empty()) {
        ASSERT_EQ(expected_cluster_length.size(), results.size());
    }

    /* Check cluster sizes */
    std::vector<size_t> obtained_cluster_length;
    std::vector<bool> unique_objects(data.size(), false);
    size_t total_size = 0;
    for (size_t i = 0; i < results.size(); i++) {
        size_t cluster_length = results[i].size();

        obtained_cluster_length.push_back(cluster_length);
        total_size += cluster_length;
        
        for (size_t j = 0; j < cluster_length; j++) {
            size_t index_object = results[i][j];

            ASSERT_EQ(false, unique_objects[index_object]);

            unique_objects[index_object] = true;
        }
    }

    ASSERT_EQ(data.size(), total_size);

    if (!expected_cluster_length.empty()) {
        std::sort(obtained_cluster_length.begin(), obtained_cluster_length.end());

        std::vector<unsigned int> sorted_expected_cluster_length(expected_cluster_length);
        std::sort(sorted_expected_cluster_length.begin(), sorted_expected_cluster_length.end());

        for (size_t i = 0; i < obtained_cluster_length.size(); i++) {
            ASSERT_EQ(obtained_cluster_length[i], sorted_expected_cluster_length[i]);
        }
    }
}


TEST(utest_kmedians, allocation_sample_simple_01) {
    std::vector<std::vector<double> > start_medians = { { 3.7, 5.5 }, { 6.7, 7.5 } };
    std::vector<unsigned int> expected_clusters_length = { 5, 5 };
    template_length_process_data(SIMPLE_SAMPLE_01, start_medians, expected_clusters_length);
}

TEST(utest_kmedians, allocation_sample_simple_02) {
    std::vector<std::vector<double> > start_medians = { { 3.5, 4.8 }, { 6.9, 7.0 }, { 7.5, 0.5 } };
    std::vector<unsigned int> expected_clusters_length = { 10, 5, 8 };
    template_length_process_data(SIMPLE_SAMPLE_02, start_medians, expected_clusters_length);
}

TEST(utest_kmedians, allocation_sample_simple_03) {
    std::vector<std::vector<double> > start_medians = { { 0.2, 0.1 }, { 4.0, 1.0 }, { 2.0, 2.0 }, { 2.3, 3.9 } };
    std::vector<unsigned int> expected_clusters_length = { 10, 10, 10, 30 };
    template_length_process_data(SIMPLE_SAMPLE_03, start_medians, expected_clusters_length);
}

TEST(utest_kmedians, large_number_medoids_sample_simple_01) {
    std::vector<std::vector<double> > start_medians = { { 1.7, 2.6 }, { 3.7, 4.5 }, { 4.5, 1.6 }, { 6.4, 5.0 }, { 2.2, 2.2 } };
    std::vector<unsigned int> expected_clusters_length;   /* pass empty */
    template_length_process_data(SIMPLE_SAMPLE_01, start_medians, expected_clusters_length);
}

TEST(utest_kmedians, large_number_medoids_sample_simple_02) {
    std::vector<std::vector<double> > start_medians = { { -1.5, 0.8 }, { -4.9, 5.0 }, { 2.3, 3.2 }, { -1.2, -0.8 }, { 2.5, 2.9 }, { 6.8, 7.9 } };
    std::vector<unsigned int> expected_clusters_length;   /* pass empty */
    template_length_process_data(SIMPLE_SAMPLE_02, start_medians, expected_clusters_length);
}


TEST(utest_kmedians, large_number_medoids_sample_simple_03) {
    std::vector<std::vector<double> > start_medians = { { -8.1, 2.3 }, { -4.9, 5.5 }, { 1.3, 8.3 }, { -2.6, -1.7 }, { 5.3, 4.2 }, { 2.1, 0.0 }, { 1.7, 0.4 } };
    std::vector<unsigned int> expected_clusters_length;   /* pass empty */
    template_length_process_data(SIMPLE_SAMPLE_03, start_medians, expected_clusters_length);
}

#endif