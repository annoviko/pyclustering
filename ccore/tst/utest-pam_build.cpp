/*!

@authors Andrei Novikov (pyclustering@yandex.ru)
@date 2014-2020
@copyright BSD-3-Clause

*/


#include <gtest/gtest.h>

#include "answer.hpp"
#include "samples.hpp"

#include <pyclustering/cluster/pam_build.hpp>

#include <pyclustering/utils/metric.hpp>


using namespace pyclustering;
using namespace pyclustering::clst;
using namespace pyclustering::utils::metric;


void template_pam_build_medoids(const dataset_ptr & p_data, 
                                const std::size_t p_amount, 
                                const medoids & p_expected,
                                const data_t p_data_type,
                                const distance_metric<point> & p_metric = distance_metric_factory<point>::euclidean_square())
{
    dataset data;
    if (p_data_type == data_t::POINTS) {
        data = *p_data;
    }
    else {
        distance_matrix(*p_data, data);
    }

    medoids medoids;
    pam_build(p_amount, p_metric).initialize(data, p_data_type, medoids);

    ASSERT_EQ(p_amount, medoids.size());
    ASSERT_EQ(p_expected, medoids);
}


TEST(utest_pam_build, correct_medoids_simple_01) {
    template_pam_build_medoids(simple_sample_factory::create_sample(SAMPLE_SIMPLE::SAMPLE_SIMPLE_01), 2, { 4, 8 }, data_t::POINTS);
}


TEST(utest_pam_build, correct_medoids_simple_01_distance_matrix) {
    template_pam_build_medoids(simple_sample_factory::create_sample(SAMPLE_SIMPLE::SAMPLE_SIMPLE_01), 2, { 4, 8 }, data_t::DISTANCE_MATRIX);
}


TEST(utest_pam_build, correct_medoids_simple_01_wrong_amount_1) {
    template_pam_build_medoids(simple_sample_factory::create_sample(SAMPLE_SIMPLE::SAMPLE_SIMPLE_01), 1, { 4 }, data_t::POINTS);
}


TEST(utest_pam_build, correct_medoids_simple_01_wrong_amount_3) {
    template_pam_build_medoids(simple_sample_factory::create_sample(SAMPLE_SIMPLE::SAMPLE_SIMPLE_01), 3, { 4, 8, 0 }, data_t::POINTS);
}


TEST(utest_pam_build, correct_medoids_simple_01_wrong_amount_10) {
    template_pam_build_medoids(simple_sample_factory::create_sample(SAMPLE_SIMPLE::SAMPLE_SIMPLE_01), 10, { 4, 8, 0, 9, 1, 7, 6, 5, 2, 3 }, data_t::POINTS);
}


TEST(utest_pam_build, correct_medoids_simple_01_metrics) {
    template_pam_build_medoids(simple_sample_factory::create_sample(SAMPLE_SIMPLE::SAMPLE_SIMPLE_01), 2, { 4, 8 }, data_t::POINTS, distance_metric_factory<point>::euclidean_square());
    template_pam_build_medoids(simple_sample_factory::create_sample(SAMPLE_SIMPLE::SAMPLE_SIMPLE_01), 2, { 4, 8 }, data_t::POINTS, distance_metric_factory<point>::euclidean());
    template_pam_build_medoids(simple_sample_factory::create_sample(SAMPLE_SIMPLE::SAMPLE_SIMPLE_01), 2, { 4, 8 }, data_t::POINTS, distance_metric_factory<point>::manhattan());
    template_pam_build_medoids(simple_sample_factory::create_sample(SAMPLE_SIMPLE::SAMPLE_SIMPLE_01), 2, { 4, 8 }, data_t::POINTS, distance_metric_factory<point>::chebyshev());
    template_pam_build_medoids(simple_sample_factory::create_sample(SAMPLE_SIMPLE::SAMPLE_SIMPLE_01), 2, { 4, 8 }, data_t::POINTS, distance_metric_factory<point>::minkowski(2.0));
}


TEST(utest_pam_build, correct_medoids_simple_01_metrics_distance_matrix) {
    template_pam_build_medoids(simple_sample_factory::create_sample(SAMPLE_SIMPLE::SAMPLE_SIMPLE_01), 2, { 4, 8 }, data_t::DISTANCE_MATRIX, distance_metric_factory<point>::euclidean_square());
    template_pam_build_medoids(simple_sample_factory::create_sample(SAMPLE_SIMPLE::SAMPLE_SIMPLE_01), 2, { 4, 8 }, data_t::DISTANCE_MATRIX, distance_metric_factory<point>::euclidean());
    template_pam_build_medoids(simple_sample_factory::create_sample(SAMPLE_SIMPLE::SAMPLE_SIMPLE_01), 2, { 4, 8 }, data_t::DISTANCE_MATRIX, distance_metric_factory<point>::manhattan());
    template_pam_build_medoids(simple_sample_factory::create_sample(SAMPLE_SIMPLE::SAMPLE_SIMPLE_01), 2, { 4, 8 }, data_t::DISTANCE_MATRIX, distance_metric_factory<point>::chebyshev());
    template_pam_build_medoids(simple_sample_factory::create_sample(SAMPLE_SIMPLE::SAMPLE_SIMPLE_01), 2, { 4, 8 }, data_t::DISTANCE_MATRIX, distance_metric_factory<point>::minkowski(2.0));
}


TEST(utest_pam_build, correct_medoids_simple_02) {
    template_pam_build_medoids(simple_sample_factory::create_sample(SAMPLE_SIMPLE::SAMPLE_SIMPLE_02), 3, { 3, 20, 14 }, data_t::POINTS);
}


TEST(utest_pam_build, correct_medoids_simple_03) {
    template_pam_build_medoids(simple_sample_factory::create_sample(SAMPLE_SIMPLE::SAMPLE_SIMPLE_03), 4, { 28, 56, 5, 34 }, data_t::POINTS);
}


TEST(utest_pam_build, correct_medoids_simple_04) {
    template_pam_build_medoids(simple_sample_factory::create_sample(SAMPLE_SIMPLE::SAMPLE_SIMPLE_04), 5, { 44, 7, 64, 25, 55 }, data_t::POINTS);
}


TEST(utest_pam_build, correct_medoids_one_dimensional) {
    template_pam_build_medoids(simple_sample_factory::create_sample(SAMPLE_SIMPLE::SAMPLE_SIMPLE_09), 2, { 0, 20 }, data_t::POINTS);
    template_pam_build_medoids(simple_sample_factory::create_sample(SAMPLE_SIMPLE::SAMPLE_SIMPLE_09), 1, { 0 }, data_t::POINTS);
    template_pam_build_medoids(simple_sample_factory::create_sample(SAMPLE_SIMPLE::SAMPLE_SIMPLE_09), 3, { 0, 20, 1 }, data_t::POINTS);
}


TEST(utest_pam_build, correct_medoids_one_dimensional_distance_matrix) {
    template_pam_build_medoids(simple_sample_factory::create_sample(SAMPLE_SIMPLE::SAMPLE_SIMPLE_09), 2, { 0, 20 }, data_t::DISTANCE_MATRIX);
    template_pam_build_medoids(simple_sample_factory::create_sample(SAMPLE_SIMPLE::SAMPLE_SIMPLE_09), 1, { 0 }, data_t::DISTANCE_MATRIX);
    template_pam_build_medoids(simple_sample_factory::create_sample(SAMPLE_SIMPLE::SAMPLE_SIMPLE_09), 3, { 0, 20, 1 }, data_t::DISTANCE_MATRIX);
}


TEST(utest_pam_build, correct_medoids_three_dimensional) {
    template_pam_build_medoids(simple_sample_factory::create_sample(SAMPLE_SIMPLE::SAMPLE_SIMPLE_11), 2, { 15, 4 }, data_t::POINTS);
    template_pam_build_medoids(simple_sample_factory::create_sample(SAMPLE_SIMPLE::SAMPLE_SIMPLE_11), 1, { 15 }, data_t::POINTS);
    template_pam_build_medoids(simple_sample_factory::create_sample(SAMPLE_SIMPLE::SAMPLE_SIMPLE_11), 3, { 15, 4, 14 }, data_t::POINTS);
}


TEST(utest_pam_build, correct_medoids_three_dimensional_distance_matrix) {
    template_pam_build_medoids(simple_sample_factory::create_sample(SAMPLE_SIMPLE::SAMPLE_SIMPLE_11), 2, { 15, 4 }, data_t::DISTANCE_MATRIX);
    template_pam_build_medoids(simple_sample_factory::create_sample(SAMPLE_SIMPLE::SAMPLE_SIMPLE_11), 1, { 15 }, data_t::DISTANCE_MATRIX);
    template_pam_build_medoids(simple_sample_factory::create_sample(SAMPLE_SIMPLE::SAMPLE_SIMPLE_11), 3, { 15, 4, 14 }, data_t::DISTANCE_MATRIX);
}


#if 0
TEST(utest_pam_build, test_performance) {
    auto p_data = fcps_sample_factory::create_sample(FCPS_SAMPLE::ENGY_TIME);

    dataset data;
    auto p_data_type = data_t::DISTANCE_MATRIX;

    if (p_data_type == data_t::POINTS) {
        data = *p_data;
    }
    else {
        distance_matrix(*p_data, data);
    }

    medoids medoids;
    pam_build(10).initialize(data, p_data_type, medoids);

    ASSERT_EQ(10, medoids.size());
}
#endif