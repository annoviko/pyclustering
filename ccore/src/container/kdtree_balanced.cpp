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

#include <pyclustering/container/kdtree_balanced.hpp>
#include <pyclustering/utils/algorithm.hpp>

#include <algorithm>


using namespace pyclustering::utils::algorithm;


namespace pyclustering {

namespace container {


kdtree_balanced::kdtree_balanced(const dataset & p_data, const std::vector<void *> & p_payloads) {
    if (p_data.empty()) { return; }

    std::vector<kdnode::ptr> nodes(p_data.size());
    for (std::size_t i = 0; i < p_data.size(); i++) {
        nodes[i] = std::make_shared<kdnode>(p_data[i], nullptr, nullptr, nullptr, nullptr, 0);

        if (!p_payloads.empty()) {
            nodes[i]->set_payload(p_payloads[i]);
        }
    }

    m_dimension = p_data.at(0).size();
    m_root = create_tree(nodes.begin(), nodes.end(), nullptr, 0);
}


kdnode::ptr kdtree_balanced::create_tree(std::vector<kdnode::ptr>::iterator p_begin, std::vector<kdnode::ptr>::iterator p_end, const kdnode::ptr & p_parent, const std::size_t p_depth) {
    const int length = static_cast<int>(std::distance(p_begin, p_end));
    if (length == 0) {
        return nullptr;
    }

    const std::size_t discriminator = p_depth % m_dimension;
    const int median = length / 2;

    std::sort(p_begin, p_end, [discriminator](const kdnode::ptr & p1, const kdnode::ptr & p2) {
        return p1->get_data()[discriminator] < p2->get_data()[discriminator];
    });

    auto median_iter = find_left_element(p_begin, p_begin + median + 1, 
        [discriminator](const kdnode::ptr & p1, const kdnode::ptr & p2) {
            return p1->get_data()[discriminator] < p2->get_data()[discriminator];
        }
    );

    kdnode::ptr new_node = *median_iter;
    new_node->set_parent(p_parent);
    new_node->set_discriminator(discriminator);
    new_node->set_left(create_tree(p_begin, median_iter, new_node, p_depth + 1));
    new_node->set_right(create_tree(median_iter + 1, p_end, new_node, p_depth + 1));

    m_size++;
    return new_node;
}


kdnode::ptr kdtree_balanced::find_node(const point & p_point) const {
    return m_root ? m_root->find_node(p_point) : nullptr;
}


kdnode::ptr kdtree_balanced::find_node(const point & p_point, const void * p_payload) const {
    if (!m_root) {
        return nullptr;
    }

    return m_root->find_node(p_point, [&p_point, p_payload](const kdnode & p_node) {
        return (p_point == p_node.get_data()) && (p_payload == p_node.get_payload());
    });
}


kdnode::ptr kdtree_balanced::get_root() const {
    return m_root;
}


std::size_t kdtree_balanced::get_size() const {
    return m_size;
}


kdtree_balanced & kdtree_balanced::operator=(const kdtree_balanced & p_other) {
    if (this != &p_other) {
        m_root = p_other.m_root;
        m_dimension = p_other.m_dimension;
        m_size = p_other.m_size;
    }

    return *this;
}


kdtree_balanced & kdtree_balanced::operator=(kdtree_balanced && p_other) {
    if (this != &p_other) {
        m_root = std::move(p_other.m_root);
        m_dimension = std::move(p_other.m_dimension);
        m_size = std::move(p_other.m_size);
    }

    return *this;
}


}

}