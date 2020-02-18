/*!

@authors Andrei Novikov (pyclustering@yandex.ru)
@date 2014-2020
@copyright GNU Public License

@cond GNU_PUBLIC_LICENSE
    pyclustering is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    pyclustering is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
@endcond

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
    kdnode() = default;

    kdnode(const std::vector<double> & p_data, void * p_payload, const kdnode::ptr & p_left, const kdnode::ptr & p_right, const kdnode::ptr & p_parent, const std::size_t p_desc);

    kdnode(const kdnode & p_other) = default;

    kdnode(kdnode && p_other) = default;

    virtual ~kdnode() = default;

public:
    void set_left(const kdnode::ptr & p_node);

    void set_right(const kdnode::ptr & p_node);

    void set_parent(const kdnode::ptr & p_node);

    void set_data(const point & p_data);

    void set_payload(void * p_payload);

    void set_discriminator(const std::size_t disc);

public:
    kdnode::ptr get_left() const;

    kdnode::ptr get_right() const;

    kdnode::ptr get_parent() const;

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

    const std::vector<double> & get_data() const;

    std::vector<double> & get_data();

    double get_value() const;

    double get_value(const std::size_t p_descr) const;

    std::size_t get_discriminator() const;

    std::size_t get_dimension() const;

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