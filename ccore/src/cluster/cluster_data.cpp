/**
*
* Copyright (C) 2014-2016    Andrei Novikov (pyclustering@yandex.ru)
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

#include "cluster_data.hpp"


namespace cluster_analysis {


cluster_data::cluster_data(void) : m_clusters(new cluster_sequence()) { }


cluster_data::cluster_data(const cluster_data & p_other) : m_clusters(p_other.m_clusters) { }


cluster_data::cluster_data(cluster_data && p_other) : m_clusters(std::move(p_other.m_clusters)) { }


cluster_data::~cluster_data(void) { }


cluster_sequence_ptr cluster_data::clusters(void) { return m_clusters; }


size_t cluster_data::size(void) const { return m_clusters->size(); }


cluster & cluster_data::operator[](const size_t p_index) { return (*m_clusters)[p_index]; }


const cluster & cluster_data::operator[](const size_t p_index) const { return (*m_clusters)[p_index]; }


cluster_data & cluster_data::operator=(const cluster_data & p_other) {
    if (this != &p_other) {
        m_clusters = p_other.m_clusters;
    }

    return *this;
}


cluster_data & cluster_data::operator=(cluster_data && p_other) {
    if (this != &p_other) {
        m_clusters = std::move(p_other.m_clusters);
    }

    return *this;
}


bool cluster_data::operator==(const cluster_data & p_other) const {
    return (m_clusters == p_other.m_clusters);
}


bool cluster_data::operator!=(const cluster_data & p_other) const {
    return !(*this == p_other);
}


}
