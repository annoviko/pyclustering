/**
*
* Copyright (C) 2014-2017    Andrei Novikov (pyclustering@yandex.ru)
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

#include "cluster/cluster_algorithm.hpp"
#include "cluster/xmeans_data.hpp"

#include "parallel/thread_pool.hpp"



using namespace parallel;


namespace cluster_analysis {


enum class splitting_type {
    BAYESIAN_INFORMATION_CRITERION = 0,
    MINIMUM_NOISELESS_DESCRIPTION_LENGTH = 1,
};


class xmeans : public cluster_algorithm {
public:
    const static std::size_t        DEFAULT_DATA_SIZE_PARALLEL_PROCESSING;

    const static std::size_t        DEFAULT_THREAD_POOL_SIZE;

private:
    const static double             DEFAULT_SPLIT_DIFFERENCE;

private:
    dataset         m_centers;

    xmeans_data     * m_ptr_result;   /* temporary pointer to output result */

    const dataset   * m_ptr_data;     /* used only during processing */

    std::size_t     m_maximum_clusters;

    double          m_tolerance;

    splitting_type  m_criterion;

    std::size_t     m_parallel_trigger      = DEFAULT_DATA_SIZE_PARALLEL_PROCESSING;

    bool            m_parallel_processing   = false;

    std::mutex      m_mutex;

    thread_pool     m_pool                  { DEFAULT_THREAD_POOL_SIZE };

public:
    /**
    *
    * @brief    Constructor of clustering algorithm where algorithm parameters for processing are
    *           specified.
    *
    * @param[in] p_centers: initial centers that are used for processing.
    * @param[in] p_kmax: maximum number of clusters that can be allocated.
    * @param[in] p_tolerance: stop condition in following way: when maximum value of distance change of
    *             cluster centers is less than tolerance than algorithm will stop processing.
    * @param[in] p_criterion: splitting criterion that is used for making descision about cluster splitting.
    *
    */
    xmeans(const dataset & p_centers, const std::size_t p_kmax, const double p_tolerance, const splitting_type p_criterion);

    /**
    *
    * @brief    Default destructor of the algorithm.
    *
    */
    virtual ~xmeans(void);

public:
    /**
    *
    * @brief    Performs cluster analysis of an input data.
    *
    * @param[in]  p_data: input data for cluster analysis.
    * @param[out] p_result: clustering result of an input data.
    *
    */
    virtual void process(const dataset & data, cluster_data & output_result) override;

    /**
    *
    * @brief    Set custom trigger (that is defined by data size) for parallel processing,
    *            by default this value is defined by static constant DEFAULT_DATA_SIZE_PARALLEL_PROCESSING.
    *
    * @param[in]  p_data_size: data size that triggers parallel processing.
    *
    */
    void set_parallel_processing_trigger(const std::size_t p_data_size);

private:
    void update_clusters(cluster_sequence & clusters, const dataset & centers, const index_sequence & available_indexes);

    double update_centers(const cluster_sequence & clusters, dataset & centers);

    double update_center(const cluster & p_cluster, point & p_center);

    void improve_structure(void);

    void improve_region_structure(const cluster & p_cluster, const point & p_center, dataset & p_allocated_centers);

    void improve_parameters(cluster_sequence & clusters, dataset & centers, const index_sequence & available_indexes);

    double splitting_criterion(const cluster_sequence & clusters, const dataset & centers) const;

    std::size_t find_proper_cluster(const dataset & analysed_centers, const point & p_point) const;

    double bayesian_information_criterion(const cluster_sequence & clusters, const dataset & centers) const;

    double minimum_noiseless_description_length(const cluster_sequence & clusters, const dataset & centers) const;
};


}

