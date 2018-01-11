/**
*
* Copyright (C) 2014-2018    Andrei Novikov (pyclustering@yandex.ru)
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


/**
*
* @brief   Clustering algorithm X-Means returns allocated clusters.
* @details Caller should destroy returned result in 'pyclustering_package'.
*
* @param[in] p_sample: input data for clustering.
* @param[in] p_centers: initial coordinates of centers of clusters.
* @param[in] p_kmax: maximum number of clusters that can be allocated.
* @param[in] p_tolerance: stop condition for local parameter improvement.
* @param[in] p_criterion: cluster splitting criterion.
*
* @return  Returns result of clustering - array of allocated clusters in the pyclustering package.
*
*/
extern "C" DECLARATION pyclustering_package * xmeans_algorithm(const pyclustering_package * const p_sample, const pyclustering_package * const p_centers, const std::size_t p_kmax, const double p_tolerance, const unsigned int p_criterion);
