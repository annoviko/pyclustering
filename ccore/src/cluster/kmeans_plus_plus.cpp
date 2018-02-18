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


#include "cluster/kmeans_plus_plus.hpp"

#include <algorithm>
#include <exception>
#include <random>
#include <string>


namespace ccore {

namespace clst {


kmeans_plus_plus::kmeans_plus_plus(const std::size_t p_amount) :
        m_amount(p_amount)
{
    m_dist_func = [](const point &p1, const point &p2) {
        return euclidean_distance_square(p1, p2);
    };
}


kmeans_plus_plus::kmeans_plus_plus(const std::size_t p_amount, const metric & p_functor) :
        m_amount(p_amount),
        m_dist_func(p_functor)
{ }


void kmeans_plus_plus::initialize(const dataset & p_data, dataset & p_centers) const {
    p_centers.clear();

    if (!m_amount) { return; }

    p_centers.reserve(m_amount);

    if (p_data.empty()) {
        throw std::invalid_argument("Input data is empty.");
    }

    if (p_data.size() < m_amount) {
        throw std::invalid_argument("Amount of object ("
                + std::to_string(p_data.size()) +
                ") should be equal or greater then amount of initialized centers ("
                + std::to_string(m_amount) + ").");
    }

    p_centers.push_back(get_first_center(p_data));

    for (std::size_t i = 1; i < m_amount; i++) {
        p_centers.push_back(get_next_center(p_data, p_centers));
    }
}


point kmeans_plus_plus::get_first_center(const dataset & p_data) const {
    std::default_random_engine generator;
    std::uniform_int_distribution<std::size_t> distribution(0, p_data.size() - 1);
    return p_data[ distribution(generator) ];
}


point kmeans_plus_plus::get_next_center(const dataset & p_data, const dataset & p_centers) const {
    std::vector<double> distances;
    calculate_shortest_distances(p_data, p_centers, distances);

    auto iter = std::max_element(distances.begin(), distances.end());
    std::size_t index = std::distance(distances.begin(), iter);

    return p_data[index];
}


void kmeans_plus_plus::calculate_shortest_distances(const dataset & p_data,
                                                    const dataset & p_centers,
                                                    std::vector<double> & p_distances) const
{
    p_distances.reserve(p_data.size());

    for (auto & point : p_data) {
        double shortest_distance = std::numeric_limits<double>::max();
        for (auto & center : p_centers) {
            double distance = m_dist_func(point, center);
            if (distance < shortest_distance) {
                shortest_distance = distance;
            }
        }

        p_distances.push_back(shortest_distance * shortest_distance);
    }
}


}

}

