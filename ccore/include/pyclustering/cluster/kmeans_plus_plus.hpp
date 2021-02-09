/*!

@authors Andrei Novikov (pyclustering@yandex.ru)
@date 2014-2020
@copyright BSD-3-Clause

*/


#pragma once


#include <random>
#include <unordered_set>

#include <pyclustering/definitions.hpp>

#include <pyclustering/cluster/center_initializer.hpp>
#include <pyclustering/cluster/cluster_data.hpp>
#include <pyclustering/utils/metric.hpp>


using namespace pyclustering::utils::metric;


namespace pyclustering {

namespace clst {


/**
 *
 * @brief K-Means++ center initializer algorithm.
 *
 */
class kmeans_plus_plus : public center_initializer {
public:
    /**
     *
     * @brief Denotes that the farthest center candidate (with highest probability) should be used as a center.
     *
     */
    static const std::size_t FARTHEST_CENTER_CANDIDATE;

    /**
     *
     * @brief Non-existed index that represents non-initialized value.
     *
     */
    static const std::size_t INVALID_INDEX;

public:
    /**
     *
     * @brief Metric that is used for distance calculation between two points.
     *
     */
    using metric = distance_functor<std::vector<double>>;

private:
    using index_set = std::unordered_set<std::size_t>;

    using center_description = std::tuple<point, std::size_t>;
    enum { POINT, INDEX };

    using store_result = std::function<void(center_description &)>;

private:
    std::size_t             m_amount        = 0;
    std::size_t             m_candidates    = 0;
    metric                  m_dist_func;
    long long               m_random_state  = RANDOM_STATE_CURRENT_TIME;
    mutable std::mt19937    m_generator;

    /* temporal members that are used only during initialization */
    mutable dataset const *           m_data_ptr      = nullptr;
    mutable index_sequence const *    m_indexes_ptr   = nullptr;

    mutable index_set       m_free_indexes;
    mutable index_sequence  m_allocated_indexes;

public:
    /**
     *
     * @brief Default constructor to create initializer algorithm K-Means++.
     *
     */
    kmeans_plus_plus() = default;

    /**
    *
    * @brief    Constructor of center initializer algorithm K-Means++.
    *
    * @param[in] p_amount: amount of centers that should initialized.
    * @param[in] p_candidates: amount of candidates that are considered to find the best center, if
    *             the farthest candidate is required (with highest probability) than static constant
    *             FARTHEST_CENTER_CANDIDATE can be specified.
    * @param[in] p_random_state: seed for random state (by default is `RANDOM_STATE_CURRENT_TIME`, current system time is used).
    *
    * @see FARTHEST_CENTER_CANDIDATE
    *
    */
    kmeans_plus_plus(const std::size_t p_amount, const std::size_t p_candidates = 1, const long long p_random_state = RANDOM_STATE_CURRENT_TIME) noexcept;

    /**
    *
    * @brief    Constructor of center initializer algorithm K-Means++.
    * @details  By default algorithm uses square Euclidean distance as a metric.
    *
    * @param[in] p_amount: amount of centers that should initialized.
    * @param[in] p_candidates: amount of candidates that are considered to find the best center, if
    *             the farthest candidate is required (with highest probability) than static constant
    *             FARTHEST_CENTER_CANDIDATE can be specified.
    * @param[in] p_metric: metric for distance calculation between points.
    * @param[in] p_random_state: seed for random state (by default is `RANDOM_STATE_CURRENT_TIME`, current system time is used).
    *
    * @see FARTHEST_CENTER_CANDIDATE
    *
    */
    kmeans_plus_plus(const std::size_t p_amount, const std::size_t p_candidates, const metric & p_metric, const long long p_random_state = RANDOM_STATE_CURRENT_TIME) noexcept;

    /**
     *
     * @brief Default copy constructor to create initializer algorithm K-Means++.
     *
     */
    kmeans_plus_plus(const kmeans_plus_plus & p_other) = default;

    /**
     *
     * @brief Default move constructor to create initializer algorithm K-Means++.
     *
     */
    kmeans_plus_plus(kmeans_plus_plus && p_other) = default;

    /**
     *
     * @brief Default destructor to destroy initializer algorithm K-Means++.
     *
     */
    ~kmeans_plus_plus() = default;

public:
    /**
    *
    * @brief    Performs center initialization process in line algorithm configuration.
    *
    * @param[in]  p_data: data for that centers are calculated.
    * @param[out] p_centers: initialized centers for the specified data.
    *
    */
    void initialize(const dataset & p_data, dataset & p_centers) const override;

    /**
    *
    * @brief    Performs center initialization process in line algorithm configuration for
    *           specific range of points.
    *
    * @param[in]  p_data: data for that centers are calculated.
    * @param[in]  p_indexes: point indexes from data that are defines which points should be considered
    *              during calculation process. If empty then all data points are considered.
    * @param[out] p_centers: initialized centers for the specified data.
    *
    */
    void initialize(const dataset & p_data, const index_sequence & p_indexes, dataset & p_centers) const override;

    /**
    *
    * @brief    Performs center initialization process in line algorithm configuration using real points from dataset as centers.
    *
    * @param[in]  p_data: data for that centers are calculated.
    * @param[out] p_center_indexes: initialized center indexes for the specified data where indexes correspond to points from the data.
    *
    */
    void initialize(const dataset & p_data, index_sequence & p_center_indexes) const;

private:
    /**
    *
    * @brief    Assigns seed to the random generator that is used by the algorithm.
    *
    */
    void initialize_random_generator();

    /**
    *
    * @brief    Performs center initialization process in line algorithm configuration.
    *
    * @param[in]  p_data: data for that centers are calculated.
    * @param[in]  p_indexes: point indexes from data that are defines which points should be considered
    *              during calculation process. If empty then all data points are considered.
    * @param[out] p_proc: function that defines how to store output result of the algorithm.
    *
    */
    void initialize(const dataset & p_data, const index_sequence & p_indexes, const store_result & p_proc) const;

    /**
    *
    * @brief    Store obtained center.
    *
    * @param[in]  p_proc: function that defines how to store output result of the algorithm.
    * @param[in]  p_result: initialized center that should be stored.
    *
    */
    void store_center(const store_result & p_proc, center_description & p_result) const;

    /**
    *
    * @brief    Store pointers to data, indexes and centers to avoiding passing them between class methods.
    * @details  Pointers are reseted when center initialization is over.
    *
    * @param[in]  p_data: data for that centers are calculated.
    * @param[in]  p_indexes: point indexes from data that are defines which points should be
    *              considered during calculation process.
    *
    * @return   The first initialized center.
    *
    */
    void store_temporal_params(const dataset & p_data, const index_sequence & p_indexes) const;

    /**
    *
    * @brief    Reset (fill by nullptr) temporal points.
    *
    */
    void free_temporal_params() const;

    /**
    *
    * @brief    Calculates the first initial center using uniform distribution.
    *
    * @return   The first initialized center.
    *
    */
    center_description get_first_center() const;

    /**
    *
    * @brief    Calculates the next most probable center in line with weighted distribution.
    *
    * @return   The next initialized center.
    *
    */
    center_description get_next_center() const;

    /**
    *
    * @brief    Calculates distances from each point to closest center.
    *
    * @param[out] p_distances: the shortest distances from each point to center.
    *
    */
    void calculate_shortest_distances(std::vector<double> & p_distances) const;

    /**
    *
    * @brief    Calculates distance from the specified point to the closest center.
    *
    * @param[in]  p_point: point for that the shortest distance is calculated.
    *
    */
    double get_shortest_distance(const point & p_point) const;

    /**
    *
    * @brief    Calculates center probability for each point using distances to closest centers.
    *
    * @param[in]  p_distances: distances from each point to closest center.
    * @param[out] p_probabilities: probability of each point to be next center.
    *
    */
    void calculate_probabilities(const std::vector<double> & p_distances, std::vector<double> & p_probabilities) const;

    /**
    *
    * @brief    Calculates most probable center.
    *
    * @param[in]  p_distances: distances from each point to closest center.
    * @param[in] p_probabilities: probability of each point to be next center.
    *
    */
    std::size_t get_probable_center(const std::vector<double> & p_distances, const std::vector<double> & p_probabilities) const;
};


}

}
