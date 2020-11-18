/*!

@authors Andrei Novikov (pyclustering@yandex.ru)
@date 2014-2020
@copyright BSD-3-Clause

*/


#pragma once


#include <functional>
#include <memory>
#include <vector>

#include <pyclustering/definitions.hpp>


namespace pyclustering {

namespace container {

/*!

@brief   Node of KD Tree.

*/
class kdnode : public std::enable_shared_from_this<kdnode> {
public:
  using ptr                 = std::shared_ptr<kdnode>;

private:
  using weak_ptr            = std::weak_ptr<kdnode>;
  using search_node_rule    = std::function< bool(const kdnode&) >;

private:
    std::vector<double>           m_data    = { };
    void *                        m_payload = nullptr;

    ptr      m_left    = nullptr;
    ptr      m_right   = nullptr;
    weak_ptr m_parent  = weak_ptr();

    std::size_t m_discriminator = 0;

public:
    /*!

    @brief   Default constructor to create empty node.

    */
    kdnode() = default;

    /*!

    @brief   Constructs a KD-tree node.

    @param[in] p_data: points that represents the node.
    @param[in] p_payload: point to data block that is associated with the node.
    @param[in] p_left: pointer to the left child node.
    @param[in] p_right: pointer to the right child node.
    @param[in] p_parent: pointer to the parent node.
    @param[in] p_desc: dimension value of the node.

    */
    kdnode(const std::vector<double> & p_data, void * p_payload, const kdnode::ptr & p_left, const kdnode::ptr & p_right, const kdnode::ptr & p_parent, const std::size_t p_desc);

    /*!

    @brief   Default copy constructor.

    */
    kdnode(const kdnode & p_other) = default;

    /*!

    @brief   Default move constructor.

    */
    kdnode(kdnode && p_other) = default;

    /*!

    @brief   Default destructor.

    */
    virtual ~kdnode() = default;

public:
    /*!

    @brief   Set left child of the node.

    @param[in] p_node: left child node.

    */
    void set_left(const kdnode::ptr & p_node);

    /*!

    @brief   Set right child of the node.

    @param[in] p_node: right child node.

    */
    void set_right(const kdnode::ptr & p_node);

    /*!

    @brief   Set parent of the node.

    @param[in] p_node: parent node.

    */
    void set_parent(const kdnode::ptr & p_node);

    /*!

    @brief   Set data of the node.

    @param[in] p_data: point that represents node.

    */
    void set_data(const point & p_data);

    /*!

    @brief   Set payload of the node.

    @param[in] p_payload: pointer to data block that is associated with the node.

    */
    void set_payload(void * p_payload);

    /*!

    @brief   Set discriminator of the node.

    @param[in] disc: discriminator value (dimension).

    */
    void set_discriminator(const std::size_t disc);

public:
    /*!

    @brief   Return left child node.

    @return  Left child node.

    */
    kdnode::ptr get_left() const;

    /*!

    @brief   Return right child node.

    @return  Right child node.

    */
    kdnode::ptr get_right() const;

    /*!

    @brief   Return parent node.

    @return  Parent node.

    */
    kdnode::ptr get_parent() const;

    /*!

    @brief   Return pointer to data block that is associated with the current node.

    @return  Pointer to data block that.

    */
    void * get_payload() const;

    /*!

    @brief   Find node in KD-tree using current node as a root of a subtree, the first founded node with
    specified coordinates is returned.

    @param[in] p_point: coordinates of searched node.

    @return  Pointer to found node in the sub-tree.

    */
    kdnode::ptr find_node(const point & p_point);

    /*!

    @brief   Find node using specified rule, it returns the first node that satisfy search rule.

    @param[in] p_point: coordinates of searched node.
    @param[in] p_cur_node: node from which search is performed.
    @param[in] p_rule: rule that should be satisfied by searched node.

    @return  Return the smallest node in specified subtree in line with discriminator.

    */
    kdnode::ptr find_node(const point & p_point, const search_node_rule & p_rule);

    /*!

    @brief   Return constant reference to a point (coordinates) that represents the current node.

    @return  Constant reference to a point (coordinates) of the current node.

    */
    const std::vector<double> & get_data() const;

    /*!

    @brief   Return reference to a point (coordinates) that represents the current node.

    @return  Reference to a point (coordinates) of the current node.

    */
    std::vector<double> & get_data();

    /*!

    @brief   Return coordinate value that represents the current node.

    @return  Coordinate value that represents the current node.

    */
    double get_value() const;

    /*!

    @brief   Return coordinate value of the specified dimension (discriminator) of the current node.

    @param[in] p_descr: dimension at which coordinate value is required.

    @return  Coordinate value of the specified dimension (discriminator) of the current node.

    */
    double get_value(const std::size_t p_descr) const;

    /*!

    @brief   Return discriminator value of the current node.

    @return  Discriminator value of the current node.

    */
    std::size_t get_discriminator() const;

    /*!

    @brief   Return dimension - amount of coordinates that represents the current node.

    @return  Dimension - amount of coordinates that represents the current node.

    */
    std::size_t get_dimension() const;

    /*!

    @brief   Return non-null child points.
    @details For example, if a node has only right node and the left node is nullptr then only right node is returned.
              If node does not have children then empty container is returned.

    @return  Dimension - amount of coordinates that represents the current node.

    */
    void get_children(std::vector<kdnode::ptr> & p_children);
};


bool operator < (const kdnode & node, const std::vector<double> & point);
bool operator < (const std::vector<double> & point, const kdnode & node);

bool operator > (const kdnode & node, const std::vector<double> & point);
bool operator > (const std::vector<double> & point, const kdnode & node);

bool operator <= (const kdnode & node, const std::vector<double> & point);
bool operator <= (const std::vector<double> & point, const kdnode & node);

bool operator >= (const kdnode & node, const std::vector<double> & point);
bool operator >= (const std::vector<double> & point, const kdnode & node);

bool operator == (const kdnode & node, const std::vector<double> & point);
bool operator == (const std::vector<double> & point, const kdnode & node);


}

}