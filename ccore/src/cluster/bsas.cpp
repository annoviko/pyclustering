/*!

@authors Andrei Novikov (pyclustering@yandex.ru)
@date 2014-2020
@copyright BSD-3-Clause

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


void bsas::process(const dataset & p_data, bsas_data & p_result) {
    m_result_ptr = &p_result;

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