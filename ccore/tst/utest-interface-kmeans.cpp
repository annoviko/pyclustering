/*!

@authors Andrei Novikov (pyclustering@yandex.ru)
@date 2014-2020
@copyright BSD-3-Clause

*/

#include <gtest/gtest.h>

#include <pyclustering/interface/kmeans_interface.h>
#include <pyclustering/interface/pyclustering_package.hpp>

#include <pyclustering/utils/metric.hpp>

#include "utenv_utils.hpp"

#include <memory>


using namespace pyclustering;
using namespace pyclustering::utils::metric;


TEST(utest_interface_kmeans, kmeans_api) {
    std::shared_ptr<pyclustering_package> sample = pack(dataset({ { 1 }, { 2 }, { 3 }, { 10 }, { 11 }, { 12 } }));
    std::shared_ptr<pyclustering_package> centers = pack(dataset({ { 1 }, { 10 } }));

    distance_metric<point> metric = distance_metric_factory<point>::euclidean_square();

    pyclustering_package * kmeans_result = kmeans_algorithm(sample.get(), centers.get(), 0.001, 200, false, &metric);
    ASSERT_NE(nullptr, kmeans_result);

    delete kmeans_result;
    kmeans_result = nullptr;

    kmeans_result = kmeans_algorithm(sample.get(), centers.get(), 0.1, 100, true, &metric);
    ASSERT_NE(nullptr, kmeans_result);

    delete kmeans_result;
}