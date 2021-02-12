/*!

@authors Andrei Novikov (pyclustering@yandex.ru)
@date 2014-2020
@copyright BSD-3-Clause

*/

#pragma once


#include <cmath>
#include <algorithm>

#include <pyclustering/container/kdtree_balanced.hpp>

#include <pyclustering/cluster/data_type.hpp>
#include <pyclustering/cluster/dbscan_data.hpp>


namespace pyclustering {

namespace clst {


/*!

@class    dbscan dbscan.hpp pyclustering/cluster/dbscan.hpp

@brief    Represents DBSCAN clustering algorithm for cluster analysis.
@details  The algorithm related to density-based class.

Implementation based on paper @cite inproceedings::dbscan::1.

*/
class dbscan {
private:
    const dataset *            m_data_ptr      = nullptr;  /* temporary pointer to input data that is used only during processing */

    dbscan_data *              m_result_ptr    = nullptr;  /* temporary pointer to clustering result that is used only during processing */

    std::vector<bool>          m_visited         = { };

    std::vector<bool>          m_belong          = { };

    double                     m_initial_radius  = 0.0;    /* original radius that was specified by user */

    size_t                     m_neighbors       = 0;

    data_t                     m_type            = data_t::POINTS;

    container::kdtree_balanced m_kdtree = container::kdtree_balanced();

public:
    /*!
    
    @brief    Default constructor of clustering algorithm.
    
    */
    dbscan() = default;

    /*!
    
    @brief    Constructor of clustering algorithm where algorithm parameters for processing are
               specified.
    
    @param[in] p_radius_connectivity: connectivity radius between objects.
    @param[in] p_minimum_neighbors: minimum amount of shared neighbors that is require to connect
                two object (if distance between them is less than connectivity radius).
    
    */
    dbscan(const double p_radius_connectivity, const size_t p_minimum_neighbors);

    /*!
    
    @brief    Default destructor of the algorithm.
    
    */
    ~dbscan() = default;

public:
    /*!
    
    @brief    Performs cluster analysis of an input data.
    
    @param[in]  p_data: input data (points) for cluster analysis.
    @param[out] p_result: clustering result of an input data.
    
    */
    void process(const dataset & p_data, dbscan_data & p_result);

    /*!
    
    @brief    Performs cluster analysis of an input data of specific type.
    
    @param[in]  p_data: input data for cluster analysis.
    @param[in]  p_type: type of an input data that should be clustered.
    @param[out] p_result: clustering result of an input data.
    
    */
    void process(const dataset & p_data, const data_t p_type, dbscan_data & p_result);

private:
    /*!
    
    @brief    Obtains neighbors of the specified node (data object).
    
    @param[in]  p_index: index of the node (data object).
    @param[out] p_neighbors: neighbor indexes of the specified node (data object).
    
    */
    void get_neighbors(const size_t p_index, std::vector<size_t> & p_neighbors);

    void get_neighbors_from_points(const size_t p_index, std::vector<size_t> & p_neighbors);

    void get_neighbors_from_distance_matrix(const size_t p_index, std::vector<size_t> & p_neighbors);

    void create_kdtree(const dataset & p_data);

    void expand_cluster(const std::size_t p_index, cluster & allocated_cluster);
};


}

}