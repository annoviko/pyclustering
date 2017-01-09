/**
*
* Copyright (C) 2014-2017    Andrei Novikov (pyclustering@yandex.ru)
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


#include "cluster/dbscan_data.hpp"


namespace cluster_analysis {


using ordering = std::vector<double>;
using ordering_ptr = std::shared_ptr<ordering>;


class optics_data : public dbscan_data {
private:
    ordering_ptr     m_ordering;

public:
    optics_data(void) = default;

    optics_data(const optics_data & p_other) = default;

    optics_data(optics_data && p_other) = default;

    virtual ~optics_data(void) = default;

public:
    inline ordering_ptr ordering(void) { return m_ordering; }
};


}