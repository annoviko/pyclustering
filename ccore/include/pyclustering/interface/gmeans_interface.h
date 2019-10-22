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


#include <pyclustering/interface/pyclustering_package.hpp>

#include <pyclustering/definitions.hpp>


/**
 *
 * @brief   G-Means result is returned by pyclustering_package that consist sub-packages and this enumerator provides
 *           named indexes for sub-packages.
 *
 */
enum gmeans_package_indexer {
    GMEANS_PACKAGE_INDEX_CLUSTERS = 0,
    GMEANS_PACKAGE_INDEX_CENTERS,
    GMEANS_PACKAGE_INDEX_WCE,
    GMEANS_PACKAGE_SIZE
};


/**
 *
 * @brief   Clustering algorithm G-Means returns allocated clusters.
 * @details Caller should destroy returned result in 'pyclustering_package'.
 *
 * @param[in] p_sample: input data for clustering.
 * @param[in] p_amount: initial amount of centers.
 * @param[in] p_tolerance: stop condition - when changes of medians are less then tolerance value.
 * @param[in] p_repeat: how many times K-Means should be run to improve parameters, with larger 'repeat' 
 *             values suggesting higher probability of finding global optimum.
 *
 * @return  Returns result of clustering - array of allocated clusters.
 *
 */
extern "C" DECLARATION pyclustering_package * gmeans_algorithm(const pyclustering_package * const p_sample, 
                                                               const std::size_t p_amount, 
                                                               const double p_tolerance,
                                                               const std::size_t p_repeat);
