/*!

@authors Andrei Novikov (pyclustering@yandex.ru)
@date 2014-2020
@copyright GNU Public License

@cond GNU_PUBLIC_LICENSE
pyclustering is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

pyclustering is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
@endcond

*/


#include <pyclustering/cluster/silhouette_ksearch_data.hpp>

#include <cmath>


namespace pyclustering {

namespace clst {


const std::size_t silhouette_ksearch_data::get_amount() const { 
    return m_amount;
}


void silhouette_ksearch_data::set_amount(const std::size_t p_amount) {
    m_amount = p_amount;
}


const double silhouette_ksearch_data::get_score() const {
    return m_score;
}


void silhouette_ksearch_data::set_score(const double p_score) {
    m_score = p_score;
}


const silhouette_score_sequence & silhouette_ksearch_data::scores() const {
    return m_scores;
}


silhouette_score_sequence & silhouette_ksearch_data::scores() {
    return m_scores;
}


bool silhouette_ksearch_data::operator==(const silhouette_ksearch_data & p_other) const {
    if (this == &p_other) {
        return true;
    }

    if ((m_amount != p_other.m_amount) || (m_score != p_other.m_score) || (m_scores.size() != p_other.m_scores.size())) {
        return false;
    }

    for (std::size_t i = 0; i < m_scores.size(); i++) {
        if (std::isnan(m_scores[i]) && std::isnan(p_other.m_scores[i])) {
            continue;
        }
        else if (m_scores[i] == p_other.m_scores[i]) {
            continue;
        }

        return false;
    }

    return true;
}


}

}