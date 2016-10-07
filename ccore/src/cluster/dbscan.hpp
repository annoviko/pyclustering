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

#ifndef _DBSCAN_H_
#define _DBSCAN_H_


#include <cmath>
#include <algorithm>

#include "cluster/cluster_algorithm.hpp"
#include "cluster/dbscan_data.hpp"


namespace cluster_analysis {


/**
*
* @brief    Represents DBSCAN clustering algorithm for cluster analysis.
* @details  The algorithm related to density-based class.
*
*/
class dbscan {
private:
    const dataset       * m_data_ptr;         /* temporary pointer to input data that is used only during processing */

    dbscan_data         * m_result_ptr;       /* temporary pointer to clustering result that is used only during processing */

    std::vector<bool>   m_visited;

    std::vector<bool>   m_belong;

    double              m_radius;

    size_t              m_neighbors;

public:
    /**
    *
    * @brief    Default constructor of clustering algorithm.
    *
    */
    dbscan(void);

    /**
    *
    * @brief    Constructor of clustering algorithm where algorithm parameters for processing are
    *           specified.
    *
    * @param[in] p_radius_connectivity: connectivity radius between objects.
    * @param[in] p_minimum_neighbors: minimum amount of shared neighbors that is require to connect
    *             two object (if distance between them is less than connectivity radius).
    *
    */
    dbscan(const double p_radius_connectivity, const size_t p_minimum_neighbors);

    /**
    *
    * @brief    Default destructor of the algorithm.
    *
    */
    virtual ~dbscan(void);

public:
    /**
    *
    * @brief    Performs cluster analysis of an input data.
    *
    * @param[in]  p_data: input data for cluster analysis.
    * @param[out] p_result: clustering result of an input data.
    *
    */
    virtual void process(const dataset & p_data, cluster_data & p_result);

private:
    /**
    *
    * @brief    Obtains neighbors of the specified node (data object).
    *
    * @param[in]  p_index: index of the node (data object).
    * @param[out] p_neighbors: neighbor indexes of the specified node (data object).
    *
    */
    void get_neighbors(const size_t p_index, std::vector<size_t> & p_neighbors);
};


}


#endif
