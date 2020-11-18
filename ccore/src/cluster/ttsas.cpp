/*!

@authors Andrei Novikov (pyclustering@yandex.ru)
@date 2014-2020
@copyright BSD-3-Clause

*/


#include <pyclustering/cluster/ttsas.hpp>


namespace pyclustering {

namespace clst {


ttsas::ttsas(const double p_threshold1,
             const double p_threshold2,
             const distance_metric<point> & p_metric) :
    bsas(0, p_threshold1, p_metric),
    m_data_ptr(nullptr),
    m_threshold2(p_threshold2),
    m_skipped_objects(),
    m_start(0)
{ }


void ttsas::process(const dataset & p_data, ttsas_data & p_result) {
    m_result_ptr = (ttsas_data *) &p_result;
    m_data_ptr = (dataset *) &p_data;

    m_amount = p_data.size();
    m_skipped_objects = std::vector<bool>(p_data.size(), true);
    m_start = 0;

    std::size_t changes = 0;
    while (m_amount != 0) {
        const std::size_t previous_amount = m_amount;
        process_objects(changes);

        changes = previous_amount - m_amount;
    }
}


void ttsas::process_objects(const std::size_t p_changes) {
    for (; m_start < m_skipped_objects.size(); m_start++) {
        if (m_skipped_objects[m_start]) {
            break;
        }
    }

    if (p_changes == 0.0) {
        allocate_cluster(m_start, m_data_ptr->at(m_start));
        m_start++;
    }

    for (std::size_t i = m_start; i < m_skipped_objects.size(); i++) {
        if (m_skipped_objects[i]) {
            process_skipped_object(i);
        }
    }
}


void ttsas::process_skipped_object(const std::size_t p_index_point) {
    const point & cur_point = m_data_ptr->at(p_index_point);
    const nearest_cluster nearest = find_nearest_cluster(cur_point);

    if (nearest.m_distance <= m_threshold) {
        append_to_cluster(nearest.m_index, p_index_point, cur_point);
    }
    else if (nearest.m_distance > m_threshold2) {
        allocate_cluster(p_index_point, cur_point);
    }
}


void ttsas::append_to_cluster(const std::size_t p_index_cluster, const std::size_t p_index_point, const point & p_point) {
    m_result_ptr->clusters()[p_index_cluster].push_back(p_index_point);
    update_representative(p_index_cluster, p_point);

    m_amount--;
    m_skipped_objects[p_index_point] = false;
}


void ttsas::allocate_cluster(const std::size_t p_index_point, const point & p_point) {
    m_result_ptr->clusters().push_back({ p_index_point });
    m_result_ptr->representatives().push_back(p_point);

    m_amount--;
    m_skipped_objects[p_index_point] = false;
}


}

}