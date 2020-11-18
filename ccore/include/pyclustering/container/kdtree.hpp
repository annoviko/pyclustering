/*!

@authors Andrei Novikov (pyclustering@yandex.ru)
@date 2014-2020
@copyright BSD-3-Clause

*/

#pragma once


#include "kdtree_balanced.hpp"

#include <functional>
#include <memory>
#include <vector>

#include <pyclustering/definitions.hpp>


namespace pyclustering {

namespace container {


/**
 *
 * @brief   KD Tree - structure for storing data where fast distance searching is required.
 *
 */
class kdtree : public kdtree_balanced {
private:
    /**
    *
    * @brief   Recursive remove of node in tree.
    *
    * @param[in] p_node: node that should be removed.
    *
    * @return  Node that should replace removed node (if it's not leaf).
    *
    */
    kdnode::ptr recursive_remove(kdnode::ptr & p_node);

    /**
    *
    * @brief   Find minimal node in subtree in line with specified discriminator.
    *
    * @param[in] p_cur_node: root of subtree where searching should be performed.
    * @param[in] p_discriminator: discriminator that is used for comparison of nodes.
    *
    * @return  Return the smallest node in specified subtree in line with discriminator.
    *
    */
    static kdnode::ptr find_minimal_node(const kdnode::ptr & p_cur_node, const std::size_t p_discriminator);

public:
    kdtree() = default;

    kdtree(const dataset & p_data, const std::vector<void *> & p_payloads = {});

    kdtree(const kdtree & p_other) = default;

    kdtree(kdtree && p_other) = default;

    virtual ~kdtree() = default;

public:
    /**
    *
    * @brief   Insert new node in the tree.
    *
    * @param[in] p_point: coordinates that describe node in tree.
    * @param[in] p_payload: payloads of node (can be nullptr if it's not required).
    *
    * @return  Pointer to added node in the tree.
    *
    */
    kdnode::ptr insert(const std::vector<double> & p_point, void * p_payload = nullptr);

    /**
    *
    * @brief   Remove point with specified coordinates.
    *
    * @param[in] p_point: coordinates that describe node in tree.
    *
    */
    void remove(const std::vector<double> & p_point);

    /**
    *
    * @brief   Remove point with specified coordinates and specific payload.
    * @details This remove is useful when points with the same coordinates are located
    *           in the tree and but only one of them should be removed with specific payload where
    *           node ID or other unique information is stored.
    *
    * @param[in] p_point: coordinates that describe node in tree.
    * @param[in] p_payload: payload that is used to identify node.
    *
    */
    void remove(const std::vector<double> & p_point, const void * p_payload);

    /**
    *
    * @brief   Remove node from the tree.
    *
    * @param[in] p_node_for_remove: pointer to node that is located in tree.
    *
    */
    void remove(kdnode::ptr & p_node_for_remove);

public:
    /*!

    @brief   Assignment operator for KD-tree.

    @param[in] p_other: another KD-tree that should be copied to the tree.

    @return  Returns reference to KD-tree to where another tree was copied.

    */
    kdtree & operator=(const kdtree & p_other) = default;

    /*!

    @brief   Movement operator for KD-tree.

    @param[in,out] p_other: another KD-tree that should be moved to the tree.

    @return  Returns reference to KD-tree to where another was moved.

    */
    kdtree & operator=(kdtree && p_other) = default;
};


}

}