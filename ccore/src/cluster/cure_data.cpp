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

#include "cluster/cure_data.hpp"


namespace cluster_analysis {


cure_data::cure_data(void) :
        cluster_data(),
        m_representative_sequence(new representor_sequence()),
        m_mean_sequence(new dataset())
{ }


cure_data::cure_data(const cure_data & p_other) :
        cluster_data(p_other),
        m_representative_sequence(p_other.m_representative_sequence),
        m_mean_sequence(p_other.m_mean_sequence)
{ }


cure_data::cure_data(cure_data && p_other) :
        cluster_data(p_other),
        m_representative_sequence(std::move(p_other.m_representative_sequence)),
        m_mean_sequence(std::move(p_other.m_mean_sequence))
{ }


cure_data::~cure_data(void) { }


representor_sequence_ptr cure_data::representors(void) {
    return m_representative_sequence;
}


dataset_ptr cure_data::means(void) {
    return m_mean_sequence;
}


}
