/*!

@authors Andrei Novikov (pyclustering@yandex.ru)
@date 2014-2020
@copyright BSD-3-Clause

*/

#include <gtest/gtest.h>

#include <pyclustering/interface/bsas_interface.h>
#include <pyclustering/interface/pyclustering_package.hpp>

#include <pyclustering/utils/metric.hpp>

#include "utenv_utils.hpp"

#include <memory>


using namespace pyclustering;
using namespace pyclustering::utils::metric;


TEST(utest_interface_bsas, bsas_api) {
    std::shared_ptr<pyclustering_package> sample = pack(dataset({ { 1 }, { 2 }, { 3 }, { 10 }, { 11 }, { 12 } }));

    distance_metric<point> metric = distance_metric_factory<point>::euclidean_square();

    pyclustering_package * bsas_result = bsas_algorithm(sample.get(), 2, 1.0, &metric);
    ASSERT_NE(nullptr, bsas_result);

    delete bsas_result;
}