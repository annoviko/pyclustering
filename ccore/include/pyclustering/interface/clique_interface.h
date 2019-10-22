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
 * @brief   CLIQUE result is returned by pyclustering_package that consist sub-packages and this enumerator provides
 *           named indexes for sub-packages.
 *
 */
enum clique_package_indexer {
    CLIQUE_PACKAGE_INDEX_CLUSTERS = 0,
    CLIQUE_PACKAGE_INDEX_NOISE,
    CLIQUE_PACKAGE_INDEX_LOGICAL_LOCATION,
    CLIQUE_PACKAGE_INDEX_MAX_CORNER,
    CLIQUE_PACKAGE_INDEX_MIN_CORNER,
    CLIQUE_PACKAGE_INDEX_BLOCK_POINTS,
    CLIQUE_PACKAGE_SIZE
};


/**
 *
 * @brief   Clustering algorithm CLIQUE returns allocated clusters.
 * @details Caller should destroy returned clustering data using 'cure_data_destroy' when
 *           it is not required anymore.
 *
 * @param[in] p_sample: input data for clustering.
 * @param[in] p_intervals: amount of intervals in each dimension.
 * @param[in] p_threshold: minimum number of objects that should be contained by non-noise block.
 *
 * @return  Returns pointer to cure data - clustering result that can be used for obtaining
 *           allocated clusters, representative points and means of each cluster.
 *
 */
extern "C" DECLARATION pyclustering_package * clique_algorithm(const pyclustering_package * const p_sample, const std::size_t p_intervals, const std::size_t p_threshold);