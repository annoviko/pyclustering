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

#include <pyclustering/cluster/clique_block.hpp>


namespace pyclustering {

namespace clst {


clique_spatial_block::clique_spatial_block(const point & p_max_corner, const point & p_min_corner) :
    m_max_corner(p_max_corner),
    m_min_corner(p_min_corner)
{ }


bool clique_spatial_block::contains(const point & p_point) const {
    for (std::size_t i = 0; i < p_point.size(); ++i) {
        if ((p_point[i] < m_min_corner[i]) || (p_point[i] > m_max_corner[i])) {
            return false;
        }
    }

    return true;
}

const point & clique_spatial_block::get_max_corner() const {
    return m_max_corner;
}

void clique_spatial_block::move_max_corner(point && p_corner) {
    m_max_corner = std::move(p_corner);
}

const point & clique_spatial_block::get_min_corner() const {
    return m_min_corner;
}

void clique_spatial_block::move_min_corner(point && p_corner) {
    m_min_corner = std::move(p_corner);
}



clique_block::clique_block(const clique_block_location & p_location, const clique_spatial_block & p_block) :
    m_logical_location(p_location),
    m_spatial_location(p_block),
    m_points(),
    m_visited(false)
{ }


clique_block::clique_block(clique_block_location && p_location, clique_spatial_block && p_block) :
    m_logical_location(std::move(p_location)),
    m_spatial_location(std::move(p_block)),
    m_points(),
    m_visited(false)
{ }


const clique_block_location & clique_block::get_logical_location() const {
    return m_logical_location;
}

const clique_spatial_block & clique_block::get_spatial_block() const {
    return m_spatial_location;
}

const clique_block::content & clique_block::get_points() const {
    return m_points;
}

bool clique_block::is_visited() const {
    return m_visited;
}

void clique_block::touch() {
    m_visited = true;
}

void clique_block::capture_points(const dataset & p_data, std::vector<bool> & p_availability) {
    for (std::size_t index_point = 0; index_point < p_data.size(); ++index_point) {
        if (p_availability[index_point] && m_spatial_location.contains(p_data[index_point])) {
            m_points.push_back(index_point);
            p_availability[index_point] = false;
        }
    }
}

void clique_block::get_location_neighbors(const std::size_t p_edge, std::vector<clique_block_location> & p_neighbors) const {
    for (std::size_t index_dimension = 0; index_dimension < m_logical_location.size(); ++index_dimension) {
        if (m_logical_location[index_dimension] + 1 < p_edge) {
            clique_block_location position = m_logical_location;
            ++position[index_dimension];
            p_neighbors.push_back(position);
        }

        if (m_logical_location[index_dimension] != 0) {
            clique_block_location position = m_logical_location;
            --position[index_dimension];
            p_neighbors.push_back(position);
        }
    }
}

}

}