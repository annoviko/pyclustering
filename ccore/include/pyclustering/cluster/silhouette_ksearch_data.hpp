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

#pragma once


#include <pyclustering/definitions.hpp>


namespace pyclustering {

namespace clst {


using silhouette_score_sequence = std::vector<double>;


class silhouette_ksearch_data {
private:
    std::size_t m_amount = 0;
    double      m_score  = 0;
    silhouette_score_sequence m_scores = { };

public:
    const std::size_t get_amount() const { return m_amount; }

    void set_amount(const std::size_t p_amount) { m_amount = p_amount; }

    const double get_score() const { return m_score; }

    void set_score(const double p_score) { m_score = p_score; }

    const silhouette_score_sequence & scores() const { return m_scores; }

    silhouette_score_sequence & scores() { return m_scores; }
};


}

}