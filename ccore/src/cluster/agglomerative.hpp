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

#ifndef _AGGLOMERATIVE_HPP_
#define _AGGLOMERATIVE_HPP_


#include <vector>

#include "cluster/cluster_algorithm.hpp"

#include "definitions.hpp"


namespace cluster_analysis {


using agglomerative_data = cluster_data;


/**
*
* @brief    Types of links that are used for connecting clusters.
*
*/
enum class type_link {
    SINGLE_LINK     = 0,
    COMPLETE_LINK   = 1,
    AVERAGE_LINK    = 2,
    CENTROID_LINK   = 3
};


/**
*
* @brief    Agglomerative algorithm implementation that is used bottom up approach for clustering.
* @details  The algorithm related to hierarchical class.
*
*/
class agglomerative : public cluster_algorithm {
private:
    size_t                  m_number_clusters;

    type_link               m_similarity;

    dataset                 m_centers;

    cluster_sequence        * m_ptr_clusters;

    const dataset           * m_ptr_data;

public:
    /**
    *
    * @brief    Default constructor of clustering algorithm.
    *
    */
    agglomerative(void);

    /**
    *
    * @brief    Constructor of clustering algorithm where algorithm parameters for processing are
    *           specified.
    *
    * @param[in] number_clusters: amount of clusters that should be allocated.
    * @param[in] link: type of linking clustering during processing.
    *
    */
    agglomerative(const size_t number_clusters, const type_link link);

    /**
    *
    * @brief    Default destructor of the algorithm.
    *
    */
    ~agglomerative(void);

public:
    /**
    *
    * @brief    Performs cluster analysis of an input data.
    *
    * @param[in]  p_data: input data for cluster analysis.
    * @param[out] p_result: clustering result of an input data.
    *
    */
     void process(const dataset & data, cluster_data & result);

private:
    /**
    *
    * @brief    Merges the most similar clusters in line with link type.
    *
    */
    void merge_similar_clusters(void);

    /**
    *
    * @brief    Merges the most similar clusters in line with average link type.
    *
    */
    void merge_by_average_link(void);

    /**
    *
    * @brief    Merges the most similar clusters in line with centroid link type.
    *
    */
    void merge_by_centroid_link(void);

    /**
    *
    * @brief    Merges the most similar clusters in line with complete link type.
    *
    */
    void merge_by_complete_link(void);

    /**
    *
    * @brief    Merges the most similar clusters in line with single link type.
    *
    */
    void merge_by_signle_link(void);

    /**
    *
    * @brief    Calculates new center.
    *
    * @param[in] cluster: cluster whose center should be calculated.
    * @param[out] center: coordinates of the cluster center.
    *
    */
    void calculate_center(const cluster & cluster, point & center);
};


}

#endif
