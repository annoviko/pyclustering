#ifndef _UTEST_AGGLOMERATIVE_
#define _UTEST_AGGLOMERATIVE_

#include "ccore/agglomerative.h"
#include "samples.h"

#include "gtest/gtest.h"

#include <algorithm>

extern dataset SIMPLE_SAMPLE_01;
extern dataset SIMPLE_SAMPLE_02;
extern dataset SIMPLE_SAMPLE_03;

static void
template_length_process_data(const dataset & data,
                             const unsigned int number_clusters,
                             const type_link link,
                             const std::vector<unsigned int> & expected_cluster_length) {
    agglomerative solver(number_clusters, link);
    solver.process(data);

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

TEST(utest_agglomerative, clustering_sampl_simple_01_two_cluster_link_average) {
    std::vector<unsigned int> expected_clusters_length_1 = {5, 5};
    template_length_process_data(SIMPLE_SAMPLE_01, 2, type_link::AVERAGE_LINK, expected_clusters_length_1);
}

TEST(utest_agglomerative, clustering_sampl_simple_01_one_cluster_link_average) {
    std::vector<unsigned int> expected_clusters_length_2 = {10};
    template_length_process_data(SIMPLE_SAMPLE_01, 1, type_link::AVERAGE_LINK, expected_clusters_length_2);
}

TEST(utest_agglomerative, clustering_sampl_simple_01_two_cluster_link_centroid) {
    std::vector<unsigned int> expected_clusters_length_1 = {5, 5};
    template_length_process_data(SIMPLE_SAMPLE_01, 2, type_link::CENTROID_LINK, expected_clusters_length_1);
}

TEST(utest_agglomerative, clustering_sampl_simple_01_one_cluster_link_centroid) {
    std::vector<unsigned int> expected_clusters_length_2 = {10};
    template_length_process_data(SIMPLE_SAMPLE_01, 1, type_link::CENTROID_LINK, expected_clusters_length_2);
}

TEST(utest_agglomerative, clustering_sampl_simple_01_two_cluster_link_complete) {
    std::vector<unsigned int> expected_clusters_length_1 = {5, 5};
    template_length_process_data(SIMPLE_SAMPLE_01, 2, type_link::COMPLETE_LINK, expected_clusters_length_1);
}

TEST(utest_agglomerative, clustering_sampl_simple_01_one_cluster_link_complete) {
    std::vector<unsigned int> expected_clusters_length_2 = {10};
    template_length_process_data(SIMPLE_SAMPLE_01, 1, type_link::COMPLETE_LINK, expected_clusters_length_2);
}

TEST(utest_agglomerative, clustering_sampl_simple_01_two_cluster_link_single) {
    std::vector<unsigned int> expected_clusters_length_1 = {5, 5};
    template_length_process_data(SIMPLE_SAMPLE_01, 2, type_link::SINGLE_LINK, expected_clusters_length_1);
}

TEST(utest_agglomerative, clustering_sampl_simple_01_one_cluster_link_single) {
    std::vector<unsigned int> expected_clusters_length_2 = {10};
    template_length_process_data(SIMPLE_SAMPLE_01, 1, type_link::SINGLE_LINK, expected_clusters_length_2);
}

TEST(utest_agglomerative, clustering_sampl_simple_02_three_cluster_link_average) {
    std::vector<unsigned int> expected_clusters_length_1 = {5, 8, 10};
    template_length_process_data(SIMPLE_SAMPLE_02, 3, type_link::AVERAGE_LINK, expected_clusters_length_1);
}

TEST(utest_agglomerative, clustering_sampl_simple_02_one_cluster_link_average) {
    std::vector<unsigned int> expected_clusters_length_2 = {23};
    template_length_process_data(SIMPLE_SAMPLE_02, 1, type_link::AVERAGE_LINK, expected_clusters_length_2);
}

TEST(utest_agglomerative, clustering_sampl_simple_02_three_cluster_link_centroid) {
    std::vector<unsigned int> expected_clusters_length_1 = {5, 8, 10};
    template_length_process_data(SIMPLE_SAMPLE_02, 3, type_link::CENTROID_LINK, expected_clusters_length_1);
}

TEST(utest_agglomerative, clustering_sampl_simple_02_one_cluster_link_centroid) {
    std::vector<unsigned int> expected_clusters_length_2 = {23};
    template_length_process_data(SIMPLE_SAMPLE_02, 1, type_link::CENTROID_LINK, expected_clusters_length_2);
}

TEST(utest_agglomerative, clustering_sampl_simple_02_three_cluster_link_complete) {
    std::vector<unsigned int> expected_clusters_length_1 = {5, 8, 10};
    template_length_process_data(SIMPLE_SAMPLE_02, 3, type_link::COMPLETE_LINK, expected_clusters_length_1);
}

TEST(utest_agglomerative, clustering_sampl_simple_02_one_cluster_link_complete) {
    std::vector<unsigned int> expected_clusters_length_2 = {23};
    template_length_process_data(SIMPLE_SAMPLE_02, 1, type_link::COMPLETE_LINK, expected_clusters_length_2);
}

TEST(utest_agglomerative, clustering_sampl_simple_02_three_cluster_link_single) {
    std::vector<unsigned int> expected_clusters_length_1 = {5, 8, 10};
    template_length_process_data(SIMPLE_SAMPLE_02, 3, type_link::SINGLE_LINK, expected_clusters_length_1);
}

TEST(utest_agglomerative, clustering_sampl_simple_02_one_cluster_link_single) {
    std::vector<unsigned int> expected_clusters_length_2 = {23};
    template_length_process_data(SIMPLE_SAMPLE_02, 1, type_link::SINGLE_LINK, expected_clusters_length_2);
}

TEST(utest_agglomerative, clustering_sampl_simple_03_four_cluster_link_average) {
    std::vector<unsigned int> expected_clusters_length_1 = {10, 10, 10, 30};
    template_length_process_data(SIMPLE_SAMPLE_03, 4, type_link::AVERAGE_LINK, expected_clusters_length_1);
}

TEST(utest_agglomerative, clustering_sampl_simple_03_one_cluster_link_average) {
    std::vector<unsigned int> expected_clusters_length_2 = {60};
    template_length_process_data(SIMPLE_SAMPLE_03, 1, type_link::AVERAGE_LINK, expected_clusters_length_2);
}

TEST(utest_agglomerative, clustering_sampl_simple_03_four_cluster_link_centroid) {
    std::vector<unsigned int> expected_clusters_length_1 = {10, 10, 10, 30};
    template_length_process_data(SIMPLE_SAMPLE_03, 4, type_link::CENTROID_LINK, expected_clusters_length_1);
}

TEST(utest_agglomerative, clustering_sampl_simple_03_one_cluster_link_centroid) {
    std::vector<unsigned int> expected_clusters_length_2 = {60};
    template_length_process_data(SIMPLE_SAMPLE_03, 1, type_link::CENTROID_LINK, expected_clusters_length_2);
}

TEST(utest_agglomerative, clustering_sampl_simple_03_four_cluster_link_complete) {
    std::vector<unsigned int> expected_clusters_length_1 = {10, 10, 10, 30};
    template_length_process_data(SIMPLE_SAMPLE_03, 4, type_link::COMPLETE_LINK, expected_clusters_length_1);
}

TEST(utest_agglomerative, clustering_sampl_simple_03_one_cluster_link_complete) {
    std::vector<unsigned int> expected_clusters_length_2 = {60};
    template_length_process_data(SIMPLE_SAMPLE_03, 1, type_link::COMPLETE_LINK, expected_clusters_length_2);
}

TEST(utest_agglomerative, clustering_sampl_simple_03_four_cluster_link_single) {
    std::vector<unsigned int> expected_clusters_length_1 = {10, 10, 10, 30};
    template_length_process_data(SIMPLE_SAMPLE_03, 4, type_link::SINGLE_LINK, expected_clusters_length_1);
}

TEST(utest_agglomerative, clustering_sampl_simple_03_one_cluster_link_single) {
    std::vector<unsigned int> expected_clusters_length_2 = {60};
    template_length_process_data(SIMPLE_SAMPLE_03, 1, type_link::SINGLE_LINK, expected_clusters_length_2);
}

#endif
