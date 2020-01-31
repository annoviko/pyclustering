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

#include <pyclustering/interface/kmedoids_interface.h>
#include <pyclustering/interface/pyclustering_package.hpp>

#include <pyclustering/cluster/kmedoids.hpp>

#include <pyclustering/utils/metric.hpp>

#include "utenv_utils.hpp"

#include <memory>


using namespace pyclustering;
using namespace pyclustering::clst;
using namespace pyclustering::utils::metric;


TEST(utest_interface_kmedoids, kmedoids_api) {
    std::shared_ptr<pyclustering_package> sample = pack(dataset({ { 1 }, { 2 }, { 3 }, { 10 }, { 11 }, { 12 } }));
    std::shared_ptr<pyclustering_package> medoids = pack(medoid_sequence({ 2, 4 }));

    distance_metric<point> metric = distance_metric_factory<point>::euclidean_square();

    pyclustering_package * kmedoids_result = kmedoids_algorithm(sample.get(), medoids.get(), 0.001, 100, &metric, 0);
    ASSERT_NE(nullptr, kmedoids_result);

    delete kmedoids_result;
}


TEST(utest_interface_kmedoids, kmedoids_api_null_metric) {
    std::shared_ptr<pyclustering_package> sample = pack(dataset({ { 1 }, { 2 }, { 3 }, { 10 }, { 11 }, { 12 } }));
    std::shared_ptr<pyclustering_package> medoids = pack(medoid_sequence({ 2, 4 }));

    pyclustering_package * kmedoids_result = kmedoids_algorithm(sample.get(), medoids.get(), 0.001, 100, nullptr, 0);
    ASSERT_NE(nullptr, kmedoids_result);

    delete kmedoids_result;
}
