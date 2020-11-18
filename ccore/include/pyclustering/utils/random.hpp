/*!

@authors Andrei Novikov (pyclustering@yandex.ru)
@date 2014-2020
@copyright BSD-3-Clause

*/


#pragma once


namespace pyclustering {

namespace utils {

namespace random {


/**
 *
 * @brief   Returns random value in specified range using uniform distribution.
 *
 * @param[in] p_from: Mean.
 * @param[in] p_to:   Standard deviation.
 *
 * @return  Returns random variable.
 *
 */
double generate_uniform_random(const double p_from = 0.0, const double p_to = 1.0);


}

}

}