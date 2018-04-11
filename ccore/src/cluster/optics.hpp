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


#include <list>
#include <tuple>

#include "container/kdtree.hpp"

#include "cluster/cluster_algorithm.hpp"
#include "cluster/optics_data.hpp"


namespace ccore {

namespace clst {


/**
 *
 * @brief Enumeration of input data type that are processed by OPTICS algorithm.
 *
 */
enum class optics_data_t {
    POINTS,
    DISTANCE_MATRIX
};


/**
 *
 * @brief Object description that used by OPTICS algorithm for cluster analysis.
 *
 */
struct optics_descriptor {
public:
    std::size_t     m_index = -1;
    double          m_core_distance = 0;
    double          m_reachability_distance = 0;
    bool            m_processed = false;

public:
    /**
     *
     * @brief Default constructor to create optics object descriptor.
     *
     */
    optics_descriptor(void) = default;

    /**
     *
     * @brief Default copy constructor to create optics object descriptor.
     *
     */
    optics_descriptor(const optics_descriptor & p_other) = default;

    /**
     *
     * @brief Default move constructor to create optics object descriptor.
     *
     */
    optics_descriptor(optics_descriptor && p_other) = default;

    /**
     *
     * @brief Creates optics object descriptor using specified parameters.
     * @details Processing is always false after creating for any created optics descriptor.
     *
     * @param[in] p_index: index of optics object that corresponds to index of real object in dataset.
     * @param[in] p_core_distance: core distance of optics-object.
     * @param[in] p_reachability_distance: reachability distance of optics-object.
     *
     */
    optics_descriptor(const std::size_t p_index, const double p_core_distance, const double p_reachability_distance);

    /**
     *
     * @brief Default destructor to destroy optics object descriptor.
     *
     */
    ~optics_descriptor(void) = default;

public:
    /**
     *
     * @brief Clears core and reachability distances and processing flag (at the same time index is not reseted).
     *
     */
    void clear(void);
};


/**
 *
 * @brief Class represents clustering algorithm OPTICS (Ordering Points To Identify Clustering Structure).
 * @details OPTICS is a density-based algorithm. Purpose of the algorithm is to provide explicit clusters, but create clustering-ordering representation of the input data.
 *          Clustering-ordering information contains information about internal structures of data set in terms of density and proper connectivity radius can be obtained
 *          for allocation required amount of clusters using this diagram. In case of usage additional input parameter 'amount of clusters' connectivity radius should be
 *          bigger than real - because it will be calculated by the algorithms.
 *
 */
class optics : public cluster_algorithm  {
public:
    static const double NONE_DISTANCE;

private:
    using neighbors_collection = std::vector< std::tuple<std::size_t, double> >;

private:
    const dataset       * m_data_ptr        = nullptr;

    optics_data         * m_result_ptr      = nullptr;

    double              m_radius            = 0.0;

    std::size_t         m_neighbors         = 0;

    std::size_t         m_amount_clusters   = 0;

    optics_data_t       m_type              = optics_data_t::POINTS;

    container::kdtree   m_kdtree            = container::kdtree();

    std::vector<optics_descriptor>      m_optics_objects    = { };

    std::vector<optics_descriptor *>    m_ordered_database  = { };

public:
    /**
     *
     * @brief Default constructor to create algorithm instance.
     *
     */
    optics(void) = default;

    /**
     *
     * @brief Default copy constructor to create algorithm instance.
     *
     */
    optics(const optics & p_other) = default;

    /**
     *
     * @brief Default move constructor to create algorithm instance.
     *
     */
    optics(optics && p_other) = default;

    /**
     *
     * @brief Creates algorithm with specified parameters.
     *
     * @param[in] p_radius: connectivity radius between objects.
     * @param[in] p_neighbors: minimum amount of shared neighbors that is require to connect
     *             two object (if distance between them is less than connectivity radius).
     *
     */
    optics(const double p_radius, const std::size_t p_neighbors);

    /**
     *
     * @brief Creates algorithm with specified parameters.
     *
     * @param[in] p_radius: connectivity radius between objects.
     * @param[in] p_neighbors: minimum amount of shared neighbors that is require to connect
     *             two object (if distance between them is less than connectivity radius).
     * @param[in] p_amount_clusters: amount of clusters that should be allocated (in this case
     *             connectivity radius may be changed by the algorithm.
     */
    optics(const double p_radius, const std::size_t p_neighbors, const std::size_t p_amount_clusters);

    /**
     *
     * @brief Default destructor to destroy algorithm instance.
     *
     */
    virtual ~optics(void) = default;

public:
    /**
    *
    * @brief    Performs cluster analysis of an input data.
    *
    * @param[in]  p_data: input data for cluster analysis.
    * @param[out] p_result: clustering result of an input data (consists of allocated clusters,
    *              cluster-ordering, noise and proper connectivity radius).
    *
    */
    virtual void process(const dataset & p_data, cluster_data & p_result) override;

    /**
    *
    * @brief    Performs cluster analysis of specific input data (points or distance matrix) that is defined by the
    *            'p_type' argument.
    *
    * @param[in]  p_data: input data for cluster analysis.
    * @param[in]  p_type: type of input data (points or distance matrix).
    * @param[out] p_result: clustering result of an input data (consists of allocated clusters,
    *              cluster-ordering, noise and proper connectivity radius).
    *
    */
    virtual void process(const dataset & p_data, const optics_data_t p_type, cluster_data & p_result);

private:
    void initialize(void);

    void allocate_clusters(void);

    void expand_cluster_order(optics_descriptor & p_object);

    void extract_clusters(void);

    void get_neighbors(const std::size_t p_index, neighbors_collection & p_neighbors);

    void get_neighbors_from_points(const std::size_t p_index, neighbors_collection & p_neighbors);

    void get_neighbors_from_distance_matrix(const std::size_t p_index, neighbors_collection & p_neighbors);

    void update_order_seed(const optics_descriptor & p_object, const neighbors_collection & neighbors, std::list<optics_descriptor *> & order_seed);

    void calculate_ordering(void);

    void calculate_cluster_result(void);

    void create_kdtree(void);
};


}

}