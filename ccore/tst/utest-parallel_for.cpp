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

#include <pyclustering/parallel/parallel.hpp>

#include <numeric>


using namespace pyclustering::parallel;


static void template_parallel_square(const std::size_t p_length) {
    std::vector<double> values(p_length);
    std::iota(values.begin(), values.end(), 0);

    std::vector<double> results(p_length);
    parallel_for(std::size_t(0), values.size(), [&values, &results](const std::size_t p_index) {
        results[p_index] = values[p_index] * values[p_index];
    });

    for (std::size_t i = 0; i < p_length; i++) {
        ASSERT_EQ(values[i] * values[i], results[i]);
    }
}


TEST(utest_parallel_for, square_1_element) {
    template_parallel_square(1);
}


TEST(utest_parallel_for, square_10_elements) {
    template_parallel_square(10);
}


TEST(utest_parallel_for, square_10000_elements) {
    template_parallel_square(10000);
}