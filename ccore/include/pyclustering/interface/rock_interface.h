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
 * @brief   Clustering algorithm ROCK returns allocated clusters.
 * @details Caller should destroy returned result in 'pyclustering_package'.
 *
 * @param[in] p_sample: input data for clustering.
 * @param[in] p_radius: connectivity radius (similarity threshold).
 * @param[in] p_number_clusters: defines number of clusters that should be allocated from the input data set.
 * @param[in] p_threshold: value that defines degree of normalization that influences
 *             on choice of clusters for merging during processing.
 *
 * @return  Returns result of clustering - array of allocated clusters in the pyclustering package.
 *
 */
extern "C" DECLARATION pyclustering_package * rock_algorithm(const pyclustering_package * const p_sample, const double p_radius, const size_t p_number_clusters, const double p_threshold);
