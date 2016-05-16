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

#ifndef _UTEST_AGGLOMERATIVE_
#define _UTEST_AGGLOMERATIVE_


#include "gtest/gtest.h"

#include "cluster/agglomerative.hpp"
#include "samples.hpp"

#include <algorithm>


using namespace container;


static void
template_length_process_data(const std::shared_ptr<dataset> & data,
                             const size_t number_clusters,
                             const cluster_analysis::type_link link,
                             const std::vector<size_t> & expected_cluster_length) {

    cluster_analysis::agglomerative solver(number_clusters, link);

    cluster_analysis::cluster_data results_data;
    solver.process(*data.get(), results_data);

    cluster_analysis::cluster_sequence & results = *results_data.clusters();

    /* Check number of clusters */
    ASSERT_EQ(expected_cluster_length.size(), results.size());

    /* Check cluster sizes */
    std::vector<size_t> obtained_cluster_length;
    for (size_t i = 0; i < results.size(); i++) {
        obtained_cluster_length.push_back(results[i].size());
    }

    std::sort(obtained_cluster_length.begin(), obtained_cluster_length.end());

    std::vector<size_t> sorted_expected_cluster_length(expected_cluster_length);
    std::sort(sorted_expected_cluster_length.begin(), sorted_expected_cluster_length.end());

    for (size_t i = 0; i < obtained_cluster_length.size(); i++) {
        ASSERT_EQ(obtained_cluster_length[i], sorted_expected_cluster_length[i]);
    }
}

TEST(utest_agglomerative, clustering_sampl_simple_01_two_cluster_link_average) {
    std::vector<size_t> expected_clusters_length_1 = {5, 5};
    template_length_process_data(simple_sample_factory::create_sample(SAMPLE_SIMPLE::SAMPLE_SIMPLE_01), 2, cluster_analysis::type_link::AVERAGE_LINK, expected_clusters_length_1);
}

TEST(utest_agglomerative, clustering_sampl_simple_01_one_cluster_link_average) {
    std::vector<size_t> expected_clusters_length_2 = {10};
    template_length_process_data(simple_sample_factory::create_sample(SAMPLE_SIMPLE::SAMPLE_SIMPLE_01), 1, cluster_analysis::type_link::AVERAGE_LINK, expected_clusters_length_2);
}

TEST(utest_agglomerative, clustering_sampl_simple_01_two_cluster_link_centroid) {
    std::vector<size_t> expected_clusters_length_1 = {5, 5};
    template_length_process_data(simple_sample_factory::create_sample(SAMPLE_SIMPLE::SAMPLE_SIMPLE_01), 2, cluster_analysis::type_link::CENTROID_LINK, expected_clusters_length_1);
}

TEST(utest_agglomerative, clustering_sampl_simple_01_one_cluster_link_centroid) {
    std::vector<size_t> expected_clusters_length_2 = {10};
    template_length_process_data(simple_sample_factory::create_sample(SAMPLE_SIMPLE::SAMPLE_SIMPLE_01), 1, cluster_analysis::type_link::CENTROID_LINK, expected_clusters_length_2);
}

TEST(utest_agglomerative, clustering_sampl_simple_01_two_cluster_link_complete) {
    std::vector<size_t> expected_clusters_length_1 = {5, 5};
    template_length_process_data(simple_sample_factory::create_sample(SAMPLE_SIMPLE::SAMPLE_SIMPLE_01), 2, cluster_analysis::type_link::COMPLETE_LINK, expected_clusters_length_1);
}

TEST(utest_agglomerative, clustering_sampl_simple_01_one_cluster_link_complete) {
    std::vector<size_t> expected_clusters_length_2 = {10};
    template_length_process_data(simple_sample_factory::create_sample(SAMPLE_SIMPLE::SAMPLE_SIMPLE_01), 1, cluster_analysis::type_link::COMPLETE_LINK, expected_clusters_length_2);
}

TEST(utest_agglomerative, clustering_sampl_simple_01_two_cluster_link_single) {
    std::vector<size_t> expected_clusters_length_1 = {5, 5};
    template_length_process_data(simple_sample_factory::create_sample(SAMPLE_SIMPLE::SAMPLE_SIMPLE_01), 2, cluster_analysis::type_link::SINGLE_LINK, expected_clusters_length_1);
}

TEST(utest_agglomerative, clustering_sampl_simple_01_one_cluster_link_single) {
    std::vector<size_t> expected_clusters_length_2 = {10};
    template_length_process_data(simple_sample_factory::create_sample(SAMPLE_SIMPLE::SAMPLE_SIMPLE_01), 1, cluster_analysis::type_link::SINGLE_LINK, expected_clusters_length_2);
}

TEST(utest_agglomerative, clustering_sampl_simple_02_three_cluster_link_average) {
    std::vector<size_t> expected_clusters_length_1 = {5, 8, 10};
    template_length_process_data(simple_sample_factory::create_sample(SAMPLE_SIMPLE::SAMPLE_SIMPLE_02), 3, cluster_analysis::type_link::AVERAGE_LINK, expected_clusters_length_1);
}

TEST(utest_agglomerative, clustering_sampl_simple_02_one_cluster_link_average) {
    std::vector<size_t> expected_clusters_length_2 = {23};
    template_length_process_data(simple_sample_factory::create_sample(SAMPLE_SIMPLE::SAMPLE_SIMPLE_02), 1, cluster_analysis::type_link::AVERAGE_LINK, expected_clusters_length_2);
}

TEST(utest_agglomerative, clustering_sampl_simple_02_three_cluster_link_centroid) {
    std::vector<size_t> expected_clusters_length_1 = {5, 8, 10};
    template_length_process_data(simple_sample_factory::create_sample(SAMPLE_SIMPLE::SAMPLE_SIMPLE_02), 3, cluster_analysis::type_link::CENTROID_LINK, expected_clusters_length_1);
}

TEST(utest_agglomerative, clustering_sampl_simple_02_one_cluster_link_centroid) {
    std::vector<size_t> expected_clusters_length_2 = {23};
    template_length_process_data(simple_sample_factory::create_sample(SAMPLE_SIMPLE::SAMPLE_SIMPLE_02), 1, cluster_analysis::type_link::CENTROID_LINK, expected_clusters_length_2);
}

TEST(utest_agglomerative, clustering_sampl_simple_02_three_cluster_link_complete) {
    std::vector<size_t> expected_clusters_length_1 = {5, 8, 10};
    template_length_process_data(simple_sample_factory::create_sample(SAMPLE_SIMPLE::SAMPLE_SIMPLE_02), 3, cluster_analysis::type_link::COMPLETE_LINK, expected_clusters_length_1);
}

TEST(utest_agglomerative, clustering_sampl_simple_02_one_cluster_link_complete) {
    std::vector<size_t> expected_clusters_length_2 = {23};
    template_length_process_data(simple_sample_factory::create_sample(SAMPLE_SIMPLE::SAMPLE_SIMPLE_02), 1, cluster_analysis::type_link::COMPLETE_LINK, expected_clusters_length_2);
}

TEST(utest_agglomerative, clustering_sampl_simple_02_three_cluster_link_single) {
    std::vector<size_t> expected_clusters_length_1 = {5, 8, 10};
    template_length_process_data(simple_sample_factory::create_sample(SAMPLE_SIMPLE::SAMPLE_SIMPLE_02), 3, cluster_analysis::type_link::SINGLE_LINK, expected_clusters_length_1);
}

TEST(utest_agglomerative, clustering_sampl_simple_02_one_cluster_link_single) {
    std::vector<size_t> expected_clusters_length_2 = {23};
    template_length_process_data(simple_sample_factory::create_sample(SAMPLE_SIMPLE::SAMPLE_SIMPLE_02), 1, cluster_analysis::type_link::SINGLE_LINK, expected_clusters_length_2);
}

TEST(utest_agglomerative, clustering_sampl_simple_03_four_cluster_link_average) {
    std::vector<size_t> expected_clusters_length_1 = {10, 10, 10, 30};
    template_length_process_data(simple_sample_factory::create_sample(SAMPLE_SIMPLE::SAMPLE_SIMPLE_03), 4, cluster_analysis::type_link::AVERAGE_LINK, expected_clusters_length_1);
}

TEST(utest_agglomerative, clustering_sampl_simple_03_one_cluster_link_average) {
    std::vector<size_t> expected_clusters_length_2 = {60};
    template_length_process_data(simple_sample_factory::create_sample(SAMPLE_SIMPLE::SAMPLE_SIMPLE_03), 1, cluster_analysis::type_link::AVERAGE_LINK, expected_clusters_length_2);
}

TEST(utest_agglomerative, clustering_sampl_simple_03_four_cluster_link_centroid) {
    std::vector<size_t> expected_clusters_length_1 = {10, 10, 10, 30};
    template_length_process_data(simple_sample_factory::create_sample(SAMPLE_SIMPLE::SAMPLE_SIMPLE_03), 4, cluster_analysis::type_link::CENTROID_LINK, expected_clusters_length_1);
}

TEST(utest_agglomerative, clustering_sampl_simple_03_one_cluster_link_centroid) {
    std::vector<size_t> expected_clusters_length_2 = {60};
    template_length_process_data(simple_sample_factory::create_sample(SAMPLE_SIMPLE::SAMPLE_SIMPLE_03), 1, cluster_analysis::type_link::CENTROID_LINK, expected_clusters_length_2);
}

TEST(utest_agglomerative, clustering_sampl_simple_03_four_cluster_link_complete) {
    std::vector<size_t> expected_clusters_length_1 = {10, 10, 10, 30};
    template_length_process_data(simple_sample_factory::create_sample(SAMPLE_SIMPLE::SAMPLE_SIMPLE_03), 4, cluster_analysis::type_link::COMPLETE_LINK, expected_clusters_length_1);
}

TEST(utest_agglomerative, clustering_sampl_simple_03_one_cluster_link_complete) {
    std::vector<size_t> expected_clusters_length_2 = {60};
    template_length_process_data(simple_sample_factory::create_sample(SAMPLE_SIMPLE::SAMPLE_SIMPLE_03), 1, cluster_analysis::type_link::COMPLETE_LINK, expected_clusters_length_2);
}

TEST(utest_agglomerative, clustering_sampl_simple_03_four_cluster_link_single) {
    std::vector<size_t> expected_clusters_length_1 = {10, 10, 10, 30};
    template_length_process_data(simple_sample_factory::create_sample(SAMPLE_SIMPLE::SAMPLE_SIMPLE_03), 4, cluster_analysis::type_link::SINGLE_LINK, expected_clusters_length_1);
}

TEST(utest_agglomerative, clustering_sampl_simple_03_one_cluster_link_single) {
    std::vector<size_t> expected_clusters_length_2 = {60};
    template_length_process_data(simple_sample_factory::create_sample(SAMPLE_SIMPLE::SAMPLE_SIMPLE_03), 1, cluster_analysis::type_link::SINGLE_LINK, expected_clusters_length_2);
}

#endif
