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