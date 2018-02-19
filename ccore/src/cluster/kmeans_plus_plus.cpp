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
#include <limits>
#include <random>
#include <string>


namespace ccore {

namespace clst {


const std::size_t kmeans_plus_plus::FARTHEST_CENTER_CANDIDATE = std::numeric_limits<std::size_t>::max();


kmeans_plus_plus::kmeans_plus_plus(const std::size_t p_amount, const std::size_t p_candidates) noexcept :
        m_amount(p_amount),
        m_candidates(p_candidates)
{
    m_dist_func = [](const point &p1, const point &p2) {
        return euclidean_distance_square(p1, p2);
    };
}


kmeans_plus_plus::kmeans_plus_plus(const std::size_t p_amount, const std::size_t p_candidates, const metric & p_functor) noexcept :
        m_amount(p_amount),
        m_candidates(p_candidates),
        m_dist_func(p_functor)
{ }


void kmeans_plus_plus::initialize(const dataset & p_data, dataset & p_centers) const {
    initialize(p_data, { }, p_centers);
}


void kmeans_plus_plus::initialize(const dataset & p_data,
                                  const index_sequence & p_indexes,
                                  dataset & p_centers) const
{
    p_centers.clear();

    if (!m_amount) { return; }

    p_centers.reserve(m_amount);

    if (p_data.empty()) {
        throw std::invalid_argument("Input data is empty.");
    }

    if (p_data.size() < m_amount) {
        throw std::invalid_argument("Amount of objects should be equal or greater then amount of initialized centers.");
    }

    if (!p_indexes.empty() && p_indexes.size() < m_amount) {
        throw std::invalid_argument("Amount of objects defined by range should be equal or greater then amount of initialized centers.");
    }

    p_centers.push_back(get_first_center(p_data, p_indexes));

    for (std::size_t i = 1; i < m_amount; i++) {
        p_centers.push_back(get_next_center(p_data, p_centers, p_indexes));
    }
}


point kmeans_plus_plus::get_first_center(const dataset & p_data, const index_sequence & p_indexes) const {
    std::size_t length = p_indexes.empty() ? p_data.size() : p_indexes.size();

    std::default_random_engine generator;
    std::uniform_int_distribution<std::size_t> distribution(0, length - 1);

    std::size_t index = distribution(generator);
    return p_indexes.empty() ? p_data[index] : p_data[ p_indexes[index] ];
}


point kmeans_plus_plus::get_next_center(const dataset & p_data,
                                        const dataset & p_centers,
                                        const index_sequence & p_indexes) const
{
    std::vector<double> distances;
    calculate_shortest_distances(p_data, p_centers, p_indexes, distances);

    auto iter = std::max_element(distances.begin(), distances.end());
    std::size_t index = std::distance(distances.begin(), iter);

    return p_indexes.empty() ? p_data[index] : p_data[ p_indexes[index] ];
}


void kmeans_plus_plus::calculate_shortest_distances(const dataset & p_data,
                                                    const dataset & p_centers,
                                                    const index_sequence & p_indexes,
                                                    std::vector<double> & p_distances) const
{
    p_distances.reserve(p_data.size());

    if (p_indexes.empty())
    {
        for (auto & point : p_data) {
            double shortest_distance = get_shortest_distance(point, p_centers);
            p_distances.push_back(shortest_distance);
        }
    }
    else {
        for (auto index : p_indexes) {
            double shortest_distance = get_shortest_distance(p_data[index], p_centers);
            p_distances.push_back(shortest_distance);
        }
    }

}


double kmeans_plus_plus::get_shortest_distance(const point & p_point, const dataset & p_centers) const {
    double shortest_distance = std::numeric_limits<double>::max();
    for (auto & center : p_centers) {
        double distance = m_dist_func(p_point, center);
        if (distance < shortest_distance) {
            shortest_distance = distance;
        }
    }

    return shortest_distance;
}


}

}

