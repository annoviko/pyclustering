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

#pragma once


#include <cmath>
#include <iterator>
#include <vector>

#include "utils/math.hpp"


namespace ccore {

namespace utils {

namespace stats {


/**
 *
 * @brief   Calculates data's mean.
 *
 * @param[in] p_container: data to calculate mean.
 *
 * @return  Mean value.
 *
 */
template <class TypeContainer>
double mean(const TypeContainer & p_container) {
    double result = 0.0;
    for (const auto value : p_container) {
        result += static_cast<double>(value);
    }

    return result / std::size(p_container);
}


/**
 *
 * @brief   Calculates correct variance deviation.
 *
 * @param[in] p_container: data to calculate standard deviation.
 * @param[in] p_mean: data's mean value.
 *
 * @return  Correct standard deviation.
 *
 */
template <class TypeContainer>
double var(const TypeContainer & p_container, const double p_mean) {
    double result = 0.0;
    for (const auto value : p_container) {
        result += std::pow(value - p_mean, 2);
    }

    result /= (std::size(p_container) - 1);
    return result;
}


/**
 *
 * @brief   Calculates correct variance deviation.
 *
 * @param[in] p_container: data to calculate standard deviation.
 *
 * @return  Correct standard deviation.
 *
 */
template <class TypeContainer>
double var(const TypeContainer & p_container) {
    double mu = mean(p_container);
    return var(p_container, mu);
}



/**
 *
 * @brief   Calculates correct standard deviation.
 *
 * @param[in] p_container: data to calculate standard deviation.
 * @param[in] p_mean: data's mean value.
 *
 * @return  Correct standard deviation.
 *
 */
template <class TypeContainer>
double std(const TypeContainer & p_container, const double p_mean) {
    return std::sqrt(var(p_container, p_mean));
}


/**
 *
 * @brief   Calculates correct standard deviation.
 *
 * @param[in] p_container: data to calculate standard deviation.
 *
 * @return  Correct standard deviation.
 *
 */
template <class TypeContainer>
double std(const TypeContainer & p_container) {
    return std::sqrt(var(p_container));
}


/**
 *
 * @brief   Calculates PDF (Probability Distribution Function) for Gaussian (normal) distribution.
 *
 * @param[in] p_container: data to calculate probability distribution function.
 *
 * @return  Probability distribution function.
 *
 */
template <class TypeContainer>
std::vector<double> pdf(const TypeContainer & p_container) {
    double m = 1.0 / std::sqrt(2.0 * ccore::utils::math::pi);

    std::vector<double> result;
    result.reserve(std::size(p_container));

    for (auto & value : p_container) {
        result.push_back(m * std::exp(-0.5 * std::pow(value, 2)));
    }

    return result;
}


}

}

}