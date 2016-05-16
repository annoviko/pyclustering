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

#include "cluster/kmedians_data.hpp"


namespace cluster_analysis {


kmedians_data::kmedians_data(void) :
        cluster_data(),
        m_medians(new dataset())
{ }


kmedians_data::kmedians_data(const kmedians_data & p_other) :
        cluster_data(p_other),
        m_medians(p_other.m_medians)
{ }


kmedians_data::kmedians_data(kmedians_data && p_other) :
        cluster_data(p_other),
        m_medians(std::move(p_other.m_medians))
{ }


kmedians_data::~kmedians_data(void) { }


dataset_ptr kmedians_data::medians(void) { return m_medians; }


}
