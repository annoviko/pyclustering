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


#include <pyclustering/cluster/kmeans_plus_plus.hpp>

#include <algorithm>
#include <chrono>
#include <exception>
#include <limits>
#include <numeric>
#include <random>
#include <string>


namespace pyclustering {

namespace clst {


const std::size_t kmeans_plus_plus::FARTHEST_CENTER_CANDIDATE = std::numeric_limits<std::size_t>::max();
const std::size_t kmeans_plus_plus::INVALID_INDEX = std::numeric_limits<std::size_t>::max();


kmeans_plus_plus::kmeans_plus_plus(const std::size_t p_amount, const std::size_t p_candidates) noexcept :
        m_amount(p_amount),
        m_candidates(p_candidates),
        m_dist_func([](const point &p1, const point &p2) {
            return euclidean_distance_square(p1, p2);
        })
{ }


kmeans_plus_plus::kmeans_plus_plus(const std::size_t p_amount, const std::size_t p_candidates, const metric & p_metric) noexcept :
        m_amount(p_amount),
        m_candidates(p_candidates),
        m_dist_func(p_metric)
{ }


void kmeans_plus_plus::initialize(const dataset & p_data, dataset & p_centers) const {
    initialize(p_data, { }, p_centers);
}


void kmeans_plus_plus::initialize(const dataset & p_data, index_sequence & p_center_indexes) const {
    p_center_indexes.clear();
    p_center_indexes.reserve(m_amount);

    initialize(p_data, { }, [&p_center_indexes](center_description & p_center) { 
        p_center_indexes.push_back(std::get<INDEX>(p_center));
    });
}


void kmeans_plus_plus::initialize(const dataset & p_data,
                                  const index_sequence & p_indexes,
                                  dataset & p_centers) const
{
    p_centers.clear();
    p_centers.reserve(m_amount);

    initialize(p_data, p_indexes, [&p_centers](center_description & p_center) { 
        p_centers.push_back(std::move(std::get<POINT>(p_center)));
    });
}


void kmeans_plus_plus::initialize(const dataset & p_data, const index_sequence & p_indexes, const store_result & p_proc) const {
    if (!m_amount) { return; }

    store_temporal_params(p_data, p_indexes);

    auto center = get_first_center();
    store_center(p_proc, center);

    for (std::size_t i = 1; i < m_amount; i++) {
        center = get_next_center();
        store_center(p_proc, center);
    }

    free_temporal_params();
}


void kmeans_plus_plus::store_center(const store_result & p_proc, center_description & p_result) const {
    m_allocated_indexes.push_back(std::get<INDEX>(p_result));
    m_free_indexes.erase(std::get<INDEX>(p_result));
    p_proc(p_result);
}


void kmeans_plus_plus::store_temporal_params(const dataset & p_data, const index_sequence & p_indexes) const {
    if (p_data.empty()) {
        throw std::invalid_argument("Input data is empty.");
    }

    if (p_data.size() < m_amount) {
        throw std::invalid_argument("Amount of objects should be equal or greater then amount of initialized centers.");
    }

    if (!p_indexes.empty() && p_indexes.size() < m_amount) {
        throw std::invalid_argument("Amount of objects defined by range should be equal or greater then amount of initialized centers.");
    }

    m_data_ptr      = (dataset *) &p_data;
    m_indexes_ptr   = (index_sequence *) &p_indexes;

    m_allocated_indexes.clear();
    m_free_indexes.clear();

    if (m_indexes_ptr->empty())
    {
        for (std::size_t i = 0; i < m_data_ptr->size(); i++) {
            m_free_indexes.insert(i);
        }
    }
    else {
        for (const auto index : *m_indexes_ptr) {
            m_free_indexes.insert(index);
        }
    }
}


void kmeans_plus_plus::free_temporal_params() const {
    m_data_ptr      = nullptr;
    m_indexes_ptr   = nullptr;
}


kmeans_plus_plus::center_description kmeans_plus_plus::get_first_center() const {
    std::size_t length = m_indexes_ptr->empty() ? m_data_ptr->size() : m_indexes_ptr->size();

    std::random_device random_device;

    std::mt19937 generator(random_device());
    generator.seed(static_cast<unsigned int>(std::chrono::system_clock::now().time_since_epoch().count()));

    std::uniform_int_distribution<std::size_t> distribution(0, length - 1);

    std::size_t index = distribution(generator);
    const auto & center = m_indexes_ptr->empty() ? (*m_data_ptr)[index] : (*m_data_ptr)[ (*m_indexes_ptr)[index] ];

    return std::make_tuple(center, index);
}


kmeans_plus_plus::center_description kmeans_plus_plus::get_next_center() const
{
    std::vector<double> distances;
    calculate_shortest_distances(distances);

    std::size_t index = 0;
    if (m_candidates == FARTHEST_CENTER_CANDIDATE) {
        auto iter = std::max_element(distances.begin(), distances.end());
        index = std::distance(distances.begin(), iter);
    }
    else {
        std::vector<double> probabilities;
        calculate_probabilities(distances, probabilities);
        index = get_probable_center(distances, probabilities);
    }

    const auto & center = m_indexes_ptr->empty() ? (*m_data_ptr)[index] : (*m_data_ptr)[ (*m_indexes_ptr)[index] ];
    return std::make_tuple(center, index);
}


void kmeans_plus_plus::calculate_shortest_distances(std::vector<double> & p_distances) const
{
    p_distances.reserve(m_data_ptr->size());

    if (m_indexes_ptr->empty())
    {
        for (auto & point : (*m_data_ptr)) {
            double shortest_distance = get_shortest_distance(point);
            p_distances.push_back(shortest_distance);
        }
    }
    else {
        for (auto index : (*m_indexes_ptr)) {
            double shortest_distance = get_shortest_distance((*m_data_ptr)[index]);
            p_distances.push_back(shortest_distance);
        }
    }

}


double kmeans_plus_plus::get_shortest_distance(const point & p_point) const {
    double shortest_distance = std::numeric_limits<double>::max();
    for (auto & index_point : m_allocated_indexes) {
        double distance = std::abs(m_dist_func(p_point, m_data_ptr->at(index_point)));
        if (distance < shortest_distance) {
            shortest_distance = distance;
        }
    }

    return shortest_distance;
}


void kmeans_plus_plus::calculate_probabilities(const std::vector<double> & p_distances, std::vector<double> & p_probabilities) const {
    double sum = std::accumulate(p_distances.begin(), p_distances.end(), 0.0);

    p_probabilities.reserve(m_data_ptr->size());
    double previous_probability = 0.0;
    for (auto distance : p_distances) {
        double current_probability = distance / sum;

        p_probabilities.push_back( current_probability + previous_probability );

        previous_probability += current_probability;
    }

    p_probabilities.back() = 1.0;
}


std::size_t kmeans_plus_plus::get_probable_center(const std::vector<double> & p_distances, const std::vector<double> & p_probabilities) const {
    std::default_random_engine generator;
    generator.seed(static_cast<unsigned int>(std::chrono::system_clock::now().time_since_epoch().count()));

    std::uniform_real_distribution<double> distribution(0.0, 1.0);

    std::size_t best_index_candidate = 0;
    for (std::size_t i = 0; i < m_candidates; i++) {
        std::size_t current_index_candidate = kmeans_plus_plus::INVALID_INDEX;
        double candidate_probability = distribution(generator);
        for (std::size_t j = 0; j < p_probabilities.size(); j++) {
            if (candidate_probability < p_probabilities[j]) {
                current_index_candidate = j;
                break;
            }
        }

        if (current_index_candidate == kmeans_plus_plus::INVALID_INDEX) {
            best_index_candidate = *(m_free_indexes.begin());
        }
        else if (p_distances[current_index_candidate] > p_distances[best_index_candidate]) {
            best_index_candidate = current_index_candidate;
        }
    }

    return best_index_candidate;
}


}

}

