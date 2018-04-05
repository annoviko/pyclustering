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

#include "definitions.hpp"

#include "utils/metric.hpp"

#include "utenv_check.hpp"


TEST(utest_metric, calculate_distance_matrix_01) {
    dataset points = { {0}, {2}, {4} };
    dataset distance_matrix;

    ccore::utils::metric::distance_matrix(points, distance_matrix);

    dataset distance_matrix_expected = { { 0.0, 2.0, 4.0 }, { 2.0, 0.0, 2.0 }, { 4.0, 2.0, 0.0 } };

    ASSERT_EQ(distance_matrix, distance_matrix_expected);
}