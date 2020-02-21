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

#include <pyclustering/container/kdtree.hpp>

#include <limits>
#include <stack>


namespace pyclustering {

namespace container {


kdtree::kdtree(const dataset & p_data, const std::vector<void *> & p_payloads) :
    kdtree_balanced(p_data, p_payloads)
{ }


kdnode::ptr kdtree::insert(const std::vector<double> & p_point, void * p_payload) {
    kdnode::ptr inserted_kdnode;

    if (m_root == nullptr) {
        kdnode::ptr node = std::make_shared<kdnode>(p_point, p_payload, nullptr, nullptr, nullptr, 0);

        m_root = node;
        m_dimension = node->get_dimension();

        inserted_kdnode = std::move(node);
    }
    else {
        kdnode::ptr cur_node = m_root;

        while(true) {
            /* If new node is greater or equal than current node then check right leaf */
            if (*cur_node <= p_point) {
                if (cur_node->get_right() == nullptr) {
                    std::size_t discriminator = cur_node->get_discriminator() + 1;
                    if (discriminator >= m_dimension) {
                        discriminator = 0;
                    }

                    cur_node->set_right(std::make_shared<kdnode>(p_point, p_payload, nullptr, nullptr, cur_node, discriminator));
                    inserted_kdnode = cur_node->get_right();
                    break;
                }
                else {
                    cur_node = cur_node->get_right();
                }
            }
            /* If new node is less than current then check left leaf */
            else {
                if (cur_node->get_left() == nullptr) {
                    std::size_t discriminator = cur_node->get_discriminator() + 1;
                    if (discriminator >= m_dimension) {
                        discriminator = 0;
                    }

                    cur_node->set_left(std::make_shared<kdnode>(p_point, p_payload, nullptr, nullptr, cur_node, discriminator));
                    inserted_kdnode = cur_node->get_left();
                    break;
                }
                else {
                    cur_node = cur_node->get_left();
                }
            }
        }
    }

    m_size++;
    return inserted_kdnode;
}


void kdtree::remove(const std::vector<double> & p_point) {
    kdnode::ptr node_for_remove = find_node(p_point);
    if (node_for_remove == nullptr) {
        return;
    }

    remove(node_for_remove);
}


void kdtree::remove(const std::vector<double> & p_point, const void * p_payload) {
    kdnode::ptr node_for_remove = find_node(p_point, p_payload);
    if (node_for_remove == nullptr) {
        return;
    }

    remove(node_for_remove);
}


void kdtree::remove(kdnode::ptr & p_node_for_remove) {
    kdnode::ptr parent = p_node_for_remove->get_parent();
    kdnode::ptr node = recursive_remove(p_node_for_remove);

    if (parent == nullptr) {
        m_root = node;

        /* if tree is almost destroyed */
        if (node != nullptr) {
            node->set_parent(nullptr);
        }

        m_size--;
    }
    else {
        if (parent->get_left() == p_node_for_remove) {
            parent->set_left(node);
        }
        else if (parent->get_right() == p_node_for_remove) {
            parent->set_right(node);
        }
        else {
            throw std::runtime_error("Structure of KD Tree is corrupted");
        }

        m_size--;
    }
}


kdnode::ptr kdtree::recursive_remove(kdnode::ptr & p_node) {
    if ( (p_node->get_right() == nullptr) && (p_node->get_left() == nullptr) ) {
        return nullptr;
    }

    std::size_t discriminator = p_node->get_discriminator();

    /* Check if only left branch exist */
    if (p_node->get_right() == nullptr) {
        p_node->set_right(p_node->get_left());
        p_node->set_left(nullptr);
    }

    /* Find minimal node in line with coordinate that is defined by discriminator */
    kdnode::ptr minimal_node = find_minimal_node(p_node->get_right(), discriminator);
    kdnode::ptr parent = minimal_node->get_parent();

    if (parent->get_left() == minimal_node) {
        parent->set_left(recursive_remove(minimal_node));
    }
    else if (parent->get_right() == minimal_node) {
        parent->set_right(recursive_remove(minimal_node));
    }
    else {
        throw std::runtime_error("Structure of KD Tree is corrupted");
    }

    minimal_node->set_parent(p_node->get_parent());
    minimal_node->set_discriminator(p_node->get_discriminator());
    minimal_node->set_right(p_node->get_right());
    minimal_node->set_left(p_node->get_left());

    /* Update parent for successors of previous parent */
    if (minimal_node->get_right() != nullptr) {
        minimal_node->get_right()->set_parent(minimal_node);
    }

    if (minimal_node->get_left() != nullptr) {
        minimal_node->get_left()->set_parent(minimal_node);
    }

    return minimal_node;
}


kdnode::ptr kdtree::find_minimal_node(const kdnode::ptr & p_cur_node, std::size_t p_discriminator) {
    std::stack<kdnode::ptr> stack;
    kdnode::ptr minimal_node = p_cur_node;
    kdnode::ptr cursor = p_cur_node;
    std::vector<kdnode::ptr> candidates;
    bool is_done = false;

    while (!is_done) {
        if (cursor != nullptr) {
            stack.push(cursor);
            cursor = cursor->get_left();
        }
        else {
            if (!stack.empty()) {
                cursor = stack.top();
                candidates.push_back(cursor);
                stack.pop();
                cursor = cursor->get_right();
            }
            else {
                is_done = true;
            }
        }
    }

    for (size_t i = 0; i < candidates.size(); i++) {
        if (candidates[i]->get_value(p_discriminator) <= minimal_node->get_value(p_discriminator)) {
            minimal_node = candidates[i];
        }
    }

    return minimal_node;
}


}

}
