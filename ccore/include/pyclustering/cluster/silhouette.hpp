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


#include <pyclustering/cluster/cluster_data.hpp>
#include <pyclustering/cluster/silhouette_data.hpp>

#include <pyclustering/definitions.hpp>

#include <pyclustering/utils/metric.hpp>


using namespace pyclustering::utils::metric;


namespace pyclustering {

namespace clst {


enum class silhouette_data_t {
    POINTS,
    DISTANCE_MATRIX
};


class silhouette {
private:
    const dataset *           m_data      = nullptr;  /* temporary object, exists during processing */
    const cluster_sequence *  m_clusters  = nullptr;  /* temporary object, exists during processing */
    silhouette_data *         m_result    = nullptr;  /* temporary object, exists during processing */

    silhouette_data_t         m_type      = silhouette_data_t::POINTS;

    distance_metric<point>    m_metric    = distance_metric_factory<point>::euclidean_square();

public:
    silhouette() = default;

    explicit silhouette(const distance_metric<point> & p_metric);

    silhouette(const silhouette & p_other) = default;

    silhouette(silhouette && p_other) = default;

    ~silhouette() = default;

public:
    void process(const dataset & p_data, const cluster_sequence & p_clusters, silhouette_data & p_result);

    void process(const dataset & p_data, const cluster_sequence & p_clusters, const silhouette_data_t & p_type, silhouette_data & p_result);

private:
    double calculate_score(const std::size_t p_index_point, const std::size_t p_index_cluster) const;

    void calculate_dataset_difference(const std::size_t p_index_point, std::vector<double> & p_dataset_difference) const;

    double calculate_cluster_difference(const std::size_t p_index_cluster, const std::vector<double> & p_dataset_difference) const;

    double calculate_within_cluster_score(const std::size_t p_index_cluster, const std::vector<double> & p_dataset_difference) const;

    double calculate_cluster_score(const std::size_t p_index_cluster, const std::vector<double> & p_dataset_difference) const;

    double caclulate_optimal_neighbor_cluster_score(const std::size_t p_index_cluster, const std::vector<double> & p_dataset_difference) const;
};


}

}