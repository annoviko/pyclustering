/*!

@authors Andrei Novikov (pyclustering@yandex.ru)
@date 2014-2020
@copyright BSD-3-Clause

*/

#include <gtest/gtest.h>

#include <pyclustering/interface/xmeans_interface.h>
#include <pyclustering/interface/pyclustering_package.hpp>

#include <pyclustering/utils/metric.hpp>

#include "utenv_utils.hpp"

#include <memory>


using namespace pyclustering;
using namespace pyclustering::utils::metric;


TEST(utest_interface_xmeans, xmeans_algorithm) {
    std::shared_ptr<pyclustering_package> sample = pack(dataset({ { 1 }, { 2 }, { 3 }, { 10 }, { 11 }, { 12 } }));
    std::shared_ptr<pyclustering_package> centers = pack(dataset({ { 1 }, { 2 } }));

    distance_metric<point> metric = distance_metric_factory<point>::euclidean_square();
    pyclustering_package * result = xmeans_algorithm(sample.get(), centers.get(), 5, 0.01, 0, 0.9, 0.9, 1, -1, &metric);
    ASSERT_EQ(3U, result->size);

    pyclustering_package * obtained_clusters = ((pyclustering_package **) result->data)[0];
    ASSERT_EQ(2U, obtained_clusters->size);

    pyclustering_package * obtained_centers = ((pyclustering_package **) result->data)[1];
    ASSERT_EQ(2U, obtained_centers->size);

    double obtained_wce = ((double *) result->data)[0];
    ASSERT_GE(obtained_wce, 0.0);

    delete result;
}
