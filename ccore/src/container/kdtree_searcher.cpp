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

#include <pyclustering/container/kdtree_searcher.hpp>

#include <pyclustering/utils/metric.hpp>


using namespace pyclustering::utils::metric;


namespace pyclustering {

namespace container {


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
    m_nearest_nodes = { nullptr };
    m_nodes_distance = { std::numeric_limits<double>::max() };

    m_proc = std::bind(&kdtree_searcher::store_best_if_reachable, this, std::placeholders::_1);
    recursive_nearest_nodes(m_initial_node);

    kdnode::ptr node = m_nearest_nodes.front();

    clear();

    return node;
}


void kdtree_searcher::clear() const {
    m_nodes_distance = {};
    m_nearest_nodes = {};
    m_nearest_points = {};

    m_user_rule = nullptr;
    m_proc = nullptr;
}


}

}