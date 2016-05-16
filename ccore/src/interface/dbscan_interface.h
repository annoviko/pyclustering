/**
*
* Copyright (C) 2014-2016    Andrei Novikov (pyclustering@yandex.ru)
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

#ifndef SRC_INTERFACE_DBSCAN_INTERFACE_H_
#define SRC_INTERFACE_DBSCAN_INTERFACE_H_


#include "interface/pyclustering_package.hpp"

#include "definitions.hpp"
#include "utils.hpp"


/**
 *
 * @brief   Clustering algorithm DBSCAN returns allocated clusters and noise that are consisted
 *          from input data.
 * @details Caller should destroy returned result in 'pyclustering_package'.
 *
 * @param[in] p_sample: input data for clustering.
 * @param[in] p_radius: connectivity radius between points, points may be connected if distance
 *             between them less then the radius.
 * @param[in] p_minumum_neighbors: minimum number of shared neighbors that is required for
 *             establish links between points.
 *
 * @return  Returns result of clustering - array of allocated clusters. The last cluster in the
 *          array is noise.
 *
 */
extern "C" DECLARATION pyclustering_package * dbscan_algorithm(const data_representation * const p_sample, const double p_radius, const size_t p_minumum_neighbors);


#endif
