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

#include "cluster/clique.hpp"


namespace ccore {

namespace clst {


coordinate_iterator::coordinate_iterator(const std::size_t p_dimension, const std::size_t p_edge) :
    m_dimension(p_dimension),
    m_edge(p_edge),
    m_coordinate(p_dimension, std::size_t(0))
{ }

const clique_block_location & coordinate_iterator::get_coordinate(void) const {
    return m_coordinate;
}

clique_block_location & coordinate_iterator::get_coordinate(void) {
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
}


void clique::create_grid(void) {

}


}

}