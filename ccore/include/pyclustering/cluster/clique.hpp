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

#include <pyclustering/cluster/clique_data.hpp>
#include <pyclustering/cluster/cluster_algorithm.hpp>

#include <list>
#include <unordered_map>


namespace pyclustering {

namespace clst {


class coordinate_iterator {
private:
    std::size_t m_dimension = 0;
    std::size_t m_edge      = 0;
    clique_block_location m_coordinate;

public:
    coordinate_iterator(const std::size_t p_dimension, const std::size_t p_edge);

public:
    const clique_block_location & get_coordinate() const noexcept;
    clique_block_location & get_coordinate() noexcept;

public:
    coordinate_iterator & operator++();
};


class clique : public cluster_algorithm {
private:
    struct data_info {
        point m_min_corner;
        point m_max_corner;
        std::vector<double> m_sizes;
    };

private:
    using block_map = std::unordered_map<std::string, clique_block *>;

private:
    std::size_t     m_intervals         = 0;
    std::size_t     m_density_threshold = 0;

    const dataset * m_data_ptr      = nullptr;
    clique_data *   m_result_ptr    = nullptr;

    block_map       m_cells_map;

public:
    clique(const std::size_t p_intervals, const std::size_t p_threshold);

public:
    virtual void process(const dataset & p_data, cluster_data & p_result) override;

private:
    void create_grid();

    void expand_cluster(clique_block & p_block);

    void get_neighbors(const clique_block & p_block, std::list<clique_block *> & p_neighbors) const;

    void get_spatial_location(const clique_block_location & p_location, const clique::data_info & p_info, clique_spatial_block & p_block) const;

    void get_data_info(clique::data_info & p_info) const;

    static std::string location_to_key(const clique_block_location & p_location);
};

}

}
