/*!

@authors Andrei Novikov (pyclustering@yandex.ru)
@date 2014-2020
@copyright BSD-3-Clause

*/

#include <limits>

#include <pyclustering/cluster/silhouette.hpp>


namespace pyclustering {

namespace clst {


silhouette::silhouette(const distance_metric<point> & p_metric) :
    m_metric(p_metric)
{ }


void silhouette::process(const dataset & p_data, const cluster_sequence & p_clusters, silhouette_data & p_result) {
    process(p_data, p_clusters, data_t::POINTS, p_result);
}


void silhouette::process(const dataset & p_data, const cluster_sequence & p_clusters, const data_t & p_type, silhouette_data & p_result) {
    m_data      = &p_data;
    m_clusters  = &p_clusters;
    m_result    = &p_result;
    m_type      = p_type;

    m_result->get_score().reserve(m_data->size());

    for (std::size_t index_cluster = 0; index_cluster < m_clusters->size(); index_cluster++) {
        const auto & current_cluster = m_clusters->at(index_cluster);
        for (const auto index_point : current_cluster) {
            m_result->get_score().push_back(calculate_score(index_point, index_cluster));
        }
    }
}


double silhouette::calculate_score(const std::size_t p_index_point, const std::size_t p_index_cluster) const {
    std::vector<double> dataset_difference;
    calculate_dataset_difference(p_index_point, dataset_difference);

    const double a_score = calculate_within_cluster_score(p_index_cluster, dataset_difference);
    const double b_score = caclulate_optimal_neighbor_cluster_score(p_index_cluster, dataset_difference);

    return (b_score - a_score) / std::max(a_score, b_score);
}


void silhouette::calculate_dataset_difference(const std::size_t p_index_point, std::vector<double> & p_dataset_difference) const {
    if (m_type == data_t::DISTANCE_MATRIX) {
        p_dataset_difference = m_data->at(p_index_point);
        return;
    }

    p_dataset_difference.reserve(m_data->size());

    const auto & current_point = m_data->at(p_index_point);
    for (const auto & point : *m_data) {
        p_dataset_difference.emplace_back(m_metric(current_point, point));
    }
}


double silhouette::calculate_cluster_difference(const std::size_t p_index_cluster, const std::vector<double> & p_dataset_difference) const {
    double cluster_difference = 0.0;

    const auto & current_cluster = m_clusters->at(p_index_cluster);
    for (const auto index_point : current_cluster) {
        cluster_difference += p_dataset_difference[index_point];
    }

    return cluster_difference;
}


double silhouette::calculate_within_cluster_score(const std::size_t p_index_cluster, const std::vector<double> & p_dataset_difference) const {
    double score = calculate_cluster_difference(p_index_cluster, p_dataset_difference);
    const std::size_t cluster_size = m_clusters->at(p_index_cluster).size();
    if (cluster_size == 1) {
        return std::nan("1");
    }

    return score / static_cast<double>(cluster_size - 1);
}


double silhouette::calculate_cluster_score(const std::size_t p_index_cluster, const std::vector<double> & p_dataset_difference) const {
    const double score = calculate_cluster_difference(p_index_cluster, p_dataset_difference);
    return score / m_clusters->at(p_index_cluster).size();
}


double silhouette::caclulate_optimal_neighbor_cluster_score(const std::size_t p_index_cluster, const std::vector<double> & p_dataset_difference) const {
    double optimal_score = std::numeric_limits<double>::infinity();
    for (std::size_t index_neighbor_cluster = 0; index_neighbor_cluster < m_clusters->size(); index_neighbor_cluster++) {
        if (p_index_cluster != index_neighbor_cluster) {
            const double candidate_score = calculate_cluster_score(index_neighbor_cluster, p_dataset_difference);
            if (candidate_score < optimal_score) {
                optimal_score = candidate_score;
            }
        }
    }

    return optimal_score;
}


}

}
