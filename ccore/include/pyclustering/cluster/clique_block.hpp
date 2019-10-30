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

#pragma once


#include <pyclustering/definitions.hpp>

#include <list>
#include <vector>


namespace pyclustering {

namespace clst {


using clique_block_location = std::vector<std::size_t>;


class clique_spatial_block {
private:
    point   m_max_corner;
    point   m_min_corner;

public:
    clique_spatial_block() = default;
    clique_spatial_block(const point & p_max_corner, const point & p_min_corner);

public:
    bool contains(const point & p_point) const;

    const point & get_max_corner() const;

    void move_max_corner(point && p_corner);

    const point & get_min_corner() const;

    void move_min_corner(point && p_corner);
};


class clique_block {
public:
    using content   = std::list<std::size_t>;

private:
    clique_block_location     m_logical_location;
    clique_spatial_block      m_spatial_location;
    content                   m_points;
    bool                      m_visited = false;

public:
    clique_block(const clique_block_location & p_location, const clique_spatial_block & p_block);

    clique_block(clique_block_location && p_location, clique_spatial_block && p_block);

public:
    const clique_block_location & get_logical_location() const;

    const clique_spatial_block & get_spatial_block() const;

    const clique_block::content & get_points() const;

    bool is_visited() const;

    void touch();

    void capture_points(const dataset & p_data, std::vector<bool> & p_availability);

    void get_location_neighbors(const std::size_t p_edge, std::vector<clique_block_location> & p_neighbors) const;
};


}

}