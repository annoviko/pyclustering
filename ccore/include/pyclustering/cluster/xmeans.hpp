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

#pragma once


#include <mutex>
#include <vector>

#include <pyclustering/cluster/xmeans_data.hpp>


namespace pyclustering {

namespace clst {


/*!

@brief  Defines splitting types for clusters that are used by X-Means algorithm.

*/
enum class splitting_type {
    BAYESIAN_INFORMATION_CRITERION = 0,         /**< Bayesian information criterion (BIC) to approximate the correct number of clusters. */
    MINIMUM_NOISELESS_DESCRIPTION_LENGTH = 1,   /**< Minimum noiseless description length (MNDL) to approximate the correct number of clusters. */
};


/*!

@class      xmeans xmeans.hpp pyclustering/cluster/xmeans.hpp

@brief      Class represents clustering algorithm X-Means.
@details    X-means clustering method starts with the assumption of having a minimum number of clusters,
             and then dynamically increases them. X-means uses specified splitting criterion to control
             the process of splitting clusters. Method K-Means++ can be used for calculation of initial centers.

*/
class xmeans {
private:
    const static double             DEFAULT_SPLIT_DIFFERENCE;

    const static std::size_t        AMOUNT_CENTER_CANDIDATES;

private:
    dataset           m_initial_centers;

    xmeans_data       * m_ptr_result        = nullptr;   /* temporary pointer to output result */

    const dataset     * m_ptr_data          = nullptr;     /* used only during processing */

    std::size_t       m_maximum_clusters;

    double            m_tolerance;

    splitting_type    m_criterion           = splitting_type::BAYESIAN_INFORMATION_CRITERION;

    std::size_t       m_repeat              = 1;

    long long         m_random_state        = RANDOM_STATE_CURRENT_TIME;

public:
    /*!
    
    @brief    Constructor of X-Means clustering algorithm.
    
    @param[in] p_initial_centers: initial centers that are used for processing.
    @param[in] p_kmax: maximum number of clusters that can be allocated.
    @param[in] p_tolerance: stop condition in following way: when maximum value of distance change of
                cluster centers is less than tolerance than algorithm will stop processing.
    @param[in] p_criterion: splitting criterion that is used for making descision about cluster splitting.
    @param[in] p_repeat: how many times K-Means should be run to improve parameters (by default is 1), 
                with larger 'repeat' values suggesting higher probability of finding global optimum.
    @param[in] p_random_state: seed for random state (by default is `RANDOM_STATE_CURRENT_TIME`, current system time is used).
    
    */
    xmeans(const dataset & p_initial_centers, 
           const std::size_t p_kmax, 
           const double p_tolerance, 
           const splitting_type p_criterion, 
           const std::size_t p_repeat = 1, 
           const long long p_random_state = RANDOM_STATE_CURRENT_TIME);

    /*!
    
    @brief    Default destructor of the algorithm.
    
    */
    ~xmeans() = default;

public:
    /*!
    
    @brief    Performs cluster analysis of an input data.
    
    @param[in]  p_data: input data for cluster analysis.
    @param[out] p_result: clustering result of an input data.
    
    */
    void process(const dataset & p_data, xmeans_data & p_result);

private:
    void improve_structure();

    void improve_region_structure(const cluster & p_cluster, const point & p_center, dataset & p_allocated_centers) const;

    double search_optimal_parameters(cluster_sequence & improved_clusters, dataset & improved_centers, const index_sequence & available_indexes) const;

    double improve_parameters(cluster_sequence & improved_clusters, dataset & improved_centers, const index_sequence & available_indexes) const;

    double splitting_criterion(const cluster_sequence & analysed_clusters, const dataset & analysed_centers) const;

    double bayesian_information_criterion(const cluster_sequence & analysed_clusters, const dataset & analysed_centers) const;

    double minimum_noiseless_description_length(const cluster_sequence & clusters, const dataset & centers) const;
};


}

}
