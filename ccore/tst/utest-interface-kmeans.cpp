/**
*
* Copyright (C) 2014-2018    Andrei Novikov (pyclustering@yandex.ru)
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

#include "gtest/gtest.h"

#include "interface/kmeans_interface.h"
#include "interface/pyclustering_package.hpp"

#include "utils/metric.hpp"

#include "utenv_utils.hpp"

#include <memory>


using namespace ccore::utils::metric;


TEST(utest_interface_kmeans, kmeans_api) {
    std::shared_ptr<pyclustering_package> sample = pack(dataset({ { 1 }, { 2 }, { 3 }, { 10 }, { 11 }, { 12 } }));
    std::shared_ptr<pyclustering_package> centers = pack(dataset({ { 1 }, { 10 } }));

    distance_metric<point> metric = distance_metric_factory<point>::euclidean_square();

    pyclustering_package * kmeans_result = kmeans_algorithm(sample.get(), centers.get(), 0.1, false, &metric);
    ASSERT_NE(nullptr, kmeans_result);

    delete kmeans_result;
    kmeans_result = nullptr;

    kmeans_result = kmeans_algorithm(sample.get(), centers.get(), 0.1, true, &metric);
    ASSERT_NE(nullptr, kmeans_result);

    delete kmeans_result;
}