/*!

@authors Andrei Novikov (pyclustering@yandex.ru)
@date 2014-2020
@copyright BSD-3-Clause

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