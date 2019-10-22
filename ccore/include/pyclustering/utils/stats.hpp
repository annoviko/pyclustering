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


#include <algorithm>
#include <cmath>
#include <iterator>
#include <vector>

#include <pyclustering/utils/math.hpp>


namespace pyclustering {

namespace utils {

namespace stats {


const double        SQRT_0_5 = 0.70710678118654752440084436210485;


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

    return result / p_container.size();
}


/**
 *
 * @brief   Calculates correct variance deviation (degree of freedom = 1).
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

    result /= (p_container.size() - 1);
    return result;
}


/**
 *
 * @brief   Calculates correct variance deviation (degree of freedom = 1).
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
 * @brief   Calculates correct standard deviation (degree of freedom = 1).
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
 * @brief   Calculates correct standard deviation (degree of freedom = 1).
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
 * @param[in] p_data: data to calculate probability distribution function.
 *
 * @return  Probability distribution function.
 *
 */
template <class TypeContainer>
std::vector<double> pdf(const TypeContainer & p_data) {
    double m = 1.0 / std::sqrt(2.0 * pyclustering::utils::math::pi);

    std::vector<double> result;
    result.reserve(p_data.size());

    for (auto & value : p_data) {
        result.push_back(m * std::exp(-0.5 * std::pow(value, 2)));
    }

    return result;
}


/**
 *
 * @brief   Calculates CDF (Cumulative Distribution Function) for Gaussian (normal) distribution.
 *
 * @param[in] p_data: data to calculate probability distribution function.
 *
 * @return  Cumulative distribution function.
 *
 */
template <class TypeContainer>
std::vector<double> cdf(const TypeContainer & p_data) {
    std::vector<double> result;
    result.reserve(p_data.size());

    for (auto & value : p_data) {
        result.push_back(0.5 * std::erfc(-value * SQRT_0_5));
    }

    return result;
}



/**
 *
 * @brief   Calculates Anderson-Darling test value for Gaussian distribution.
 *
 * @param[in] p_data: data to test against Gaussian distribution.
 *
 * @return  Anderson-Darling test value.
 *
 */
template <class TypeContainer>
double anderson(const TypeContainer & p_data) {
    const double m = mean(p_data);
    const double v = pyclustering::utils::stats::std(p_data, m);

    TypeContainer sample = p_data;
    for (auto & value : sample) {
        value = (value - m) / v;
    }

    std::sort(std::begin(sample), std::end(sample));

    const auto y = cdf(sample);

    double s = 0.0;
    std::size_t n = p_data.size();

    for (std::size_t i = 0; i < n; ++i) {
        const double k = 2.0 * (i + 1.0) - 1.0;
        s += k * (std::log(y[i]) + std::log(1.0 - y[n - i - 1]));
    }

    s /= n;
    return -s - n;
}



/**
 *
 * @brief   Calculates critical values for data with Gaussian distribution for the following 
 *           significance levels: 15%, 10%, 5%, 2.5%, 1%.
 *
 * @param[in] p_data_size: Data size for that critical values should be calculated.
 *
 * @return  Calculates critical values.
 *
 */
std::vector<double> critical_values(const std::size_t p_data_size);



}

}

}