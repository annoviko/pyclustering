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

#ifndef _UTEST_KMEDIANS_
#define _UTEST_KMEDIANS_


#include "gtest/gtest.h"

#include "samples.hpp"

#include "cluster/kmedians.hpp"
#include "utest-cluster.hpp"


using namespace cluster_analysis;


static void
template_kmedians_length_process_data(const dataset_ptr & p_data,
const dataset & p_start_medians,
const std::vector<size_t> & p_expected_cluster_length)
{
    kmedians_data output_result;
    kmedians solver(p_start_medians, 0.0001);
    solver.process(*p_data, output_result);

    const dataset & data = *p_data;
    const cluster_sequence & actual_clusters = *(output_result.clusters());
    ASSERT_CLUSTER_SIZES(data, actual_clusters, p_expected_cluster_length);
}


TEST(utest_kmedians, allocation_sample_simple_01) {
    dataset start_medians = { { 3.7, 5.5 }, { 6.7, 7.5 } };
    std::vector<size_t> expected_clusters_length = { 5, 5 };
    template_kmedians_length_process_data(simple_sample_factory::create_sample(SAMPLE_SIMPLE::SAMPLE_SIMPLE_01), start_medians, expected_clusters_length);
}

TEST(utest_kmedians, allocation_sample_simple_02) {
    dataset start_medians = { { 3.5, 4.8 }, { 6.9, 7.0 }, { 7.5, 0.5 } };
    std::vector<size_t> expected_clusters_length = { 10, 5, 8 };
    template_kmedians_length_process_data(simple_sample_factory::create_sample(SAMPLE_SIMPLE::SAMPLE_SIMPLE_02), start_medians, expected_clusters_length);
}

TEST(utest_kmedians, allocation_sample_simple_03) {
    dataset start_medians = { { 0.2, 0.1 }, { 4.0, 1.0 }, { 2.0, 2.0 }, { 2.3, 3.9 } };
    std::vector<size_t> expected_clusters_length = { 10, 10, 10, 30 };
    template_kmedians_length_process_data(simple_sample_factory::create_sample(SAMPLE_SIMPLE::SAMPLE_SIMPLE_03), start_medians, expected_clusters_length);
}

TEST(utest_kmedians, large_number_medians_sample_simple_01) {
    dataset start_medians = { { 1.7, 2.6 }, { 3.7, 4.5 }, { 4.5, 1.6 }, { 6.4, 5.0 }, { 2.2, 2.2 } };
    std::vector<size_t> expected_clusters_length;   /* pass empty */
    template_kmedians_length_process_data(simple_sample_factory::create_sample(SAMPLE_SIMPLE::SAMPLE_SIMPLE_01), start_medians, expected_clusters_length);
}

TEST(utest_kmedians, large_number_medians_sample_simple_02) {
    dataset start_medians = { { -1.5, 0.8 }, { -4.9, 5.0 }, { 2.3, 3.2 }, { -1.2, -0.8 }, { 2.5, 2.9 }, { 6.8, 7.9 } };
    std::vector<size_t> expected_clusters_length;   /* pass empty */
    template_kmedians_length_process_data(simple_sample_factory::create_sample(SAMPLE_SIMPLE::SAMPLE_SIMPLE_02), start_medians, expected_clusters_length);
}


TEST(utest_kmedians, large_number_medians_sample_simple_03) {
    dataset start_medians = { { -8.1, 2.3 }, { -4.9, 5.5 }, { 1.3, 8.3 }, { -2.6, -1.7 }, { 5.3, 4.2 }, { 2.1, 0.0 }, { 1.7, 0.4 } };
    std::vector<size_t> expected_clusters_length;   /* pass empty */
    template_kmedians_length_process_data(simple_sample_factory::create_sample(SAMPLE_SIMPLE::SAMPLE_SIMPLE_03), start_medians, expected_clusters_length);
}


TEST(utest_kmedians, one_dimension_sample_simple_07) {
    dataset start_medians = { { -2.0 }, { 4.0 } };
    std::vector<size_t> expected_clusters_length = { 10, 10 };
    template_kmedians_length_process_data(simple_sample_factory::create_sample(SAMPLE_SIMPLE::SAMPLE_SIMPLE_07), start_medians, expected_clusters_length);
}


TEST(utest_kmedians, one_dimension_sample_simple_08) {
    dataset start_medians = { { -4.0 }, { 3.0 }, { 6.0 }, { 10.0 } };
    std::vector<size_t> expected_clusters_length = { 15, 30, 20, 80 };
    template_kmedians_length_process_data(simple_sample_factory::create_sample(SAMPLE_SIMPLE::SAMPLE_SIMPLE_08), start_medians, expected_clusters_length);
}


TEST(utest_kmedians, rough_medians_sample_simple_10) {
    dataset start_medians = { { 0.0772944481804071, 0.05224990900863469 }, { 1.6021689021213712, 1.0347579135245601 }, { 2.3341008076636096, 1.280022869739064 } };
    std::vector<size_t> expected_clusters_length;   /* pass empty */
    template_kmedians_length_process_data(simple_sample_factory::create_sample(SAMPLE_SIMPLE::SAMPLE_SIMPLE_10), start_medians, expected_clusters_length);
}


#endif
