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


#include <pyclustering/cluster/random_center_initializer.hpp>

#include <chrono>
#include <random>


namespace pyclustering {

namespace clst {


random_center_initializer::random_center_initializer(const std::size_t p_amount) :
    m_amount(p_amount)
{ }


void random_center_initializer::initialize(const dataset & p_data, dataset & p_centers) const {
    initialize(p_data, { }, p_centers);
}


void random_center_initializer::initialize(const dataset & p_data, const index_sequence & p_indexes, dataset & p_centers) const {
    p_centers.clear();
    p_centers.reserve(m_amount);

    if ((m_amount > p_data.size()) || (m_amount == 0)) {
        return;
    }

    m_available_indexes.reserve(p_data.size());
    for (std::size_t i = 0; i < p_data.size(); i++) {
        m_available_indexes.insert(i);
    }

    if (m_amount == p_data.size()) {
        p_centers = p_data;
        return;
    }

    for (std::size_t i = 0; i < m_amount; i++) {
        create_center(p_data, p_centers);
    }
}


void random_center_initializer::create_center(const dataset & p_data, dataset & p_centers) const {
    std::random_device random_device;

    std::mt19937 engine(random_device());
    engine.seed(static_cast<unsigned int>(std::chrono::system_clock::now().time_since_epoch().count()));

    std::uniform_int_distribution<std::size_t> distribution(0, p_data.size() - 1);

    std::size_t random_index_point = distribution(engine);
    index_storage::iterator available_index = m_available_indexes.find(random_index_point);
    if (available_index == m_available_indexes.end()) {
        random_index_point = *m_available_indexes.begin();
        available_index = m_available_indexes.begin();
    }

    p_centers.push_back(p_data.at(random_index_point));
    m_available_indexes.erase(available_index);
}


}

}