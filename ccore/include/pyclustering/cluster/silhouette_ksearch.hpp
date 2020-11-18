/*!

@authors Andrei Novikov (pyclustering@yandex.ru)
@date 2014-2020
@copyright BSD-3-Clause

*/

#pragma once


#include <pyclustering/cluster/silhouette.hpp>
#include <pyclustering/cluster/silhouette_ksearch_data.hpp>


namespace pyclustering {

namespace clst {


/*!

@class    silhouette_ksearch_allocator silhouette_ksearch.hpp pyclustering/cluster/silhouette_ksearch.hpp

@brief    Interface of silhouette's K-search allocator that is used by the algorithm to define strategy that defines how to
           perform cluster analysis.


@see    kmeans_allocator
@see    kmedians_allocator
@see    kmedoids_allocator

*/
class silhouette_ksearch_allocator {
public:
    /*!

    @brief Defines shared pointer to the interface 'silhouette_ksearch_allocator'.

    */
    using ptr = std::shared_ptr<silhouette_ksearch_allocator>;

public:
    /*!
    
    @brief Default destructor of the algorithm.
    
    */
    virtual ~silhouette_ksearch_allocator() = default;

public:
    /*!

    @brief Performs cluster analysis in order to allocate specified amount of cluster from an input data.

    @param[in]  p_amount: amount of clusters that should be allocated.
    @param[in]  p_data: input data for cluster analysis.
    @param[out] p_clusters: container where result (allocated clusters) is placed.

    */
    virtual void allocate(const std::size_t p_amount, const dataset & p_data, cluster_sequence & p_clusters) = 0;

    /*!

    @brief Performs cluster analysis in order to allocate specified amount of cluster from an input data.

    @param[in]  p_amount: amount of clusters that should be allocated.
    @param[in]  p_data: input data for cluster analysis.
    @param[in]  p_random_state: seed for random state (value `RANDOM_STATE_CURRENT_TIME` means the current system time is going to used as a seed).
    @param[out] p_clusters: container where result (allocated clusters) is placed.

    */
    virtual void allocate(const std::size_t p_amount, const dataset & p_data, const long long p_random_state, cluster_sequence & p_clusters) = 0;
};


/*!

@class    kmeans_allocator silhouette_ksearch.hpp pyclustering/cluster/silhouette_ksearch.hpp

@brief    Silhouette K-search allocator based on K-Means algorithm.

*/
class kmeans_allocator : public silhouette_ksearch_allocator {
public:
    /*!

    @brief Performs cluster analysis using K-Means algorithm.

    @param[in]  p_amount: amount of clusters that should be allocated.
    @param[in]  p_data: input data for cluster analysis.
    @param[out] p_clusters: container where result (allocated clusters) is placed.

    */
    virtual void allocate(const std::size_t p_amount, const dataset & p_data, cluster_sequence & p_clusters) override;

    /*!

    @brief Performs cluster analysis using K-Means algorithm.

    @param[in]  p_amount: amount of clusters that should be allocated.
    @param[in]  p_data: input data for cluster analysis.
    @param[in]  p_random_state: seed for random state (value `RANDOM_STATE_CURRENT_TIME` means the current system time is going to used as a seed).
    @param[out] p_clusters: container where result (allocated clusters) is placed.

    */
    virtual void allocate(const std::size_t p_amount, const dataset & p_data, const long long p_random_state, cluster_sequence & p_clusters) override;
};


/*!

@class    kmedians_allocator silhouette_ksearch.hpp pyclustering/cluster/silhouette_ksearch.hpp

@brief    Silhouette K-search allocator based on K-Medians algorithm.

*/
class kmedians_allocator : public silhouette_ksearch_allocator {
public:
    /*!

    @brief Performs cluster analysis using K-Medians algorithm.

    @param[in]  p_amount: amount of clusters that should be allocated.
    @param[in]  p_data: input data for cluster analysis.
    @param[out] p_clusters: container where result (allocated clusters) is placed.

    */
    virtual void allocate(const std::size_t p_amount, const dataset & p_data, cluster_sequence & p_clusters) override;

    /*!

    @brief Performs cluster analysis using K-Medians algorithm.

    @param[in]  p_amount: amount of clusters that should be allocated.
    @param[in]  p_data: input data for cluster analysis.
    @param[in]  p_random_state: seed for random state (value `RANDOM_STATE_CURRENT_TIME` means the current system time is going to used as a seed).
    @param[out] p_clusters: container where result (allocated clusters) is placed.

    */
    virtual void allocate(const std::size_t p_amount, const dataset & p_data, const long long p_random_state, cluster_sequence & p_clusters) override;
};


/*!

@class    kmedoids_allocator silhouette_ksearch.hpp pyclustering/cluster/silhouette_ksearch.hpp

@brief    Silhouette K-search allocator based on K-Medoids algorithm.

*/
class kmedoids_allocator : public silhouette_ksearch_allocator {
public:
    /*!

    @brief Performs cluster analysis using K-Medoids algorithm.

    @param[in]  p_amount: amount of clusters that should be allocated.
    @param[in]  p_data: input data for cluster analysis.
    @param[out] p_clusters: container where result (allocated clusters) is placed.

    */
    virtual void allocate(const std::size_t p_amount, const dataset & p_data, cluster_sequence & p_clusters) override;

    /*!

    @brief Performs cluster analysis using K-Medoids algorithm.

    @param[in]  p_amount: amount of clusters that should be allocated.
    @param[in]  p_data: input data for cluster analysis.
    @param[in]  p_random_state: seed for random state (value `RANDOM_STATE_CURRENT_TIME` means the current system time is going to used as a seed).
    @param[out] p_clusters: container where result (allocated clusters) is placed.

    */
    virtual void allocate(const std::size_t p_amount, const dataset & p_data, const long long p_random_state, cluster_sequence & p_clusters) override;
};



/*!

@class    silhouette_ksearch silhouette_ksearch.hpp pyclustering/cluster/silhouette_ksearch.hpp

@brief    Defines algorithms that is used to find optimal number of cluster using Silhouette method.

*/
class silhouette_ksearch {
private:
    std::size_t m_kmin;
    std::size_t m_kmax;
    silhouette_ksearch_allocator::ptr m_allocator = std::make_shared<kmeans_allocator>();
    long long m_random_state;

public:
    /*!

    @brief    Default constructor of Silhouette search algorithm.

    */
    silhouette_ksearch() = default;

    /*!

    @brief    Constructor of Silhouette search algorithm.

    @param[in] p_kmin: minimum amount of clusters that might be allocated.
    @param[in] p_kmax: maximum amount of clusters that might be allocated.
    @param[in] p_allocator: strategy that is used to allocate clusters or in other words, to perform cluster analysis.
    @param[in] p_random_state: seed for random state (by default is `RANDOM_STATE_CURRENT_TIME`, current system time is used).

    */
    silhouette_ksearch(const std::size_t p_kmin, const std::size_t p_kmax, const silhouette_ksearch_allocator::ptr & p_allocator = std::make_shared<kmeans_allocator>(), const long long p_random_state = RANDOM_STATE_CURRENT_TIME);

    /*!

    @brief    Default copy constructor of Silhouette search algorithm.

    */
    silhouette_ksearch(const silhouette_ksearch & p_other) = default;

    /*!

    @brief    Default move constructor of Silhouette search algorithm.

    */
    silhouette_ksearch(silhouette_ksearch && p_other) = default;

    /*!

    @brief    Default destructor of Silhouette search algorithm.

    */
    ~silhouette_ksearch() = default;

public:
    /*!

    @brief    Performs analysis to find optimal amount of clusters.

    @param[in] p_data: input data that is used for searching optimal amount of clusters.
    @param[in] p_result: analysis result of an input data.

    */
    void process(const dataset & p_data, silhouette_ksearch_data & p_result);
};

}

}