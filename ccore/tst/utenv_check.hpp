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


#include <algorithm>
#include <vector>

#include "gtest/gtest.h"

#include "cluster/cluster_data.hpp"
#include "cluster/cluster_algorithm.hpp"


using namespace ccore::clst;


/**
*
* @brief    Checks that clusters have all allocated objects together from input data and that
*           sizes of allocated clusters are expected.
* @details  If 'p_expected_cluster_length' is empty than only total number of allocated object
*           is checked - clusters consist of each point index from input data.
*
* @param[in] p_data: data that has been processed.
* @param[in] p_actual_clusters: allocated clusters.
* @param[in] p_expected_cluster_length: expected clusters length - can be empty.
* @param[in] p_indexes: specific object indexes that are used for clustering.
*
*/
void ASSERT_CLUSTER_SIZES(const dataset & p_data,
        const cluster_sequence & p_actual_clusters,
        const std::vector<size_t> & p_expected_cluster_length,
        const index_sequence & p_indexes = { });


template <typename EnsemblesType>
bool COMPARE_SYNC_ENSEMBLES(EnsemblesType & p_ensembles,
                            EnsemblesType & p_expected_ensembles,
                            typename EnsemblesType::value_type & p_dead,
                            typename EnsemblesType::value_type & p_expected_dead)
{
    /* compare dead neurons */
    std::sort(p_dead.begin(), p_dead.end());
    std::sort(p_expected_dead.begin(), p_expected_dead.end());

    if (p_expected_dead != p_dead) {
        return false;
    }


    /* compare ensembles */
    if (p_expected_ensembles.size() != p_ensembles.size()) {
        return false;
    }

    /* sort indexes in ensembles */
    for (auto & ensemble : p_ensembles) {
        std::sort(ensemble.begin(), ensemble.end());
    }

    for (auto & ensemble : p_expected_ensembles) {
        std::sort(ensemble.begin(), ensemble.end());
    }

    /* compare */
    bool ensemble_found = false;
    for (auto & ensemble : p_ensembles) {
        for (auto & expected_ensemble : p_expected_ensembles) {
            if (ensemble == expected_ensemble) {
                ensemble_found = true;
                break;
            }
        }

        if (!ensemble_found) {
            return false;
        }
    }

    return true;
}


template <typename EnsemblesType>
void ASSERT_SYNC_ENSEMBLES(EnsemblesType & p_ensembles,
                           EnsemblesType & p_expected_ensembles,
                           typename EnsemblesType::value_type & p_dead,
                           typename EnsemblesType::value_type & p_expected_dead)
{
    ASSERT_TRUE(COMPARE_SYNC_ENSEMBLES(p_ensembles, p_expected_ensembles, p_dead, p_expected_dead));
}