/*!

@authors Andrei Novikov (pyclustering@yandex.ru)
@date 2014-2020
@copyright BSD-3-Clause

*/

#pragma once

#include <functional>
#include <vector>

#include <pyclustering/container/kdnode.hpp>
#include <pyclustering/definitions.hpp>


namespace pyclustering {

namespace container {


/*!

@brief   Searcher in KD Tree provides services related to searching in KD Tree.

*/
class kdtree_searcher {
public:
    using rule_store = std::function<void(const kdnode::ptr, const double)>;

private:
    using proc_store = std::function<void(const kdnode::ptr)>;

private:
    mutable std::vector<double>        m_nodes_distance     = { };
    mutable std::vector<kdnode::ptr>   m_nearest_nodes      = { };
    mutable dataset                    m_nearest_points     = { };

    mutable rule_store                 m_user_rule          = nullptr;
    mutable proc_store                 m_proc               = nullptr;

    double                  m_distance            = -1;
    double                  m_sqrt_distance       = -1;
    kdnode::ptr             m_initial_node        = nullptr;
    std::vector<double>     m_search_point        = { };

public:
    /**
    *
    * @brief   Default constructor. Search will not be performed until it's initialized.
    *
    */
    kdtree_searcher() = default;

    /**
    *
    * @brief   Constructor of searcher with request for searching.
    *
    * @param[in] point: point for which nearest nodes should be found.
    * @param[in] node: initial node in tree from which searching should started.
    * @param[in] radius_search: allowable distance for searching from the point.
    *
    */
    kdtree_searcher(const std::vector<double> & point, const kdnode::ptr & node, const double radius_search);

    /**
    *
    * @brief   Default destructor.
    *
    */
    ~kdtree_searcher() = default;

public:
    /**
    *
    * @brief   Search nodes that are located in specified distance from specified point.
    *
    * @param[out] p_distances: distances from the point to nodes in the location (that are radius-reachable).
    * @param[out] p_nearest_nodes: nodes in the location (radius-reachable).
    *
    * @return  Return vector of found nodes in kd tree that satisfy the request. If distances are
    *          specified then it will be filled by corresponding distances.
    *
    */
    void find_nearest_nodes(std::vector<double> & p_distances, std::vector<kdnode::ptr> & p_nearest_nodes) const;

    /**
    *
    * @brief   Search the nearest node in specified location for specified point in the request.
    *
    * @return  Return pointer to the nearest node in kd tree that satisfy the request.
    *
    */
    kdnode::ptr find_nearest_node() const;

    /**
    *
    * @brief   Search the nearest nodes and store information about found node using user-defined way.
    *
    * @param[in]  p_store_rule: defines how to store KD-node.
    *
    */
    void find_nearest(const rule_store & p_store_rule) const;

private:
    /**
    *
    * @brief   Initialization of new request for searching.
    *
    * @param[in] point: point for which nearest nodes should be found.
    * @param[in] node: initial node in tree from which searching should started.
    * @param[in] radius_search: allowable distance for searching from the point.
    *
    */
    void initialize(const std::vector<double> & point, const kdnode::ptr & node, const double radius_search);

    /**
    *
    * @brief   Clear internal temporary structures.
    *
    */
    void clear() const;

    /**
    *
    * @brief   Recursive method for searching nodes that satisfy the request.
    *
    * @param[in] node: initial node in tree from which searching should performed.
    *
    */
    void recursive_nearest_nodes(const kdnode::ptr & node) const;

    /**
    *
    * @brief   Append to storage reachable node and distance to it.
    *
    * @param[in] node: node that should be added to best collection if it is reachable.
    *
    */
    void store_if_reachable(const kdnode::ptr & node) const;

    /**
    *
    * @brief   Store only one node in collection if it the best node.
    *
    * @param[in] node: node that should be added to best collection if it is reachable.
    *
    */
    void store_best_if_reachable(const kdnode::ptr & node) const;

    /**
    *
    * @brief   Store nodes using user-defined rule.
    *
    * @param[in] node: node that should be added to best collection if it is reachable.
    *
    */
    void store_user_nodes_if_reachable(const kdnode::ptr & node) const;
};


}

}