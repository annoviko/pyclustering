/*!

@authors Andrei Novikov (pyclustering@yandex.ru)
@date 2014-2020
@copyright BSD-3-Clause

*/


#include <gtest/gtest.h>

#include <pyclustering/interface/pam_build_interface.h>
#include <pyclustering/interface/pyclustering_package.hpp>
#include <pyclustering/utils/metric.hpp>

#include "samples.hpp"

#include "answer.hpp"
#include "answer_reader.hpp"
#include "utenv_utils.hpp"

#include <memory>


using namespace pyclustering;
using namespace pyclustering::utils::metric;


TEST(utest_interface_pam_build, pam_build) {
    dataset_ptr data = simple_sample_factory::create_sample(SAMPLE_SIMPLE::SAMPLE_SIMPLE_01);
    answer ans = answer_reader::read(SAMPLE_SIMPLE::SAMPLE_SIMPLE_01);

    std::shared_ptr<pyclustering_package> data_package = pack(*data);
    distance_metric<point> metric = distance_metric_factory<point>::euclidean_square();

    pyclustering_package * result = pam_build_algorithm(data_package.get(), 2, &metric, 0);

    ASSERT_NE(nullptr, result);

    delete result;
}



TEST(utest_interface_pam_build, pam_build_null_metric) {
    dataset_ptr data = simple_sample_factory::create_sample(SAMPLE_SIMPLE::SAMPLE_SIMPLE_01);
    answer ans = answer_reader::read(SAMPLE_SIMPLE::SAMPLE_SIMPLE_01);

    std::shared_ptr<pyclustering_package> data_package = pack(*data);

    pyclustering_package * result = pam_build_algorithm(data_package.get(), 2, nullptr, 0);

    ASSERT_NE(nullptr, result);

    delete result;
}
