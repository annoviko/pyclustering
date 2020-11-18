/*!

@authors Andrei Novikov (pyclustering@yandex.ru)
@date 2014-2020
@copyright BSD-3-Clause

*/

#pragma once


#include <iterator>


namespace pyclustering {

namespace utils {

namespace algorithm {


/*!

@brief Returns the element at the left side from the right border with the same value as the 
        last element in the range `[p_begin, p_end)`.
@details The element at the right is considered as target to search. `[p_begin, p_end)` must 
         be sorted collection. `InputIt` must meet the requirements of `LegacyInputIterator` 
         and `LegacyRandomAccessIterator`. The complexity of the algorithm is `O(log(n))`. The 
         algorithm is based on the binary search algorithm.

@param[in] p_begin: iterator pointing to the first element.
@param[in] p_end: iterator pointing to the end of the range.
@param[in] p_comparator: comparison function object which returns `true` if the first argument
            is less than the second. The signature of the compare function should be equivalent
            to the following: `bool comparator(const Type & p_val1, const Type & p_val2)`.

@return The element at the left side from the right border with the same value as the 
         last element in the range `[p_begin, p_end)`.

*/
template <class InputIt, class Comparator>
InputIt find_left_element(const InputIt p_begin, const InputIt p_end, Comparator p_comparator) {
    if (p_begin == p_end) {
        return p_end;
    }

    InputIt left = p_begin, right = p_end - 1;
    InputIt middle = p_begin + (std::distance(left, right) / 2);
    auto target = *right;

    while (left < right) {
        if (p_comparator(*middle, target)) {
            left = middle + 1;
        }
        else {
            right = middle;
        }

        const auto offset = std::distance(left, right) / 2;
        middle = left + offset;
    }

    return left;
}


/*!

@brief Returns the element at the left side from the right border with the same value as the 
        last element in the range `[p_begin, p_end)`.
@details The element at the right is considered as target to search. `[p_begin, p_end)` must 
         be sorted collection. `InputIt` must meet the requirements of `LegacyInputIterator` 
         and `LegacyRandomAccessIterator`. The complexity of the algorithm is `O(log(n))`. The 
         algorithm is based on the binary search algorithm.

@param[in] p_begin: iterator pointing to the first element.
@param[in] p_end: iterator pointing to the end of the range.

@return The element at the left side from the right border with the same value as the 
         last element in the range `[p_begin, p_end)`.

@code
    #include <iterator>
    #include <vector>
    #include <iostream>

    #include <pyclustering/utils/algorithm.hpp>

    using namespace pyclustering::utils::algorithm;

    int main() {
        std::vector<int> seq = { 1, 2, 2, 3, 3, 3, 6, 6, 6 };

        for (auto iter = seq.begin() + 1; iter != seq.end(); iter++) {
            auto left = find_left_element(seq.begin(), iter);
            std::cout << "Index of the left element: " << std::distance(seq.begin(), left)
                << " for " << *iter << std::endl;
        }

        return 0;
    }
@endcode

*/
template <class InputIt>
InputIt find_left_element(const InputIt p_begin, const InputIt p_end) {
    using iter_type = typename std::iterator_traits<InputIt>::value_type;

    return find_left_element(p_begin, p_end, [](iter_type & p_val1, iter_type & p_val2) {
        return p_val1 < p_val2;
    });
}


}

}

}