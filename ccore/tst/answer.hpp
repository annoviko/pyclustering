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


#include <vector>


using cluster = std::vector<std::size_t>;
using cluster_sequence = std::vector<cluster>;

using length_sequence = std::vector<std::size_t>;


class answer {
private:
    cluster_sequence m_clusters;
    length_sequence  m_cluster_lengths;
    cluster          m_noise;

public:
    const cluster_sequence & clusters(void) const { return m_clusters; }

    cluster_sequence & clusters(void) { return m_clusters; }

    const length_sequence & cluster_lengths(void) const { return m_cluster_lengths; }

    length_sequence & cluster_lengths(void) { return m_cluster_lengths; }

    const cluster & noise(void) const { return m_noise; }

    cluster & noise(void) { return m_noise; }
};