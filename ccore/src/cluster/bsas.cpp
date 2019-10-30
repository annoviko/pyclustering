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


#include <pyclustering/cluster/bsas.hpp>


namespace pyclustering {

namespace clst {


bsas::bsas(const std::size_t p_amount,
           const double p_threshold,
           const distance_metric<point> & p_metric) :
    m_threshold(p_threshold),
    m_amount(p_amount),
    m_metric(p_metric)
{ }


void bsas::process(const dataset & p_data, cluster_data & p_result) {
    m_result_ptr = (bsas_data *) &p_result;

    cluster_sequence & clusters = m_result_ptr->clusters();
    representative_sequence & representatives = m_result_ptr->representatives();

    clusters.push_back({ 0 });
    representatives.push_back( p_data[0] );

    for (std::size_t i = 1; i < p_data.size(); i++) {
        auto nearest = find_nearest_cluster(p_data[i]);

        if ( (nearest.m_distance > m_threshold) && (clusters.size() < m_amount) ) {
            representatives.push_back(p_data[i]);
            clusters.push_back({ i });
        }
        else {
            clusters[nearest.m_index].push_back(i);
            update_representative(nearest.m_index, p_data[i]);
        }
    }
}


bsas::nearest_cluster bsas::find_nearest_cluster(const point & p_point) const {
    bsas::nearest_cluster result;

    for (std::size_t i = 0; i < m_result_ptr->clusters().size(); i++) {
        double distance = m_metric(p_point, m_result_ptr->representatives()[i]);
        if (distance < result.m_distance) {
            result.m_distance = distance;
            result.m_index = i;
        }
    }

    return result;
}


void bsas::update_representative(const std::size_t p_index, const point & p_point) {
    auto len = static_cast<double>(m_result_ptr->clusters().size());
    auto & rep = m_result_ptr->representatives()[p_index];

    for (std::size_t dim = 0; dim < rep.size(); dim++) {
        rep[dim] = ( (len - 1) * rep[dim] + p_point[dim] ) / len;
    }
}


}

}