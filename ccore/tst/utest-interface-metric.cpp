/*!

@authors Andrei Novikov (pyclustering@yandex.ru)
@date 2014-2020
@copyright BSD-3-Clause

*/
#include <gtest/gtest.h>

#include <pyclustering/interface/metric_interface.h>
#include <pyclustering/interface/pyclustering_package.hpp>

#include <pyclustering/utils/metric.hpp>

#include "utenv_utils.hpp"

#include <memory>


using namespace pyclustering;
using namespace pyclustering::utils::metric;


TEST(utest_interface_metric, euclidean) {
    std::shared_ptr<pyclustering_package> arguments = pack(std::vector<double>());
    double (*p_solver)(const void *, const void *) = nullptr;

    void * metric_pointer = metric_create(metric_t::EUCLIDEAN, arguments.get(), p_solver);

    ASSERT_NE(nullptr, metric_pointer);

    std::shared_ptr<pyclustering_package> point1 = pack(point({1.0, 1.0}));
    std::shared_ptr<pyclustering_package> point2 = pack(point({2.0, 1.0}));

    double distance = metric_calculate(metric_pointer, point1.get(), point2.get());

    ASSERT_EQ(1.0, distance);

    metric_destroy(metric_pointer);
}

TEST(utest_interface_metric, gower) {
    std::shared_ptr<pyclustering_package> arguments = pack(std::vector<double>({1.0, 0.0}));
    double (*p_solver)(const void *, const void *) = nullptr;

    void * metric_pointer = metric_create(metric_t::GOWER, arguments.get(), p_solver);

    ASSERT_NE(nullptr, metric_pointer);

    std::shared_ptr<pyclustering_package> point1 = pack(point({1.0, 1.0}));
    std::shared_ptr<pyclustering_package> point2 = pack(point({2.0, 1.0}));

    double distance = metric_calculate(metric_pointer, point1.get(), point2.get());

    ASSERT_EQ(0.5, distance);

    metric_destroy(metric_pointer);
}
