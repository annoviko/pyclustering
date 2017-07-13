/**
*
* Copyright (C) 2014-2017    Andrei Novikov (pyclustering@yandex.ru)
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


#include "interface/pyclustering_package.hpp"

#include "definitions.hpp"

/**
 *
 * @brief   Clustering algorithm antmean returns allocated clusters.
 * @details Caller should destroy returned clustering data using 'free_pyclustering_package' when
 *           it is not required anymore.
 *
 * @param[in] p_sample: input data for clustering.
 * @param[in] p_params: ant colony parameters for clustering.
 * @param[in] p_clusters: amount of clusters that should be allocated.
 *
 * @return  Returns pointer to pyclustering package where results (allocated clusters) are stored.
 *
 */
extern "C" DECLARATION pyclustering_package * antmean_algorithm(const pyclustering_package * const p_sample, const void * p_params, unsigned int p_clusters);
