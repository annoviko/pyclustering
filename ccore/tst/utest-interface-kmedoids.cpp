/**
*
* Copyright (C) 2014-2017    Andrei Novikov (pyclustering@yandex.ru)
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

#include "interface/kmedoids_interface.h"
#include "interface/pyclustering_package.hpp"

#include "cluster/kmedoids.hpp"

#include "utenv-utils.hpp"

#include <memory>


TEST(utest_interface_kmedoids, kmedoids_api) {
    std::shared_ptr<pyclustering_package> sample = pack(dataset({ { 1 }, { 2 }, { 3 }, { 10 }, { 11 }, { 12 } }));
    std::shared_ptr<pyclustering_package> medoids = pack(cluster_analysis::medoid_sequence({ 2, 4 }));

    pyclustering_package * kmedoids_result = kmedoids_algorithm(sample.get(), medoids.get(), 0.1);
    ASSERT_NE(nullptr, kmedoids_result);

    delete kmedoids_result;
}