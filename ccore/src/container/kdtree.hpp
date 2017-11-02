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

#pragma once


#include "kdnode.hpp"

#include <functional>
#include <memory>
#include <vector>

#include "definitions.hpp"


namespace container {


/**
 *
 * @brief   KD Tree - structure for storing data where fast distance searching is required.
 *
 */
class kdtree {
private:
    kdnode::ptr     m_root          = nullptr;
    std::size_t     m_dimension     = 0;

    std::size_t     m_size          = 0;

private:
    /**
    *
    * @brief   Recursive remove of node in tree.
    *
    * @param   node            - node that should be removed.
    *
    * @return  Node that should replace removed node (if it's not leaf).
    *
    */
    kdnode::ptr recursive_remove(kdnode::ptr node);

    /**
    *
    * @brief   Find minimal node in subtree in line with specified discriminator.
    *
    * @param   node            - root of subtree where searching should be performed.
    * @param   discriminator   - discriminator that is used for comparison of nodes.
    *
    * @return  Return the smallest node in specified subtree in line with discriminator.
    *
    */
    kdnode::ptr find_minimal_node(const kdnode::ptr p_cur_node, const std::size_t p_discriminator);

public:
    kdtree(void) = default;

    kdtree(const kdtree & p_other) = default;

    kdtree(kdtree && p_other) = default;

    virtual ~kdtree(void) = default;

public:
    /**
    *
    * @brief   Insert new node in the tree.
    *
    * @param   point              - coordinates that describe node in tree.
    * @param   payload            - payloads of node (can be nullptr if it's not required).
    *
    * @return  Pointer to added node in the tree.
    *
    */
    kdnode::ptr insert(const std::vector<double> & p_point, void * p_payload = nullptr);

    /**
    *
    * @brief   Remove point with specified coordinates.
    *
    * @param   point              - coordinates that describe node in tree.
    *
    */
    void remove(const std::vector<double> & p_point);

    /**
    *
    * @brief   Remove node from the tree.
    *
    * @param   node_for_remove    - pointer to node that is located in tree.
    *
    */
    void remove(kdnode::ptr p_node_for_remove);

    /**
    *
    * @brief   Find node in tree using coordinates.
    *
    * @param   point              - coordinates of searched node.
    *
    * @return  Pointer to found node in tree.
    *
    */
    kdnode::ptr find_node(const std::vector<double> & p_point) const;

    /**
    *
    * @brief   Find node in tree using coordinates in subtree.
    *
    * @param   point              - coordinates of searched node.
    * @param   cur_node           - root of subtree.
    *
    * @return  Pointer to found node in tree.
    *
    */
    kdnode::ptr find_node(const std::vector<double> & p_point, kdnode::ptr p_cur_node) const;

    /**
    *
    * @brief   Traverse tree from specified node and returns number of nodes in subtree.
    *
    * @param   node               - pointer to node of tree.
    *
    * @return  Returns number of nodes in subtree.
    *
    */
    std::size_t traverse(const kdnode::ptr p_node);

    /**
    *
    * @brief   Return root of the tree.
    *
    * @return  Returns pointer to root of the tree.
    *
    */
    kdnode::ptr get_root(void);

    /**
    *
    * @brief   Return size of KD-tree.
    *
    * @return  Returns amount of nodes in KD-tree.
    *
    */
    std::size_t get_size(void) const;

public:
    kdtree & operator=(const kdtree & p_other);

    kdtree & operator=(kdtree && p_other);
};



/**
 *
 * @brief   Searcher in KD Tree provides services related to searching in KD Tree.
 *
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
    kdtree_searcher(void) = default;

    /**
    *
    * @brief   Constructor of searcher with request for searching.
    *
    * @param[in] point: point for which nearest nodes should be found.
    * @param[in] node: initial node in tree from which searching should started.
    * @param[in] radius_search: allowable distance for searching from the point.
    *
    */
    kdtree_searcher(const std::vector<double> & point, const kdnode::ptr node, const double radius_search);

    /**
    *
    * @brief   Default destructor.
    *
    */
    ~kdtree_searcher(void) = default;

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
    kdnode::ptr find_nearest_node(void) const;

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
    void initialize(const std::vector<double> & point, const kdnode::ptr node, const double radius_search);

    /**
    *
    * @brief   Clear internal temporary structures.
    *
    */
    void clear(void) const;

    /**
    *
    * @brief   Recursive method for searching nodes that satisfy the request.
    *
    * @param[in] node: initial node in tree from which searching should performed.
    *
    */
    void recursive_nearest_nodes(const kdnode::ptr node) const;

    /**
    *
    * @brief   Append to storage reachable node and distance to it.
    *
    * @param[in] node: node that should be added to best collection if it is reachable.
    *
    */
    void store_if_reachable(const kdnode::ptr node) const;

    /**
    *
    * @brief   Store only one node in collection if it the best node.
    *
    * @param[in] node: node that should be added to best collection if it is reachable.
    *
    */
    void store_best_if_reachable(const kdnode::ptr node) const;

    /**
    *
    * @brief   Store nodes using user-defined rule.
    *
    * @param[in] node: node that should be added to best collection if it is reachable.
    *
    */
    void store_user_nodes_if_reachable(const kdnode::ptr node) const;
};


}
