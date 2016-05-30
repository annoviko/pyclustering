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

#ifndef _KMEANS_H_
#define _KMEANS_H_


#include <vector>

#include "cluster/cluster_algorithm.hpp"
#include "cluster/kmeans_data.hpp"


namespace cluster_analysis {


/**
*
* @brief    Represents K-Means clustering algorithm for cluster analysis.
* @details  The algorithm related to partitional class when input data is divided into groups.
*
*/
class kmeans : public cluster_algorithm {
private:
    double          m_tolerance;

    dataset         m_initial_centers;

    kmeans_data     * m_ptr_result;   /* temporary pointer to output result */

    const dataset   * m_ptr_data;     /* used only during processing */

public:
    /**
    *
    * @brief    Default constructor of clustering algorithm.
    *
    */
    kmeans(void);

    /**
    *
    * @brief    Constructor of clustering algorithm where algorithm parameters for processing are
    *           specified.
    *
    * @param[in] p_initial_centers: initial centers that are used for processing.
    * @param[in] p_tolerance: stop condition in following way: when maximum value of distance change of
    *             cluster centers is less than tolerance than algorithm will stop processing.
    *
    */
    kmeans(const dataset & p_initial_centers, const double p_tolerance);

    /**
    *
    * @brief    Default destructor of the algorithm.
    *
    */
    ~kmeans(void);

public:
    /**
    *
    * @brief    Performs cluster analysis of an input data.
    *
    * @param[in]  p_data: input data for cluster analysis.
    * @param[out] p_result: clustering result of an input data.
    *
    */
    void process(const dataset & data, cluster_data & output_result);

private:
    void update_clusters(const dataset & centers, cluster_sequence & clusters);

    double update_centers(const cluster_sequence & clusters, dataset & centers);

    /**
    *
    * @brief    Erases clusters that do not have any points.
    *
    * @param[in|out] p_clusters: clusters that should be analyzed and modified.
    *
    */
    void erase_empty_clusters(cluster_sequence & p_clusters);
};


}


#endif
