/*!

@authors Andrei Novikov (pyclustering@yandex.ru)
@date 2014-2020
@copyright GNU Public License

@cond GNU_PUBLIC_LICENSE
    pyclustering is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    pyclustering is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
@endcond

*/


#include <gtest/gtest.h>

#include <pyclustering/parallel/parallel.hpp>

#include <numeric>


using namespace pyclustering::parallel;


static void template_parallel_square(const std::size_t p_length, const std::size_t p_step = 1) {
    std::vector<double> values(p_length);
    std::iota(values.begin(), values.end(), 0);

    std::vector<double> results(p_length);
    parallel_for(std::size_t(0), values.size(), p_step, [&values, &results](const std::size_t p_index) {
        results[p_index] = values[p_index] * values[p_index];
    });

    for (std::size_t i = 0; i < p_length; i += p_step) {
        ASSERT_EQ(values[i] * values[i], results[i]);
    }
}


TEST(utest_parallel_for, square_1_element) {
    template_parallel_square(1);
}


TEST(utest_parallel_for, square_3_element) {
    template_parallel_square(3);
}


TEST(utest_parallel_for, square_10_elements) {
    template_parallel_square(10);
}


TEST(utest_parallel_for, square_elements_step_increase) {
    for (std::size_t i = 0; i < 50; i++) {
        template_parallel_square(i);
    }
}


TEST(utest_parallel_for, square_10000_elements) {
    template_parallel_square(10000);
}


TEST(utest_parallel_for, square_10_elements_step_2) {
    template_parallel_square(10, 2);
}


TEST(utest_parallel_for, square_10_elements_step_3) {
    template_parallel_square(10, 3);
}


TEST(utest_parallel_for, square_20_elements_step_2) {
    template_parallel_square(20, 2);
}


TEST(utest_parallel_for, square_20_elements_step_3) {
    template_parallel_square(20, 3);
}


TEST(utest_parallel_for, square_20_elements_step_4) {
    template_parallel_square(20, 4);
}


TEST(utest_parallel_for, square_100_elements_step_2) {
    template_parallel_square(100, 2);
}


TEST(utest_parallel_for, square_100_elements_step_3) {
    template_parallel_square(100, 3);
}


TEST(utest_parallel_for, square_100_elements_step_5) {
    template_parallel_square(100, 5);
}


TEST(utest_parallel_for, square_100_elements_step_10) {
    template_parallel_square(100, 10);
}


TEST(utest_parallel_for, square_1000_elements_step_13) {
    template_parallel_square(1000, 13);
}


TEST(utest_parallel_for, square_100_elements_step_increase) {
    for (std::size_t i = 1; i < 100; i++) {     /* go over the limit as well */
        template_parallel_square(100, i);
    }
}


static void template_parallel_square_negative_step(const std::size_t p_length, const int p_step = -1) {
    std::vector<double> values(p_length);
    std::iota(values.begin(), values.end(), 0);

    std::vector<double> results(p_length);
    parallel_for((int) values.size() - 1, (int) 0, p_step, [&values, &results](const int p_index) {
        results[p_index] = values[p_index] * values[p_index];
    });

    for (std::size_t i = 0; i < p_length; i += p_step) {
        ASSERT_EQ(values[i] * values[i], results[i]);
    }
}


TEST(utest_parallel_for, square_10_elements_negative_step) {
    template_parallel_square_negative_step(10);
}


TEST(utest_parallel_for, square_10_elements_negative_step_2) {
    template_parallel_square_negative_step(10, -2);
}


TEST(utest_parallel_for, square_10_elements_negative_step_3) {
    template_parallel_square_negative_step(10, -3);
}


TEST(utest_parallel_for, square_100_elements_negative_step) {
    template_parallel_square_negative_step(100);
}


TEST(utest_parallel_for, square_100_elements_negative_step_2) {
    template_parallel_square_negative_step(100, -2);
}


TEST(utest_parallel_for, square_100_elements_negative_step_3) {
    template_parallel_square_negative_step(100, -3);
}


TEST(utest_parallel_for, square_100_elements_negative_step_4) {
    template_parallel_square_negative_step(100, -4);
}


TEST(utest_parallel_for, square_100_elements_negative_step_5) {
    template_parallel_square_negative_step(100, -5);
}
