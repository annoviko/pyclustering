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
 * @brief   BSAS result is returned by pyclustering_package that consist sub-packages and this enumerator provides
 *           named indexes for sub-packages.
 *
 */
enum bsas_package_indexer {
    BSAS_PACKAGE_INDEX_CLUSTERS = 0,
    BSAS_PACKAGE_INDEX_REPRESENTATIVES,
    BSAS_PACKAGE_SIZE
};


/**
 *
 * @brief   Clustering algorithm BSAS returns allocated clusters.
 * @details Caller should destroy returned result that is in 'pyclustering_package'.
 *
 * @param[in] p_sample: input data for clustering.
 * @param[in] p_amount: maximum allowable number of clusters that can be allocated during processing.
 * @param[in] p_threshold: threshold of dissimilarity (maximum distance) between points.
 * @param[in] p_metric: pointer to distance metric 'distance_metric' that is used for distance calculation between two points.
 *
 * @return  Returns result of clustering - array of allocated clusters in pyclustering package.
 *
 */
extern "C" DECLARATION pyclustering_package * bsas_algorithm(const pyclustering_package * const p_sample,
                                                             const std::size_t p_amount,
                                                             const double p_threshold,
                                                             const void * const p_metric);