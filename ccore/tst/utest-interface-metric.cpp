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
