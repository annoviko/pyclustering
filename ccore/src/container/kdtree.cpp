/**
*
* @authors Andrei Novikov (pyclustering@yandex.ru)
* @date 2014-2019
* @copyright GNU Public License
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

#include <pyclustering/container/kdtree.hpp>

#include <limits>
#include <iostream>
#include <stack>

#include <pyclustering/utils/metric.hpp>


using namespace pyclustering::utils::metric;


namespace pyclustering {

namespace container {


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


kdnode::ptr kdtree::find_node(const std::vector<double> & p_point) const {
    search_node_rule rule = [&p_point](const kdnode::ptr & p_node) { return p_point == p_node->get_data(); };
    return find_node(p_point, m_root);
}


kdnode::ptr kdtree::find_node(const std::vector<double> & p_point, const void * p_payload) const {
    search_node_rule rule = [&p_point, p_payload](const kdnode::ptr & p_node) { 
        return ( p_point == p_node->get_data() ) && ( p_payload == p_node->get_payload() );
    };

    return find_node_by_rule(p_point, m_root, rule);
}


kdnode::ptr kdtree::find_node(const std::vector<double> & p_point, const kdnode::ptr & p_cur_node) {
    search_node_rule rule = [&p_point](const kdnode::ptr & p_node) { return p_point == p_node->get_data(); };
    return find_node_by_rule(p_point, p_cur_node, rule);
}


kdnode::ptr kdtree::find_node_by_rule(const std::vector<double> & p_point, const kdnode::ptr & p_cur_node, const search_node_rule & p_rule) {
    kdnode::ptr req_node = nullptr;
    kdnode::ptr cur_node = p_cur_node;

    if (p_cur_node == nullptr) { return nullptr; }

    while(true) {
        if (*cur_node <= p_point) {
            if (p_rule(cur_node)) {
                req_node = cur_node;
                break;
            }

            if (cur_node->get_right() != nullptr) {
                cur_node = cur_node->get_right();
            }
            else {
                return nullptr;
            }
        }
        else {
            if (cur_node->get_left() != nullptr) {
                cur_node = cur_node->get_left();
            }
            else {
                return nullptr;
            }
        }
    }

    return req_node;
}


std::size_t kdtree::traverse(const kdnode::ptr & p_node) {
    std::size_t number_nodes = 0;

    if (p_node != nullptr) {
        if (p_node->get_left() != nullptr) {
            number_nodes += traverse(p_node->get_left());
        }

        if (p_node->get_right() != nullptr) {
            number_nodes += traverse(p_node->get_right());
        }

        number_nodes++;
    }

    return number_nodes;
}


kdnode::ptr kdtree::get_root() const {
    return m_root;
}


std::size_t kdtree::get_size() const {
    return m_size;
}


kdtree & kdtree::operator=(const kdtree & p_other) {
    if (this != &p_other) {
        m_root      = p_other.m_root;
        m_dimension = p_other.m_dimension;
        m_size      = p_other.m_size;
    }

    return *this;
}


kdtree & kdtree::operator=(kdtree && p_other) {
    if (this != &p_other) {
        m_root      = std::move(p_other.m_root);
        m_dimension = std::move(p_other.m_dimension);
        m_size      = std::move(p_other.m_size);
    }

    return *this;
}



kdtree_searcher::kdtree_searcher(const std::vector<double> & point, const kdnode::ptr & node, const double radius_search) {
    initialize(point, node, radius_search);
}


void kdtree_searcher::initialize(const std::vector<double> & point, const kdnode::ptr & node, const double radius_search) {
    m_distance = radius_search;
    m_sqrt_distance = radius_search * radius_search;

    m_initial_node = node;
    m_search_point = point;
}


void kdtree_searcher::recursive_nearest_nodes(const kdnode::ptr & node) const {
    double minimum = node->get_value() - m_distance;
    double maximum = node->get_value() + m_distance;

    if (node->get_right() != nullptr) {
        if (m_search_point[node->get_discriminator()] >= minimum) {
            recursive_nearest_nodes(node->get_right());
        }
    }

    if (node->get_left() != nullptr) {
        if (m_search_point[node->get_discriminator()] < maximum) {
            recursive_nearest_nodes(node->get_left());
        }
    }

    m_proc(node);
}


void kdtree_searcher::store_if_reachable(const kdnode::ptr & node) const {
    double candidate_distance = euclidean_distance_square(m_search_point, node->get_data());
    if (candidate_distance <= m_sqrt_distance) {
        m_nearest_nodes.push_back(node);
        m_nodes_distance.push_back(candidate_distance);
    }
}


void kdtree_searcher::store_best_if_reachable(const kdnode::ptr & node) const {
    double candidate_distance = euclidean_distance_square(m_search_point, node->get_data());
    if (candidate_distance <= m_nodes_distance[0]) {
        m_nearest_nodes[0] = node;
        m_nodes_distance[0] = candidate_distance;
    }
}


void kdtree_searcher::store_user_nodes_if_reachable(const kdnode::ptr & node) const {
    double candidate_distance = euclidean_distance_square(m_search_point, node->get_data());
    if (candidate_distance <= m_sqrt_distance) {
        m_user_rule(node, candidate_distance);
    }
}


void kdtree_searcher::find_nearest_nodes(std::vector<double> & p_distances, std::vector<kdnode::ptr> & p_nearest_nodes) const {
    m_proc = std::bind(&kdtree_searcher::store_if_reachable, this, std::placeholders::_1);
    recursive_nearest_nodes(m_initial_node);

    p_distances = std::move(m_nodes_distance);
    p_nearest_nodes = std::move(m_nearest_nodes);

    clear();
}


void kdtree_searcher::find_nearest(const rule_store & p_store_rule) const {
    m_proc = std::bind(&kdtree_searcher::store_user_nodes_if_reachable, this, std::placeholders::_1);
    m_user_rule = p_store_rule;
    recursive_nearest_nodes(m_initial_node);

    clear();
}


kdnode::ptr kdtree_searcher::find_nearest_node() const {
    m_nearest_nodes     = { nullptr };
    m_nodes_distance    = { std::numeric_limits<double>::max() };

    m_proc = std::bind(&kdtree_searcher::store_best_if_reachable, this, std::placeholders::_1);
    recursive_nearest_nodes(m_initial_node);

    kdnode::ptr node = m_nearest_nodes.front();

    clear();

    return node;
}


void kdtree_searcher::clear() const {
    m_nodes_distance    = { };
    m_nearest_nodes     = { };
    m_nearest_points    = { };

    m_user_rule = nullptr;
    m_proc      = nullptr;
}


}

}
