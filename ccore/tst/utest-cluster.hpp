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

#ifndef TST_UTEST_CLUSTER_HPP_
#define TST_UTEST_CLUSTER_HPP_


#include <algorithm>
#include <vector>

#include "gtest/gtest.h"

#include "cluster/cluster_data.hpp"
#include "cluster/cluster_algorithm.hpp"


using namespace cluster_analysis;


/***********************************************************************************************
*
* @brief    Checks that clusters have all allocated objects together from input data and that
*           sizes of allocated clusters are expected.
* @details  If 'p_expected_cluster_length' is empty than only total number of allocated object
*           is checked - clusters consist of each point index from input data.
*
* @param[in] p_data: data that has been processed.
* @param[in] p_actual_clusters: allocated clusters.
* @param[in] p_expected_cluster_length: expected clusters length - can be empty.
*
***********************************************************************************************/
void ASSERT_CLUSTER_SIZES(const dataset & p_data,
        const cluster_sequence & p_actual_clusters,
        const std::vector<size_t> & p_expected_cluster_length);


#endif
