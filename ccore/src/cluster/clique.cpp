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

#include <pyclustering/cluster/clique.hpp>

#include <cmath>


namespace pyclustering {

namespace clst {


coordinate_iterator::coordinate_iterator(const std::size_t p_dimension, const std::size_t p_edge) :
    m_dimension(p_dimension),
    m_edge(p_edge),
    m_coordinate(p_dimension, std::size_t(0))
{ }

const clique_block_location & coordinate_iterator::get_coordinate() const noexcept {
    return m_coordinate;
}

clique_block_location & coordinate_iterator::get_coordinate() noexcept {
    return m_coordinate;
}

coordinate_iterator & coordinate_iterator::operator++() {
    for (std::size_t index_dimension = 0; index_dimension < m_dimension; ++index_dimension) {
        if (m_coordinate[index_dimension] + 1 < m_edge) {
            ++m_coordinate[index_dimension];
            return *this;
        }
        else {
            m_coordinate[index_dimension] = 0;
        }
    }

    m_coordinate = clique_block_location(m_dimension, 0);
    return *this;
}


clique::clique(const std::size_t p_intervals, const std::size_t p_threshold) :
    m_intervals(p_intervals),
    m_density_threshold(p_threshold)
{ }


void clique::process(const dataset & p_data, cluster_data & p_result) {
    m_data_ptr   = &p_data;
    m_result_ptr = dynamic_cast<clique_data *>(&p_result);

    create_grid();

    for (auto & block : m_result_ptr->blocks()) {
        if (!block.is_visited()) {
            expand_cluster(block);
        }
    }

    m_cells_map.clear();
}


void clique::expand_cluster(clique_block & p_block) {
    p_block.touch();

    const auto & points = p_block.get_points();
    if (points.size() <= m_density_threshold) {
        if (!points.empty()) {
            m_result_ptr->noise().insert(m_result_ptr->noise().end(), points.begin(), points.end());
        }

        return;
    }

    m_result_ptr->clusters().push_back({ });
    cluster & cur_cluster = m_result_ptr->clusters().back();
    cur_cluster.insert(cur_cluster.end(), p_block.get_points().begin(), p_block.get_points().end());

    std::list<clique_block *> neighbors;
    get_neighbors(p_block, neighbors);

    for (clique_block * neighbor : neighbors) {
        const auto & points = neighbor->get_points();
        if (points.size() > m_density_threshold) {
            cur_cluster.insert(cur_cluster.end(), points.begin(), points.end());
            get_neighbors(*neighbor, neighbors);
        }
        else if (!points.empty()) {
            m_result_ptr->noise().insert(m_result_ptr->noise().end(), points.begin(), points.end());
        }
    }
}


void clique::get_neighbors(const clique_block & p_block, std::list<clique_block *> & p_neighbors) const {
    std::vector<clique_block_location> location_neighbors;
    p_block.get_location_neighbors(m_intervals, location_neighbors);

    for (const auto & location : location_neighbors) {
        const std::string key = location_to_key(location);
        clique_block * candidate = m_cells_map.at(key);

        if (!candidate->is_visited()) {
            candidate->touch();
            p_neighbors.push_back(candidate);
        }
    }
}


void clique::create_grid() {
    clique::data_info info;
    get_data_info(info);

    const std::size_t dimension = m_data_ptr->at(0).size();
    const auto amount_blocks = static_cast<std::size_t>(std::pow(m_intervals, dimension));

    auto & blocks = m_result_ptr->blocks();
    blocks.reserve(amount_blocks);

    auto iterator = coordinate_iterator(dimension, m_intervals);

    std::vector<bool> point_availability(m_data_ptr->size(), true);

    for (std::size_t i = 0; i < amount_blocks; ++i) {
        clique_block_location logical_location = iterator.get_coordinate();
        ++iterator;

        clique_spatial_block spatial_block;
        get_spatial_location(logical_location, info, spatial_block);

        clique_block cell(logical_location, std::move(spatial_block));
        cell.capture_points(*m_data_ptr, point_availability);

        blocks.push_back(std::move(cell));

        m_cells_map.insert({ location_to_key(blocks.back().get_logical_location()), &(blocks.back()) });
    }
}


std::string clique::location_to_key(const clique_block_location & p_location) {
    std::string result;
    for (const auto coordinate : p_location) {
        result += std::to_string(coordinate) + '.';
    }

    return result;
}


void clique::get_spatial_location(const clique_block_location & p_location, const clique::data_info & p_info, clique_spatial_block & p_block) const {
    point min_corner = p_info.m_min_corner;
    point max_corner = p_info.m_max_corner;

    const std::size_t dimension = m_data_ptr->at(0).size();
    std::vector<double> cell_sizes(dimension, 0.0);

    for (std::size_t i = 0; i < cell_sizes.size(); ++i) {
        cell_sizes[i] = p_info.m_sizes[i] / m_intervals;
    }

    for (std::size_t index_dimension = 0; index_dimension < dimension; ++index_dimension) {
        min_corner[index_dimension] += cell_sizes[index_dimension] * p_location[index_dimension];

        if (p_location[index_dimension] == m_intervals - 1) {
            max_corner[index_dimension] = p_info.m_max_corner[index_dimension];
        }
        else {
            max_corner[index_dimension] = min_corner[index_dimension] + cell_sizes[index_dimension];
        }
    }

    p_block.move_max_corner(std::move(max_corner));
    p_block.move_min_corner(std::move(min_corner));
}


void clique::get_data_info(clique::data_info & p_info) const {
    p_info.m_min_corner = m_data_ptr->at(0);
    p_info.m_max_corner = p_info.m_min_corner;

    const std::size_t dimension = p_info.m_min_corner.size();
    const dataset & data = *m_data_ptr;

    for (const auto & data_point : data) {
        for (std::size_t index_dimension = 0; index_dimension < dimension; ++index_dimension) {
            const double coordinate = data_point[index_dimension];
            if (coordinate > p_info.m_max_corner[index_dimension]) {
                p_info.m_max_corner[index_dimension] = coordinate;
            }

            if (coordinate < p_info.m_min_corner[index_dimension]) {
                p_info.m_min_corner[index_dimension] = coordinate;
            }
        }
    }

    for (std::size_t index_dimension = 0; index_dimension < dimension; ++index_dimension) {
        p_info.m_sizes.push_back(p_info.m_max_corner[index_dimension] - p_info.m_min_corner[index_dimension]);
    }
}


}

}