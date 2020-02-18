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


#include <pyclustering/container/kdnode.hpp>


namespace pyclustering {

namespace container {


kdnode::kdnode(const std::vector<double> & p_data, void * p_payload, const kdnode::ptr & p_left, const kdnode::ptr & p_right, const kdnode::ptr & p_parent, const std::size_t p_desc) :
    m_data(p_data),
    m_payload(p_payload),
    m_left(p_left),
    m_right(p_right),
    m_parent(p_parent),
    m_discriminator(p_desc)
{ }


void kdnode::set_left(const kdnode::ptr & p_node) {
    m_left = p_node;
}


void kdnode::set_right(const kdnode::ptr & p_node) {
    m_right = p_node;
}


void kdnode::set_parent(const kdnode::ptr & p_node) {
    m_parent = p_node;
}


void kdnode::set_data(const point & p_data) {
    m_data = p_data;
}


void kdnode::set_payload(void * p_payload) {
    m_payload = p_payload;
}


void kdnode::set_discriminator(const std::size_t disc) {
    m_discriminator = disc;
}


kdnode::ptr kdnode::get_left() const {
    return m_left;
}


kdnode::ptr kdnode::get_right() const {
    return m_right;
}


kdnode::ptr kdnode::get_parent() const {
    return m_parent.lock();
}


void * kdnode::get_payload() const {
    return m_payload;
}


kdnode::ptr kdnode::find_node(const point & p_point) {
    search_node_rule rule = [&p_point](const kdnode & p_node) { 
        return p_point == p_node.get_data();
    };
    return find_node(p_point, rule);
}


kdnode::ptr kdnode::find_node(const point & p_point, const search_node_rule & p_rule) {
    kdnode::ptr cur_node = shared_from_this();

    while (cur_node != nullptr) {
        if (*cur_node <= p_point) {
            if (p_rule(*cur_node)) {    /* Less or equal - check if equal. */
                return cur_node;
            }

            cur_node = cur_node->get_right();
        }
        else {
            cur_node = cur_node->get_left();
        }
    }

    return nullptr;
}


const std::vector<double> & kdnode::get_data() const {
    return m_data;
}


std::vector<double> & kdnode::get_data() {
    return m_data;
}


double kdnode::get_value() const {
    return m_data[m_discriminator];
}


double kdnode::get_value(const std::size_t p_descr) const {
    return m_data[p_descr];
}


std::size_t kdnode::get_discriminator() const {
    return m_discriminator;
}


std::size_t kdnode::get_dimension() const {
    return m_data.size();
}


void kdnode::get_children(std::vector<kdnode::ptr> & p_children) {
    p_children.clear();

    if (m_left != nullptr) {
        p_children.push_back(m_left);
    }

    if (m_right != nullptr) {
        p_children.push_back(m_right);
    }
}


bool operator < (const kdnode & node, const std::vector<double> & point) {
    return node.get_value() < point[node.get_discriminator()];
}


bool operator < (const std::vector<double> & point, const kdnode & node) {
    return point[node.get_discriminator()] < node.get_value();
}


bool operator > (const kdnode & node, const std::vector<double> & point) {
    return point[node.get_discriminator()] < node.get_value();
}


bool operator > (const std::vector<double> & point, const kdnode & node) {
    return node.get_value() < point[node.get_discriminator()];
}


bool operator <= (const kdnode & node, const std::vector<double> & point) {
    return !(node.get_value() > point[node.get_discriminator()]);
}


bool operator <= (const std::vector<double> & point, const kdnode & node) {
    return !(point[node.get_discriminator()] > node.get_value());
}


bool operator >= (const kdnode & node, const std::vector<double> & point) {
    return !(node.get_value() < point[node.get_discriminator()]);
}


bool operator >= (const std::vector<double> & point, const kdnode & node) {
    return !(point[node.get_discriminator()] < node.get_value());
}


bool operator == (const kdnode & node, const std::vector<double> & point) {
    return node.get_value() == point[node.get_discriminator()];
}


bool operator == (const std::vector<double> & point, const kdnode & node) {
    return node == point;
}


}

}