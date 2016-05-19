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

#ifndef SRC_INTERFACE_ROCK_INTERFACE_H_
#define SRC_INTERFACE_ROCK_INTERFACE_H_


#include "interface/pyclustering_package.hpp"

#include "definitions.hpp"
#include "utils.hpp"


/**
 *
 * @brief   Clustering algorithm ROCK returns allocated clusters.
 * @details Caller should destroy returned result in 'pyclustering_package'.
 *
 * @param[in] sample: input data for clustering.
 * @param[in] radius: connectivity radius (similarity threshold).
 * @param[in] number_clusters: defines number of clusters that should be allocated from the input data set.
 * @param[in] threshold: value that defines degree of normalization that influences
 *             on choice of clusters for merging during processing.
 *
 * @return  Returns result of clustering - array of allocated clusters in the pyclustering package.
 *
 */
extern "C" DECLARATION pyclustering_package * rock_algorithm(const data_representation * const sample, const double radius, const size_t number_clusters, const double threshold);


#endif
