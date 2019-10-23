/**
*
* @authors Andrei Novikov (pyclustering@yandex.ru)
* @date 2014-2019
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


#include <pyclustering/utils/linalg.hpp>

#include <functional>
#include <numeric>
#include <sstream>


namespace pyclustering {

namespace utils {

namespace linalg {


static sequence action_for_each_component(const sequence & a, 
                                          const sequence & b,
                                          const std::function<double(double, double)> && func)
{
    if (a.size() != b.size()) {
        throw std::invalid_argument("Both vectors should have the same size.");
    }

    sequence result(a.size(), 0.0);
    for (std::size_t i = 0; i < result.size(); i++) {
        result[i] = func(a[i], b[i]);
    }
    return result;
}


static sequence action_for_each_component(const sequence & a, 
                                          const double b,
                                          const std::function<double(double, double)> && func)
{
    sequence result(a.size(), 0.0);
    for (std::size_t i = 0; i < result.size(); i++) {
        result[i] = func(a[i], b);
    }
    return result;
}


sequence subtract(const sequence & a, const sequence & b) {
    return action_for_each_component(a, b, [](double v1, double v2) { return v1 - v2; });
}


sequence subtract(const sequence & a, const double b) {
    return action_for_each_component(a, b, [](double v1, double v2) { return v1 - v2; });
}


sequence multiply(const sequence & a, const sequence & b) {
    return action_for_each_component(a, b, [](double v1, double v2) { return v1 * v2; });
}


sequence multiply(const sequence & a, const double b) {
    return action_for_each_component(a, b, [](double v1, double v2) { return v1 * v2; });
}


matrix multiply(const matrix & a, const sequence & b) {
    if (a.empty()) {
        throw std::invalid_argument("Matrix is empty.");
    }

    if (a.begin()->size() != b.size()) {
        std::stringstream stream;
        stream << "Matrix vector (" << a.begin()->size() << ") and vector (" << b.size() << ") should have the same size.";
        throw std::invalid_argument(stream.str());
    }

    matrix result;
    result.reserve(a.size());

    for (const auto & v : a) {
        result.push_back(action_for_each_component(v, b, [](double v1, double v2) { return v1 * v2; }));
    }
    return result;
}


sequence divide(const sequence & a, const sequence & b) {
    return action_for_each_component(a, b, [](double v1, double v2) { return v1 / v2; });
}


sequence divide(const sequence & a, const double b) {
    return action_for_each_component(a, b, [](double v1, double v2) { return v1 / v2; });
}


double sum(const sequence & a) {
    return std::accumulate(std::begin(a), std::end(a), 0.0);
}


sequence sum(const matrix & a, std::size_t axis) {
    if (a.empty()) {
        throw std::invalid_argument("Matrix is empty.");
    }

    if (axis == 0) {
        sequence result(a.begin()->size(), 0.0);
        for (std::size_t col = 0; col < a.begin()->size(); col++) {
            for (std::size_t row = 0; row < a.size(); row++) {
                result[col] += a[row][col];
            }
        }

        return result;
    }
    else if (axis == 1) {
        sequence result(a.size(), 0.0);
        for (std::size_t row = 0; row < a.size(); row++) {
            result[row] = std::move(sum(a[row]));
        }

        return result;
    }
    else {
        throw std::invalid_argument("Axis is out of matrix's dimension.");
    }
}



}

}

}