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


#include <mutex>
#include <vector>

#include <pyclustering/cluster/cluster_algorithm.hpp>
#include <pyclustering/cluster/gmeans_data.hpp>

#include <pyclustering/utils/metric.hpp>


using namespace pyclustering::utils::metric;


namespace pyclustering {

namespace clst {


/**
*
* @brief    Represents G-Means clustering algorithm for cluster analysis.
* @details  The G-means algorithm starts with a small number of centers, and grows the number of centers.
*            Each iteration of the G-Means algorithm splits into two those centers whose data appear not to come from a
*            Gaussian distribution. G-means repeatedly makes decisions based on a statistical test for the data
*            assigned to each center.
*
*/
class gmeans : public cluster_algorithm {
private:
    using projection = std::vector<double>;

public:
    const static double             DEFAULT_TOLERANCE;

    const static std::size_t        DEFAULT_REPEAT;

    const static std::size_t        DEFAULT_CANDIDATES;

private:
    std::size_t             m_amount                = 0;

    double                  m_tolerance             = DEFAULT_TOLERANCE;

    std::size_t             m_repeat                = DEFAULT_REPEAT;

    gmeans_data             * m_ptr_result          = nullptr;      /* temporary pointer to output result */

    const dataset           * m_ptr_data            = nullptr;      /* used only during processing */

public:
    /**
    *
    * @brief    Default constructor of clustering algorithm.
    *
    */
    gmeans() = default;

    /**
    *
    * @brief    Constructor of clustering algorithm where algorithm parameters for processing are
    *           specified.
    *
    * @param[in] p_k_initial: initial amount of centers.
    * @param[in] p_tolerance: stop condition in following way: when maximum value of distance change of
    *             cluster centers is less than tolerance than algorithm will stop processing.
    * @param[in] p_repeat: how many times K-Means should be run to improve parameters (by default is 3),
                  with larger 'repeat' values suggesting higher probability of finding global optimum.
    * @param[in] p_itermax: maximum number of iterations (by default gmeans::DEFAULT_ITERMAX).
    *
    */
    gmeans(const std::size_t p_k_initial, 
           const double p_tolerance = DEFAULT_TOLERANCE,
           const std::size_t p_repeat = DEFAULT_REPEAT);

    /**
    *
    * @brief    Default destructor of the algorithm.
    *
    */
    virtual ~gmeans() = default;

public:
    /**
    *
    * @brief    Performs cluster analysis of an input data.
    *
    * @param[in]     p_data: input data for cluster analysis.
    * @param[in|out] p_result: clustering result of an input data, it is also considered as an input argument to
    *                 where observer parameter can be set to collect changes of clusters and centers on each step of
    *                 processing.
    *
    */
    virtual void process(const dataset & p_data, cluster_data & p_result) override;

private:
    void search_optimal_parameters(const dataset & p_data, const std::size_t p_amount, cluster_sequence & p_clusters, dataset & p_centers) const;

    void statistical_optimization();

    void perform_clustering();

    void split_and_search_optimal(const cluster & p_cluster, dataset & p_centers) const;

    static bool is_null_hypothesis(const dataset & p_data, const point & p_center1, const point & p_center2);

    static std::size_t get_amount_candidates(const dataset & p_data);

    static projection calculate_projection(const dataset & p_data, const point & p_vector);
};


}

}
