/*!

@authors Andrei Novikov (pyclustering@yandex.ru)
@date 2014-2020
@copyright BSD-3-Clause

*/

#pragma once


#include <list>
#include <set>
#include <tuple>

#include <pyclustering/container/kdtree_balanced.hpp>

#include <pyclustering/cluster/data_type.hpp>
#include <pyclustering/cluster/optics_data.hpp>
#include <pyclustering/cluster/optics_descriptor.hpp>


namespace pyclustering {

namespace clst {


/*!

@brief Class represents clustering algorithm OPTICS (Ordering Points To Identify Clustering Structure).
@details OPTICS is a density-based algorithm. Purpose of the algorithm is to provide explicit clusters, but create clustering-ordering representation of the input data.
          Clustering-ordering information contains information about internal structures of data set in terms of density and proper connectivity radius can be obtained
          for allocation required amount of clusters using this diagram. In case of usage additional input parameter 'amount of clusters' connectivity radius should be
          bigger than real - because it will be calculated by the algorithms.

Implementation based on paper @cite article::optics::1.

*/
class optics {
public:
    static const double       NONE_DISTANCE;    /**< Defines no distance value. */
    static const std::size_t  INVALID_INDEX;    /**< Defines incorrect index. */

private:
    struct neighbor_descriptor {
    public:
        std::size_t m_index             = INVALID_INDEX;
        double m_reachability_distance  = 0;

    public:
        neighbor_descriptor(const std::size_t p_index, const double p_distance) :
            m_index(p_index), m_reachability_distance(p_distance)
        { }
    };

    struct neighbor_descriptor_less {
    public:
        bool operator()(const neighbor_descriptor & p_object1, const neighbor_descriptor & p_object2) const {
            return p_object1.m_reachability_distance < p_object2.m_reachability_distance;
        }
    };

    using neighbors_collection = std::multiset<neighbor_descriptor, neighbor_descriptor_less>;

private:
    const dataset       * m_data_ptr        = nullptr;

    optics_data         * m_result_ptr      = nullptr;

    double              m_radius            = 0.0;

    std::size_t         m_neighbors         = 0;

    std::size_t         m_amount_clusters   = 0;

    data_t              m_type              = data_t::POINTS;

    container::kdtree_balanced      m_kdtree            = container::kdtree_balanced();

    optics_object_sequence *        m_optics_objects    = nullptr;

    std::list<optics_descriptor *>  m_ordered_database  = { };

public:
    /*!
    
    @brief Default constructor of the algorithm.
    
    */
    optics() = default;

    /*!
    
    @brief Default copy constructor of the algorithm.
    
    */
    optics(const optics & p_other) = default;

    /*!

    @brief Default move constructor of the algorithm.

    */
    optics(optics && p_other) = default;

    /*!

    @brief Parameterized constructor of the algorithm.

    @param[in] p_radius: connectivity radius between objects.
    @param[in] p_neighbors: minimum amount of shared neighbors that is require to connect
                two object (if distance between them is less than connectivity radius).

    */
    optics(const double p_radius, const std::size_t p_neighbors);

    /*!

    @brief Creates algorithm with specified parameters.

    @param[in] p_radius: connectivity radius between objects.
    @param[in] p_neighbors: minimum amount of shared neighbors that is require to connect
                two object (if distance between them is less than connectivity radius).
    @param[in] p_amount_clusters: amount of clusters that should be allocated (in this case
                connectivity radius may be changed by the algorithm.
    */
    optics(const double p_radius, const std::size_t p_neighbors, const std::size_t p_amount_clusters);

    /*!

    @brief Default destructor to destroy algorithm instance.

    */
    ~optics() = default;

public:
    /*!

    @brief    Performs cluster analysis of an input data.

    @param[in]  p_data: input data for cluster analysis.
    @param[out] p_result: clustering result of an input data (consists of allocated clusters,
                 cluster-ordering, noise and proper connectivity radius).

    */
    void process(const dataset & p_data, optics_data & p_result);

    /*!

    @brief    Performs cluster analysis of specific input data (points or distance matrix) that is defined by the
               `p_type` argument.

    @param[in]  p_data: input data for cluster analysis.
    @param[in]  p_type: type of input data (points or distance matrix).
    @param[out] p_result: clustering result of an input data (consists of allocated clusters,
                 cluster-ordering, noise and proper connectivity radius).

    */
    void process(const dataset & p_data, const data_t p_type, optics_data & p_result);

private:
    void initialize();

    void allocate_clusters();

    void expand_cluster_order(optics_descriptor & p_object);

    void extract_clusters();

    void get_neighbors(const std::size_t p_index, neighbors_collection & p_neighbors);

    void get_neighbors_from_points(const std::size_t p_index, neighbors_collection & p_neighbors);

    void get_neighbors_from_distance_matrix(const std::size_t p_index, neighbors_collection & p_neighbors);

    double get_core_distance(const neighbors_collection & p_neighbors) const;

    void update_order_seed(const optics_descriptor & p_object, const neighbors_collection & p_neighbors, std::multiset<optics_descriptor *, optics_pointer_descriptor_less> & order_seed);

    void calculate_ordering();

    void calculate_cluster_result();

    void create_kdtree();
};


}

}