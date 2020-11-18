/*!

@authors Andrei Novikov (pyclustering@yandex.ru)
@date 2014-2020
@copyright BSD-3-Clause

*/

#pragma once


namespace pyclustering {

namespace utils {

namespace math {


/*!

@brief   Mathematical constant pi.

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