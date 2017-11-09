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

#include "interface/xmeans_interface.h"
#include "interface/pyclustering_package.hpp"

#include "utenv-utils.hpp"

#include <memory>


TEST(utest_interface_xmeans, xmeans_algorithm) {
    std::shared_ptr<pyclustering_package> sample = pack(dataset({ { 1 }, { 2 }, { 3 }, { 10 }, { 11 }, { 12 } }));
    std::shared_ptr<pyclustering_package> centers = pack(dataset({ { 1 }, { 2 } }));

    pyclustering_package * result = xmeans_algorithm(sample.get(), centers.get(), 5, 0.01, 0);
    ASSERT_EQ(2, result->size);

    pyclustering_package * obtained_clusters = ((pyclustering_package **) result->data)[0];
    ASSERT_EQ(2, obtained_clusters->size);

    pyclustering_package * obtained_centers = ((pyclustering_package **) result->data)[1];
    ASSERT_EQ(2, obtained_centers->size);

    delete result;
}
