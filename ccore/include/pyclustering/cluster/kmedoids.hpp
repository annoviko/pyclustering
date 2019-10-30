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


#include <memory>

#include <pyclustering/cluster/cluster_algorithm.hpp>
#include <pyclustering/cluster/kmedoids_data.hpp>

#include <pyclustering/utils/metric.hpp>


using namespace pyclustering::utils::metric;


namespace pyclustering {

namespace clst {


enum class kmedoids_data_t {
    POINTS,
    DISTANCE_MATRIX
};


/**
*
* @brief    Represents K-Medoids clustering algorithm for cluster analysis.
* @details  The algorithm related to partitional class when input data is divided into groups.
*
*/
class kmedoids : public cluster_algorithm {
public:
    static const double      DEFAULT_TOLERANCE;

    static const std::size_t DEFAULT_ITERMAX;

private:
    static const std::size_t OBJECT_ALREADY_CONTAINED;

private:
    using distance_calculator = std::function<double(const std::size_t, const std::size_t)>;

private:
    const dataset                   * m_data_ptr      = nullptr;   /* temporary pointer to input data that is used only during processing */

    kmedoids_data                   * m_result_ptr    = nullptr; /* temporary pointer to clustering result that is used only during processing */

    medoid_sequence                 m_initial_medoids = { };

    double                          m_tolerance       = DEFAULT_TOLERANCE;

    std::size_t                     m_itermax         = DEFAULT_ITERMAX;

    distance_metric<point>          m_metric;

    distance_calculator             m_calculator;

public:
    /**
    *
    * @brief    Default constructor of clustering algorithm.
    *
    */
    kmedoids() = default;

    /**
    *
    * @brief    Constructor of clustering algorithm where algorithm parameters for processing are
    *           specified.
    *
    * @param[in] p_initial_medoids: initial medoids that are used for processing.
    * @param[in] p_tolerance: stop condition in following way: when maximum value of distance change of
    *             medoids of clusters is less than tolerance than algorithm will stop processing.
    * @param[in] p_itermax: maximum amount of iterations (by default kmedoids::DEFAULT_ITERMAX).
    * @param[in] p_metric: distance metric calculator for two points.
    *
    */
    kmedoids(const medoid_sequence & p_initial_medoids,
             const double p_tolerance = DEFAULT_TOLERANCE,
             const std::size_t p_itermax = DEFAULT_ITERMAX,
             const distance_metric<point> & p_metric = distance_metric_factory<point>::euclidean_square());

    /**
    *
    * @brief    Default destructor of the algorithm.
    *
    */
    virtual ~kmedoids();

public:
    /**
    *
    * @brief    Performs cluster analysis of an input data.
    *
    * @param[in]  p_data: input data for cluster analysis.
    * @param[out] p_result: clustering result of an input data.
    *
    */
    virtual void process(const dataset & p_data, cluster_data & p_result) override;

    /**
    *
    * @brief    Performs cluster analysis of an input data.
    *
    * @param[in]  p_data: input data for cluster analysis.
    * @param[in]  p_type: data type (points or distance matrix).
    * @param[out] p_result: clustering result of an input data.
    *
    */
    virtual void process(const dataset & p_data, const kmedoids_data_t p_type, cluster_data & p_result);

private:
    /**
    *
    * @brief    Updates clusters in line with current medoids.
    *
    */
    void update_clusters();

    /**
    *
    * @brief    Calculates medoids in line with current clusters.
    *
    * @param[out] p_medoids: calculated medoids for current clusters.
    *
    */
    void calculate_medoids(cluster & p_medoids);

    /**
    *
    * @brief    Calculates medoid for specified cluster.
    *
    * @param[in] p_cluster: cluster that is used for medoid calculation.
    *
    * @return   Medoid (index point) of specified cluster.
    *
    */
    size_t calculate_cluster_medoid(const cluster & p_cluster) const;

    /**
    *
    * @brief    Calculates maximum difference in data allocation between previous medoids and specified.
    *
    * @param[in] p_medoids: medoids that should be used for difference calculation.
    *
    * @return   Maximum difference between current medoids and specified.
    *
    */
    double calculate_changes(const medoid_sequence & p_medoids) const;

    /**
    *
    * @brief    Creates distance calcultor in line with data type and distance metric metric.
    *
    * @param[in] p_type: data type (points or distance matrix).
    *
    * @return   Distance calculator.
    *
    */
    distance_calculator create_distance_calculator(const kmedoids_data_t p_type);

    /**
    *
    * @brief    Find appropriate cluster for the particular point.
    *
    * @param[in] p_index: Index of point that should be placed to cluster.
    * @param[in] p_medoids: Medoids that corresponds to clusters.
    *
    * @return   Index of cluster that is appropriate for the particular point. If point is a medoid
    *           then OBJECT_ALREADY_CONTAINED value is returned.
    *
    */
    std::size_t find_appropriate_cluster(const std::size_t p_index, medoid_sequence & p_medoids);
};


}

}
