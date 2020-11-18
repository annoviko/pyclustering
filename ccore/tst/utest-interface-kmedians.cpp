/*!

@authors Andrei Novikov (pyclustering@yandex.ru)
@date 2014-2020
@copyright BSD-3-Clause

*/

#include <gtest/gtest.h>

#include <pyclustering/interface/kmedians_interface.h>
#include <pyclustering/interface/pyclustering_package.hpp>

#include <pyclustering/utils/metric.hpp>

#include "utenv_utils.hpp"

#include <memory>


using namespace pyclustering;
using namespace pyclustering::utils::metric;


TEST(utest_interface_kmedians, kmedians_api) {
    std::shared_ptr<pyclustering_package> sample = pack(dataset({ { 1 }, { 2 }, { 3 }, { 10 }, { 11 }, { 12 } }));
    std::shared_ptr<pyclustering_package> medians = pack(dataset({ { 1 }, { 10 } }));

    distance_metric<point> metric = distance_metric_factory<point>::euclidean_square();

    pyclustering_package * kmedians_result = kmedians_algorithm(sample.get(), medians.get(), 0.001, 100, &metric);
    ASSERT_NE(nullptr, kmedians_result);

    delete kmedians_result;
}


TEST(utest_interface_kmedians, kmedians_api_null_metric) {
    std::shared_ptr<pyclustering_package> sample = pack(dataset({ { 1 }, { 2 }, { 3 }, { 10 }, { 11 }, { 12 } }));
    std::shared_ptr<pyclustering_package> medians = pack(dataset({ { 1 }, { 10 } }));

    pyclustering_package * kmedians_result = kmedians_algorithm(sample.get(), medians.get(), 0.001, 100, nullptr);
    ASSERT_NE(nullptr, kmedians_result);

    delete kmedians_result;
}