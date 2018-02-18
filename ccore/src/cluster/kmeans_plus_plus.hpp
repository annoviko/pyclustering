/**
*
* Copyright (C) 2014-2018    Andrei Novikov (pyclustering@yandex.ru)
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


#include "definitions.hpp"

#include "utils/metric.hpp"


using namespace ccore::utils::metric;


namespace ccore {

namespace clst {


class kmeans_plus_plus {
private:
    using distance_solver = distance_functor< std::vector<double> >;

private:
    std::size_t         m_amount        = 0;
    distance_solver     m_dist_func;

public:
    kmeans_plus_plus(void) = default;

    kmeans_plus_plus(const std::size_t p_amount);

    kmeans_plus_plus(const std::size_t p_amount, const distance_solver & p_functor);

    kmeans_plus_plus(const kmeans_plus_plus & p_other) = default;

    kmeans_plus_plus(kmeans_plus_plus && p_other) = default;

    ~kmeans_plus_plus(void) = default;

public:
    void initialize(const dataset & p_data, dataset & p_centers) const;

private:
    point get_first_center(const dataset & p_data) const;

    point get_next_center(const dataset & p_data, const dataset & p_centers) const;

    void calculate_shortest_distances(const dataset & p_data,
                                      const dataset & p_centers,
                                      std::vector<double> & p_distances) const;
};


}

}
