/**
*
* @authors Andrei Novikov (pyclustering@yandex.ru)
* @date 2014-2020
* @copyright GNU Public License
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


#include <gtest/gtest.h>

#include <pyclustering/cluster/cure.hpp>

#include "samples.hpp"
#include "utenv_check.hpp"


using namespace pyclustering;
using namespace pyclustering::clst;


static void
template_length_process_data(const std::shared_ptr<dataset> & p_data,
        const size_t p_amount_clusters,
        const size_t p_number_represent_points,
        const double p_compression,
        const std::vector<size_t> & p_expected_cluster_length) {

    cure_data output_result;
    cure solver(p_amount_clusters, p_number_represent_points, p_compression);
    solver.process(*p_data, output_result);

    const dataset & data = *p_data;
    const cluster_sequence & actual_clusters = output_result.clusters();
    ASSERT_CLUSTER_SIZES(data, actual_clusters, p_expected_cluster_length);

    ASSERT_EQ(p_amount_clusters, output_result.representors().size());
    for (auto cluster_representors : output_result.representors()) {
        ASSERT_TRUE(cluster_representors.size() > 0);
    }

    const size_t dimension = (*p_data)[0].size();

    ASSERT_EQ(p_amount_clusters, output_result.means().size());
    for (auto cluster_mean : output_result.means()) {
        ASSERT_EQ(dimension, cluster_mean.size());
    }
}


TEST(utest_cure, allocation_sample_simple_01) {
    const std::vector<size_t> expected_clusters_length = { 5, 5 };
    template_length_process_data(simple_sample_factory::create_sample(SAMPLE_SIMPLE::SAMPLE_SIMPLE_01), 2, 5, 0.5, expected_clusters_length);
}


TEST(utest_cure, allocation_sample_simple_01_one_representative) {
    const std::vector<size_t> expected_clusters_length = { 5, 5 };
    template_length_process_data(simple_sample_factory::create_sample(SAMPLE_SIMPLE::SAMPLE_SIMPLE_01), 2, 1, 0.5, expected_clusters_length);
}


TEST(utest_cure, allocation_sample_simple_01_no_compression) {
    const std::vector<size_t> expected_clusters_length = { 5, 5 };
    template_length_process_data(simple_sample_factory::create_sample(SAMPLE_SIMPLE::SAMPLE_SIMPLE_01), 2, 5, 0.0, expected_clusters_length);
}


TEST(utest_cure, allocation_sample_one_allocation_simple_01) {
    const std::vector<size_t> expected_clusters_length = { 10 };
    template_length_process_data(simple_sample_factory::create_sample(SAMPLE_SIMPLE::SAMPLE_SIMPLE_01), 1, 5, 0.5, expected_clusters_length);
}


TEST(utest_cure, allocation_sample_simple_02) {
    const std::vector<size_t> expected_clusters_length = { 10, 5, 8 };
    template_length_process_data(simple_sample_factory::create_sample(SAMPLE_SIMPLE::SAMPLE_SIMPLE_02), 3, 5, 0.5, expected_clusters_length);
}


TEST(utest_cure, allocation_sample_simple_02_one_representative) {
    const std::vector<size_t> expected_clusters_length = { 10, 5, 8 };
    template_length_process_data(simple_sample_factory::create_sample(SAMPLE_SIMPLE::SAMPLE_SIMPLE_02), 3, 1, 0.5, expected_clusters_length);
}


TEST(utest_cure, allocation_sample_simple_02_no_compression) {
    const std::vector<size_t> expected_clusters_length = { 10, 5, 8 };
    template_length_process_data(simple_sample_factory::create_sample(SAMPLE_SIMPLE::SAMPLE_SIMPLE_02), 3, 5, 0.0, expected_clusters_length);
}


TEST(utest_cure, allocation_sample_one_allocation_simple_02) {
    const std::vector<size_t> expected_clusters_length = { 23 };
    template_length_process_data(simple_sample_factory::create_sample(SAMPLE_SIMPLE::SAMPLE_SIMPLE_02), 1, 5, 0.5, expected_clusters_length);
}


TEST(utest_cure, allocation_sample_simple_03) {
    const std::vector<size_t> expected_clusters_length = { 10, 10, 10, 30 };
    template_length_process_data(simple_sample_factory::create_sample(SAMPLE_SIMPLE::SAMPLE_SIMPLE_03), 4, 5, 0.5, expected_clusters_length);
}


TEST(utest_cure, allocation_sample_one_allocation_simple_03) {
    const std::vector<size_t> expected_clusters_length = { 60 };
    template_length_process_data(simple_sample_factory::create_sample(SAMPLE_SIMPLE::SAMPLE_SIMPLE_03), 1, 5, 0.5, expected_clusters_length);
}


TEST(utest_cure, allocation_sample_simple_04) {
    const std::vector<size_t> expected_clusters_length = { 15, 15, 15, 15, 15 };
    template_length_process_data(simple_sample_factory::create_sample(SAMPLE_SIMPLE::SAMPLE_SIMPLE_04), 5, 5, 0.5, expected_clusters_length);
}


TEST(utest_cure, allocation_sample_simple_05) {
    const std::vector<size_t> expected_clusters_length = { 15, 15, 15, 15 };
    template_length_process_data(simple_sample_factory::create_sample(SAMPLE_SIMPLE::SAMPLE_SIMPLE_05), 4, 5, 0.5, expected_clusters_length);
}


TEST(utest_cure, allocation_sample_simple_07) {
    const std::vector<size_t> expected_clusters_length = { 10, 10 };
    template_length_process_data(simple_sample_factory::create_sample(SAMPLE_SIMPLE::SAMPLE_SIMPLE_07), 2, 5, 0.5, expected_clusters_length);
}


TEST(utest_cure, allocation_sample_simple_08) {
    const std::vector<size_t> expected_clusters_length = { 15, 30, 20, 80 };
    template_length_process_data(simple_sample_factory::create_sample(SAMPLE_SIMPLE::SAMPLE_SIMPLE_08), 4, 5, 0.5, expected_clusters_length);
}


TEST(utest_cure, allocation_sample_simple_09) {
    const std::vector<size_t> expected_clusters_length = { 10, 20 };
    template_length_process_data(simple_sample_factory::create_sample(SAMPLE_SIMPLE::SAMPLE_SIMPLE_09), 2, 5, 0.3, expected_clusters_length);
}


TEST(utest_cure, allocation_sample_simple_10) {
    const std::vector<size_t> expected_clusters_length = { 11, 11, 11 };
    template_length_process_data(simple_sample_factory::create_sample(SAMPLE_SIMPLE::SAMPLE_SIMPLE_10), 3, 5, 0.3, expected_clusters_length);
}


TEST(utest_cure, allocation_sample_simple_10_one_representative) {
    const std::vector<size_t> expected_clusters_length = { 11, 11, 11 };
    template_length_process_data(simple_sample_factory::create_sample(SAMPLE_SIMPLE::SAMPLE_SIMPLE_10), 3, 1, 0.3, expected_clusters_length);
}


TEST(utest_cure, allocation_sample_simple_11) {
    const std::vector<size_t> expected_clusters_length = { 10, 10 };
    template_length_process_data(simple_sample_factory::create_sample(SAMPLE_SIMPLE::SAMPLE_SIMPLE_11), 2, 5, 0.3, expected_clusters_length);
}


TEST(utest_cure, allocation_sample_simple_11_one_representative) {
    const std::vector<size_t> expected_clusters_length = { 10, 10 };
    template_length_process_data(simple_sample_factory::create_sample(SAMPLE_SIMPLE::SAMPLE_SIMPLE_11), 2, 1, 0.3, expected_clusters_length);
}


TEST(utest_cure, allocation_sample_simple_12) {
    const std::vector<size_t> expected_clusters_length = { 5, 5, 5 };
    template_length_process_data(simple_sample_factory::create_sample(SAMPLE_SIMPLE::SAMPLE_SIMPLE_12), 3, 5, 0.3, expected_clusters_length);
}


TEST(utest_cure, allocation_sample_simple_12_one_representative) {
    const std::vector<size_t> expected_clusters_length = { 5, 5, 5 };
    template_length_process_data(simple_sample_factory::create_sample(SAMPLE_SIMPLE::SAMPLE_SIMPLE_12), 3, 1, 0.3, expected_clusters_length);
}


TEST(utest_cure, allocation_hepta) {
    const std::vector<size_t> expected_clusters_length = { 30, 30, 30, 30, 30, 30, 32 };
    template_length_process_data(fcps_sample_factory::create_sample(FCPS_SAMPLE::HEPTA), 7, 5, 0.3, expected_clusters_length);
}


TEST(utest_cure, allocation_hepta_max_compression) {
    const std::vector<size_t> expected_clusters_length = { 30, 30, 30, 30, 30, 30, 32 };
    template_length_process_data(fcps_sample_factory::create_sample(FCPS_SAMPLE::HEPTA), 7, 5, 1.0, expected_clusters_length);
}


TEST(utest_cure, allocation_hepta_one_representative) {
    const std::vector<size_t> expected_clusters_length = { 30, 30, 30, 30, 30, 30, 32 };
    template_length_process_data(fcps_sample_factory::create_sample(FCPS_SAMPLE::HEPTA), 7, 1, 0.3, expected_clusters_length);
}


TEST(utest_cure, allocation_hepta_one_cluster_allocation) {
    const std::vector<size_t> expected_clusters_length = { 212 };
    template_length_process_data(fcps_sample_factory::create_sample(FCPS_SAMPLE::HEPTA), 1, 1, 0.3, expected_clusters_length);
}


#ifndef VALGRIND_ANALYSIS_SHOCK

TEST(utest_cure, allocation_tetra) {
    const std::vector<size_t> expected_clusters_length = { 100, 100, 100, 100 };
    template_length_process_data(fcps_sample_factory::create_sample(FCPS_SAMPLE::TETRA), 4, 5, 0.5, expected_clusters_length);
}


TEST(utest_cure, allocation_lsun) {
    const std::vector<size_t> expected_clusters_length = { 100, 101, 202 };
    template_length_process_data(fcps_sample_factory::create_sample(FCPS_SAMPLE::LSUN), 3, 5, 0.3, expected_clusters_length);
}


TEST(utest_cure, allocation_two_diamonds) {
    const std::vector<size_t> expected_clusters_length = { 399, 401 };
    template_length_process_data(fcps_sample_factory::create_sample(FCPS_SAMPLE::TWO_DIAMONDS), 2, 5, 0.5, expected_clusters_length);
}


TEST(utest_cure, allocation_wing_nut) {
    const std::vector<size_t> expected_clusters_length = { 508, 508 };
    template_length_process_data(fcps_sample_factory::create_sample(FCPS_SAMPLE::WING_NUT), 2, 4, 0.3, expected_clusters_length);
}


TEST(utest_cure, allocation_chainlink) {
    const std::vector<size_t> expected_clusters_length = { 500, 500 };
    template_length_process_data(fcps_sample_factory::create_sample(FCPS_SAMPLE::CHAINLINK), 2, 10, 0.3, expected_clusters_length);
}

#endif
