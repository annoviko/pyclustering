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

#include <pyclustering/utils/algorithm.hpp>


using namespace pyclustering::utils::algorithm;


TEST(utest_algorithm, find_left_element_valid_input) {
    std::vector<int> values = { 0, 0, 1, 1, 1, 2, 2, 2, 2, 3, 3, 3, 4 };
    std::vector<int> answer = { 0, 0, 2, 2, 2, 5, 5, 5, 5, 9, 9, 9, 12 };

    for (std::size_t i = 0; i < values.size(); i++) {
        auto iter = find_left_element(values.begin(), values.begin() + i + 1);

        auto actual_index = std::distance(values.begin(), iter);
        auto expected_index = answer[i];

        ASSERT_EQ(expected_index, actual_index);
    }
}

TEST(utest_algorithm, find_left_element_invalid_input) {
    std::vector<int> values = { 0, 0, 1, 1, 1, 2, 2, 2, 2, 3, 3, 3, 4 };
    auto iter = find_left_element(values.begin(), values.begin());
    ASSERT_EQ(values.begin(), iter);
}