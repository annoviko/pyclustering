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

#include "cluster/kmedoids_data.hpp"


namespace cluster_analysis {


kmedoids_data::kmedoids_data(void) :
        cluster_data(),
        m_medoids(new medoid_sequence())
{ }


kmedoids_data::kmedoids_data(const kmedoids_data & p_other) :
        cluster_data(p_other),
        m_medoids(p_other.m_medoids)
{ }


kmedoids_data::kmedoids_data(kmedoids_data && p_other) :
        cluster_data(p_other),
        m_medoids(std::move(p_other.m_medoids))
{ }


kmedoids_data::~kmedoids_data(void) { }


medoid_sequence_ptr kmedoids_data::medoids(void) { return m_medoids; }


}
