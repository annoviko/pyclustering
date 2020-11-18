/*!

@authors Andrei Novikov (pyclustering@yandex.ru)
@date 2014-2020
@copyright BSD-3-Clause

*/

#pragma once


#include <vector>



namespace pyclustering {

namespace utils {

namespace linalg {

using sequence = std::vector<double>;
using matrix = std::vector<sequence>;


sequence subtract(const sequence & a, const sequence & b);

sequence subtract(const sequence & a, const double b);

sequence multiply(const sequence & a, const sequence & b);

sequence multiply(const sequence & a, const double b);

matrix multiply(const matrix & a, const sequence & b);

sequence divide(const sequence & a, const sequence & b);

sequence divide(const sequence & a, const double b);

double sum(const sequence & a);

sequence sum(const matrix & a, std::size_t axis = 0);

}

}

}