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


#include <cmath>
#include <algorithm>

#include <pyclustering/container/kdtree.hpp>

#include <pyclustering/cluster/cluster_algorithm.hpp>
#include <pyclustering/cluster/dbscan_data.hpp>


namespace pyclustering {

namespace clst {


enum class dbscan_data_t {
    POINTS,
    DISTANCE_MATRIX
};


/**
*
* @brief    Represents DBSCAN clustering algorithm for cluster analysis.
* @details  The algorithm related to density-based class.
*
*/
class dbscan {
private:
    const dataset       * m_data_ptr      = nullptr;       /* temporary pointer to input data that is used only during processing */

    dbscan_data         * m_result_ptr    = nullptr;       /* temporary pointer to clustering result that is used only during processing */

    std::vector<bool>   m_visited         = { };

    std::vector<bool>   m_belong          = { };

    double              m_initial_radius  = 0.0;    /* original radius that was specified by user */

    size_t              m_neighbors       = 0;

    dbscan_data_t       m_type            = dbscan_data_t::POINTS;

    container::kdtree   m_kdtree          = container::kdtree();

public:
    /**
    *
    * @brief    Default constructor of clustering algorithm.
    *
    */
    dbscan() = default;

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
    virtual ~dbscan() = default;

public:
    /**
    *
    * @brief    Performs cluster analysis of an input data.
    *
    * @param[in]  p_data: input data (points) for cluster analysis.
    * @param[out] p_result: clustering result of an input data.
    *
    */
    virtual void process(const dataset & p_data, cluster_data & p_result);

    /**
    *
    * @brief    Performs cluster analysis of an input data of specific type.
    *
    * @param[in]  p_data: input data for cluster analysis.
    * @param[in]  p_type: type of an input data that should be processed.
    * @param[out] p_result: clustering result of an input data.
    *
    */
    virtual void process(const dataset & p_data, const dbscan_data_t p_type, cluster_data & p_result);

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

    void get_neighbors_from_points(const size_t p_index, std::vector<size_t> & p_neighbors);

    void get_neighbors_from_distance_matrix(const size_t p_index, std::vector<size_t> & p_neighbors);

    void create_kdtree(const dataset & p_data);

    void expand_cluster(const std::size_t p_index, cluster & allocated_cluster);
};


}

}