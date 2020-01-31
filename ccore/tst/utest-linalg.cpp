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

#include <algorithm>

#include <pyclustering/utils/linalg.hpp>


using namespace pyclustering::utils::linalg;


TEST(utest_lingalg, subtract) {
    std::vector<double> a = { 2, 3, 4, 5 };
    std::vector<double> b = { 1, 2, 3, 4 };

    auto result = subtract(a, b);

    std::vector<double> expected = { 1, 1, 1, 1 };
    ASSERT_EQ(expected, result);
}

TEST(utest_lingalg, subtract_with_number) {
    std::vector<double> a = { 2, 4, 6, 8 };

    auto result = subtract(a, 2);

    std::vector<double> expected = { 0, 2, 4, 6 };
    ASSERT_EQ(expected, result);
}

TEST(utest_lingalg, multiply) {
    std::vector<double> a = { 2, 3, 4, 5 };
    std::vector<double> b = { 1, 2, 3, 4 };

    auto result = multiply(a, b);

    std::vector<double> expected = { 2, 6, 12, 20 };
    ASSERT_EQ(expected, result);
}

TEST(utest_lingalg, multiply_with_number) {
    std::vector<double> a = { 2, 3, 4, 5 };

    auto result = multiply(a, 2);

    std::vector<double> expected = { 4, 6, 8, 10 };
    ASSERT_EQ(expected, result);
}

TEST(utest_lingalg, multiply_matrix) {
    matrix a = { { 1, 1 }, { 2, 2 }, { 3, 3 } };
    std::vector<double> b = { 2, 2 };

    auto result = multiply(a, b);

    matrix expected = { { 2, 2 }, { 4, 4 }, { 6, 6 } };
    ASSERT_EQ(expected, result);
}

TEST(utest_lingalg, divide) {
    std::vector<double> a = { 2, 6, 9, 16 };
    std::vector<double> b = { 2, 2, 3, 4 };

    auto result = divide(a, b);

    std::vector<double> expected = { 1, 3, 3, 4 };
    ASSERT_EQ(expected, result);
}

TEST(utest_lingalg, divide_with_number) {
    std::vector<double> a = { 10, 20, 30, 40 };

    auto result = divide(a, 5);

    std::vector<double> expected = { 2, 4, 6, 8 };
    ASSERT_EQ(expected, result);
}

TEST(utest_linalg, sum_vector) {
    std::vector<double> a = { 1, 2, 3 };
    ASSERT_EQ(6, sum(a));
}

TEST(utest_linalg, sum_matrix) {
    matrix a = { { 1, 1 }, { 2, 2 }, { 3, 3 } };
    std::vector<double> expected = { 6, 6 };
    ASSERT_EQ(expected, sum(a, 0));

    expected = { 2, 4, 6 };
    ASSERT_EQ(expected, sum(a, 1));
}