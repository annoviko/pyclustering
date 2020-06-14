/*!

@authors Andrei Novikov (pyclustering@yandex.ru)
@date 2014-2020
@copyright GNU Public License

@cond GNU_PUBLIC_LICENSE
    pyclustering is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    pyclustering is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
@endcond

*/



#include <gtest/gtest.h>

#include "samples.hpp"

#include <pyclustering/cluster/fcm.hpp>

#include "utenv_check.hpp"

#include <cmath>
#include <numeric>


using namespace pyclustering;
using namespace pyclustering::clst;


static void template_fcm_data_processing(
    const dataset_ptr & p_data,
    const dataset & p_start_centers,
    const double p_m,
    const std::vector<size_t> & p_expected_cluster_length,
    const std::size_t p_itermax = fcm::DEFAULT_ITERMAX)
{
    fcm_data output_result;
    fcm solver(p_start_centers, p_m, fcm::DEFAULT_TOLERANCE, p_itermax);

    solver.process(*p_data, output_result);

    if (p_itermax == 0) {
        ASSERT_TRUE(output_result.clusters().empty());
        ASSERT_TRUE(output_result.membership().empty());
        ASSERT_EQ(p_start_centers, output_result.centers());
        return;
    }

    for (const auto & probablities : output_result.membership()) {
        double total_probability = std::accumulate(probablities.begin(), probablities.end(), 0.0);
        ASSERT_DOUBLE_EQ(1.0, total_probability);
    }

    ASSERT_CLUSTER_SIZES(*p_data, output_result.clusters(), p_expected_cluster_length);

    const std::size_t dimension = p_data->at(0).size();
    for (const auto & center : output_result.centers()) {
        ASSERT_EQ(dimension, center.size());

        for (std::size_t dim = 0; dim < center.size(); dim++) {
            ASSERT_FALSE(std::isnan(center[dim]));
        }
    }

    ASSERT_EQ(output_result.centers().size(), output_result.clusters().size());
}


TEST(utest_fcm, allocation_sample_simple_01) {
    dataset start_centers = { { 3.7, 5.5 },{ 6.7, 7.5 } };
    std::vector<size_t> expected_clusters_length = { 5, 5 };
    template_fcm_data_processing(simple_sample_factory::create_sample(SAMPLE_SIMPLE::SAMPLE_SIMPLE_01), start_centers, 2, expected_clusters_length);
}


TEST(utest_fcm, allocation_sample_simple_01_centers_are_points) {
    dataset start_centers = { { 3.522979, 5.487981 }, { 6.750795, 7.269541 } };
    std::vector<size_t> expected_clusters_length = { 5, 5 };
    template_fcm_data_processing(simple_sample_factory::create_sample(SAMPLE_SIMPLE::SAMPLE_SIMPLE_01), start_centers, 2, expected_clusters_length);
}


TEST(utest_fcm, allocation_sample_simple_01_one_cluster) {
    dataset start_centers = { { 3.7, 5.5 } };
    std::vector<size_t> expected_clusters_length = { 10 };
    template_fcm_data_processing(simple_sample_factory::create_sample(SAMPLE_SIMPLE::SAMPLE_SIMPLE_01), start_centers, 2, expected_clusters_length);
}


TEST(utest_fcm, allocation_sample_simple_01_hyper_4) {
    dataset start_centers = { { 3.7, 5.5 },{ 6.7, 7.5 } };
    std::vector<size_t> expected_clusters_length = { 5, 5 };
    template_fcm_data_processing(simple_sample_factory::create_sample(SAMPLE_SIMPLE::SAMPLE_SIMPLE_01), start_centers, 4, expected_clusters_length);
}


TEST(utest_fcm, allocation_sample_simple_02) {
    dataset start_centers = { { 3.5, 4.8 },{ 6.9, 7.0 },{ 7.5, 0.5 } };
    std::vector<size_t> expected_clusters_length = { 10, 5, 8 };
    template_fcm_data_processing(simple_sample_factory::create_sample(SAMPLE_SIMPLE::SAMPLE_SIMPLE_02), start_centers, 2, expected_clusters_length);
}


TEST(utest_fcm, allocation_sample_simple_02_centers_are_points) {
    dataset start_centers = { { 3.889032, 4.103663 }, { 7.090406, 6.647416 }, { 7.482343, 0.762685 } };
    std::vector<size_t> expected_clusters_length = { 10, 5, 8 };
    template_fcm_data_processing(simple_sample_factory::create_sample(SAMPLE_SIMPLE::SAMPLE_SIMPLE_02), start_centers, 2, expected_clusters_length);
}


TEST(utest_fcm, allocation_sample_simple_02_one_cluster) {
    dataset start_centers = { { 3.5, 4.8 } };
    std::vector<size_t> expected_clusters_length = { 23 };
    template_fcm_data_processing(simple_sample_factory::create_sample(SAMPLE_SIMPLE::SAMPLE_SIMPLE_02), start_centers, 2, expected_clusters_length);
}


TEST(utest_fcm, allocation_sample_simple_03) {
    dataset start_centers = { { 0.2, 0.1 },{ 4.0, 1.0 },{ 2.0, 2.0 },{ 2.3, 3.9 } };
    std::vector<size_t> expected_clusters_length = { 10, 10, 10, 30 };
    template_fcm_data_processing(simple_sample_factory::create_sample(SAMPLE_SIMPLE::SAMPLE_SIMPLE_03), start_centers, 2, expected_clusters_length);
}


TEST(utest_fcm, allocation_sample_simple_04) {
    dataset start_centers = { { 1.5, 0.0 }, { 1.5, 2.0 }, { 1.5, 4.0 }, { 1.5, 6.0 }, { 1.5, 8.0 } };
    std::vector<size_t> expected_clusters_length = { 15, 15, 15, 15, 15 };
    template_fcm_data_processing(simple_sample_factory::create_sample(SAMPLE_SIMPLE::SAMPLE_SIMPLE_04), start_centers, 2, expected_clusters_length);
}


TEST(utest_fcm, allocation_sample_simple_05) {
    dataset start_centers = { { 0.0, 1.0 }, { 0.0, 0.0 }, { 1.0, 1.0 }, { 1.0, 0.0 } };
    std::vector<size_t> expected_clusters_length = { 15, 15, 15, 15 };
    template_fcm_data_processing(simple_sample_factory::create_sample(SAMPLE_SIMPLE::SAMPLE_SIMPLE_05), start_centers, 2, expected_clusters_length);
}


TEST(utest_fcm, allocation_sample_simple_07) {
    dataset start_centers = { { -3.0 }, { 2.0 } };
    std::vector<size_t> expected_clusters_length = { 10, 10 };
    template_fcm_data_processing(simple_sample_factory::create_sample(SAMPLE_SIMPLE::SAMPLE_SIMPLE_07), start_centers, 2, expected_clusters_length);
}


TEST(utest_fcm, allocation_sample_simple_07_centers_are_points) {
    dataset start_centers = { { -2.18865771721 }, { 4.18586756767 } };
    std::vector<size_t> expected_clusters_length = { 10, 10 };
    template_fcm_data_processing(simple_sample_factory::create_sample(SAMPLE_SIMPLE::SAMPLE_SIMPLE_07), start_centers, 2, expected_clusters_length);
}


TEST(utest_fcm, allocation_sample_simple_08) {
    dataset start_centers = { { -4.0 }, { 3.1 }, { 6.1 }, { 12.0 } };
    std::vector<size_t> expected_clusters_length = { 15, 30, 20, 80 };
    template_fcm_data_processing(simple_sample_factory::create_sample(SAMPLE_SIMPLE::SAMPLE_SIMPLE_08), start_centers, 2, expected_clusters_length);
}


TEST(utest_fcm, allocation_sample_simple_09) {
    dataset start_centers = { { 4.0 }, { 8.0 } };
    std::vector<size_t> expected_clusters_length = { 10, 20 };
    template_fcm_data_processing(simple_sample_factory::create_sample(SAMPLE_SIMPLE::SAMPLE_SIMPLE_09), start_centers, 2, expected_clusters_length);
}


TEST(utest_fcm, allocation_sample_simple_09_centers_are_points) {
    dataset start_centers = { { 4.1232 }, { 7.8391 } };
    std::vector<size_t> expected_clusters_length = { 30, 0 };
    template_fcm_data_processing(simple_sample_factory::create_sample(SAMPLE_SIMPLE::SAMPLE_SIMPLE_09), start_centers, 2, expected_clusters_length);
}


TEST(utest_fcm, allocation_sample_simple_11) {
    dataset start_centers = { { 1.0, 0.6, 0.8 }, { 4.1, 4.2, 4.3 } };
    std::vector<size_t> expected_clusters_length = { 10, 10 };
    template_fcm_data_processing(simple_sample_factory::create_sample(SAMPLE_SIMPLE::SAMPLE_SIMPLE_11), start_centers, 2, expected_clusters_length);
}


TEST(utest_fcm, allocation_sample_simple_12) {
    dataset start_centers = { { 1.0, 1.0 }, { 2.5, 2.5 }, { 4.0, 4.0 } };
    std::vector<size_t> expected_clusters_length = { 5, 5, 5 };
    template_fcm_data_processing(simple_sample_factory::create_sample(SAMPLE_SIMPLE::SAMPLE_SIMPLE_12), start_centers, 2, expected_clusters_length);
}


TEST(utest_fcm, allocation_famous_old_faithful) {
    dataset start_centers = { { 4.0, 70 }, { 1.0, 48 } };
    std::vector<size_t> expected_clusters_length = { };
    template_fcm_data_processing(famous_sample_factory::create_sample(FAMOUS_SAMPLE::OLD_FAITHFUL), start_centers, 2, expected_clusters_length);
}


TEST(utest_fcm, allocation_fcps_hepta) {
    dataset start_centers = { { -0.06, 0.02, 0.02 }, { 2.41, 0.49, 0.03 }, { -2.69, 0.34, 0.29 }, { 0.49, 2.89, 0.78 }, { -0.60, -2.31, 0.05 }, { -0.15, 0.77, 3.23 }, { -0.50, 0.43, -2.60 } };
    std::vector<size_t> expected_clusters_length = { 30, 30, 30, 30, 30, 30, 32 };
    template_fcm_data_processing(fcps_sample_factory::create_sample(FCPS_SAMPLE::HEPTA), start_centers, 2, expected_clusters_length);
}


TEST(utest_fcm, allocation_fcps_tetra) {
    dataset start_centers = { { 1.001, -0.083, -0.681 }, { -0.811, 0.476, -0.759 }, { -0.956, -1.427, -0.020 }, { 0.225, 0.560, 1.794 } };
    std::vector<size_t> expected_clusters_length = { 100, 100, 100, 100 };
    template_fcm_data_processing(fcps_sample_factory::create_sample(FCPS_SAMPLE::TETRA), start_centers, 2, expected_clusters_length);
}


TEST(utest_fcm, incorrect_hyper_parameter_positive) {
    dataset start_centers = { { 3.7, 5.5 },{ 6.7, 7.5 } };
    EXPECT_THROW(fcm(start_centers, 1.0), std::invalid_argument);
}


TEST(utest_fcm, incorrect_hyper_parameter_negative) {
    dataset start_centers = { { 3.7, 5.5 },{ 6.7, 7.5 } };
    EXPECT_THROW(fcm(start_centers, -1.0), std::invalid_argument);
}


TEST(utest_fcm, itermax_0) {
    dataset start_centers = { { 3.7, 5.5 },{ 6.7, 7.5 } };
    std::vector<size_t> expected_clusters_length = { };
    template_fcm_data_processing(simple_sample_factory::create_sample(SAMPLE_SIMPLE::SAMPLE_SIMPLE_01), start_centers, 2, expected_clusters_length, 0);
}


TEST(utest_fcm, itermax_1) {
    dataset start_centers = { { 3.7, 5.5 },{ 6.7, 7.5 } };
    std::vector<size_t> expected_clusters_length = { 5, 5 };  /* it is enough to make one step to obtain proper result */
    template_fcm_data_processing(simple_sample_factory::create_sample(SAMPLE_SIMPLE::SAMPLE_SIMPLE_01), start_centers, 2, expected_clusters_length, 1);
}

TEST(utest_fcm, itermax_10_simple01) {
    dataset start_centers = { { 3.7, 5.5 },{ 6.7, 7.5 } };
    std::vector<size_t> expected_clusters_length = { 5, 5 };
    template_fcm_data_processing(simple_sample_factory::create_sample(SAMPLE_SIMPLE::SAMPLE_SIMPLE_01), start_centers, 2, expected_clusters_length, 10);
}

TEST(utest_fcm, itermax_10_simple02) {
    dataset start_centers = { { 3.5, 4.8 },{ 6.9, 7.0 },{ 7.5, 0.5 } };
    std::vector<size_t> expected_clusters_length = { 10, 5, 8 };
    template_fcm_data_processing(simple_sample_factory::create_sample(SAMPLE_SIMPLE::SAMPLE_SIMPLE_02), start_centers, 2, expected_clusters_length, 10);
}


#ifdef UT_PERFORMANCE_SESSION
#include <chrono>

TEST(performance_fcm, big_data) {
    auto points = simple_sample_factory::create_random_sample(100000, 10);
    auto centers = simple_sample_factory::create_random_sample(1, 10);

    auto start = std::chrono::system_clock::now();

    const std::size_t repeat = 1;
    for (std::size_t i = 0; i < repeat; i++) {
      fcm_data output_result;
      fcm solver(*centers, 2.0);
      solver.process(*points, output_result);
    }

    auto end = std::chrono::system_clock::now();

    std::chrono::duration<double> difference = end - start;
    std::cout << "Clustering time: '" << difference.count() / repeat << "' sec." << std::endl;
}
#endif