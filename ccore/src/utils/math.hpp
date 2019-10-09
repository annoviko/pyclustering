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


namespace pyclustering {

namespace utils {

namespace math {


/**
 *
 * @brief   Mathematical constant pi.
 *
 */
const double pi = 3.14159265358979323846;


/**
 *
 * @brief   Calculates Heaviside function.
 * @details If value >= 0.0 then 1.0 is returned, otherwise 0.0 is returned.
 *
 * @param[in] value: Input argument of the Heaviside function.
 *
 * @return  Returns result of Heaviside function.
 *
 */
double heaviside(const double value);


/**
 *
 * @brief   Calculates absolute difference between two objects.
 *
 * @param[in] p_value1: The first value of the operation.
 * @param[in] p_value2: The second value of the operation.
 *
 * @return  Returns absolute difference.
 *
 */
template <class TypeValue>
TypeValue absolute_difference(const TypeValue & p_value1, const TypeValue & p_value2) {
    return (p_value1 >= p_value2) ? p_value1 - p_value2 : p_value2 - p_value1;
}


}

}

}