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

#include <pyclustering/cluster/kmeans.hpp>

#include <pyclustering/parallel/parallel.hpp>

#include <algorithm>
#include <limits>
#include <unordered_map>

#include <pyclustering/utils/metric.hpp>


using namespace pyclustering::parallel;
using namespace pyclustering::utils::metric;


namespace pyclustering {

namespace clst {


const double             kmeans::DEFAULT_TOLERANCE                       = 0.001;

const std::size_t        kmeans::DEFAULT_ITERMAX                         = 100;


kmeans::kmeans(const dataset & p_initial_centers, const double p_tolerance, const std::size_t p_itermax, const distance_metric<point> & p_metric) :
    m_tolerance(p_tolerance),
    m_itermax(p_itermax),
    m_initial_centers(p_initial_centers),
    m_ptr_result(nullptr),
    m_ptr_data(nullptr),
    m_metric(p_metric)
{ }


void kmeans::process(const dataset & p_data, cluster_data & p_result) {
    process(p_data, { }, p_result);
}


void kmeans::process(const dataset & p_data, const index_sequence & p_indexes, cluster_data & p_result) {
    m_ptr_data = &p_data;
    m_ptr_indexes = &p_indexes;

    m_ptr_result = (kmeans_data *) &p_result;

    if (p_data[0].size() != m_initial_centers[0].size()) {
        throw std::invalid_argument("Dimension of the input data and dimension of the initial cluster centers must be the same.");
    }

    m_ptr_result->centers().assign(m_initial_centers.begin(), m_initial_centers.end());

    if (m_ptr_result->is_observed()) {
        cluster_sequence sequence;
        update_clusters(m_initial_centers, sequence);

        m_ptr_result->evolution_centers().push_back(m_initial_centers);
        m_ptr_result->evolution_clusters().push_back(sequence);
    }

    double current_change = std::numeric_limits<double>::max();

    for(std::size_t iteration = 0; iteration < m_itermax && current_change > m_tolerance; iteration++) {
        update_clusters(m_ptr_result->centers(), m_ptr_result->clusters());
        current_change = update_centers(m_ptr_result->clusters(), m_ptr_result->centers());

        if (m_ptr_result->is_observed()) {
            m_ptr_result->evolution_centers().push_back(m_ptr_result->centers());
            m_ptr_result->evolution_clusters().push_back(m_ptr_result->clusters());
        }
    }

    calculate_total_wce();
}


void kmeans::update_clusters(const dataset & p_centers, cluster_sequence & p_clusters) {
    const dataset & data = *m_ptr_data;

    p_clusters.clear();
    p_clusters.resize(p_centers.size());

    /* fill clusters again in line with centers. */
    if (m_ptr_indexes->empty()) {
        index_sequence winners(data.size(), 0);
        parallel_for(std::size_t(0), data.size(), [this, &p_centers, &winners](std::size_t p_index) {
            assign_point_to_cluster(p_index, p_centers, winners);
        });

        for (std::size_t index_point = 0; index_point < winners.size(); index_point++) {
            const std::size_t suitable_index_cluster = winners[index_point];
            p_clusters[suitable_index_cluster].push_back(index_point);
        }
    }
    else {
        /* This part of code is used by X-Means and in case of parallel implementation of this part in scope of X-Means
           performance is slightly reduced. Experiments has been performed our implementation and Intel TBB library. 
           But in K-Means case only - it works perfectly and increase performance. */
        std::vector<std::size_t> winners(data.size(), 0);
        parallel_for_each(*m_ptr_indexes, [this, &p_centers, &winners](std::size_t p_index) {
            assign_point_to_cluster(p_index, p_centers, winners);
        });

        for (std::size_t index_point : *m_ptr_indexes) {
            const std::size_t suitable_index_cluster = winners[index_point];
            p_clusters[suitable_index_cluster].push_back(index_point);
        }
    }

    erase_empty_clusters(p_clusters);
}


void kmeans::assign_point_to_cluster(const std::size_t p_index_point, const dataset & p_centers, index_sequence & p_clusters) {
    double    minimum_distance = std::numeric_limits<double>::max();
    size_t    suitable_index_cluster = 0;

    for (size_t index_cluster = 0; index_cluster < p_centers.size(); index_cluster++) {
        double distance = m_metric(p_centers[index_cluster], (*m_ptr_data)[p_index_point]);

        if (distance < minimum_distance) {
            minimum_distance = distance;
            suitable_index_cluster = index_cluster;
        }
    }

    p_clusters[p_index_point] = suitable_index_cluster;
}


void kmeans::erase_empty_clusters(cluster_sequence & p_clusters) {
    for (size_t index_cluster = p_clusters.size() - 1; index_cluster != (size_t) -1; index_cluster--) {
        if (p_clusters[index_cluster].empty()) {
            p_clusters.erase(p_clusters.begin() + index_cluster);
        }
    }
}


double kmeans::update_centers(const cluster_sequence & clusters, dataset & centers) {
    const dataset & data = *m_ptr_data;
    const size_t dimension = data[0].size();

    dataset calculated_clusters(clusters.size(), point(dimension, 0.0));
    std::vector<double> changes(clusters.size(), 0.0);

    parallel_for(std::size_t(0), clusters.size(), [this, &clusters, &centers, &calculated_clusters, &changes](const std::size_t p_index) {
        calculated_clusters[p_index] = centers[p_index];
        changes[p_index] = update_center(clusters[p_index], calculated_clusters[p_index]);
    });

    centers = std::move(calculated_clusters);

    return *(std::max_element(changes.begin(), changes.end()));
}


double kmeans::update_center(const cluster & p_cluster, point & p_center) {
    point total(p_center.size(), 0.0);

    /* for each object in cluster */
    for (auto object_index : p_cluster) {
        /* for each dimension */
        for (size_t dimension = 0; dimension < total.size(); dimension++) {
            total[dimension] += (*m_ptr_data)[object_index][dimension];
        }
    }

    /* average for each dimension */
    for (auto & dimension : total) {
        dimension /= p_cluster.size();
    }

    const double change = m_metric(p_center, total);

    p_center = std::move(total);
    return change;
}


void kmeans::calculate_total_wce() {
    double & wce = m_ptr_result->wce();
    for (std::size_t i = 0; i < m_ptr_result->clusters().size(); i++) {
        const auto & current_cluster = m_ptr_result->clusters().at(i);
        const auto & cluster_center = m_ptr_result->centers().at(i);

        for (const auto & cluster_point : current_cluster) {
            wce += m_metric(m_ptr_data->at(cluster_point), cluster_center);
        }
    }
}


}

}
