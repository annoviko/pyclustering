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


/*!

@class   random_center_initializer random_center_initializer.hpp pyclustering/cluster/random_center_initializer.hpp

@brief   Random center initializer is for generation specified amount of random of centers for specified data.

*/
class random_center_initializer : public center_initializer {
private:
    /**
     *
     * @brief Storage where indexes are stored.
     *
     */
    using index_storage = std::unordered_set<std::size_t>;

private:
    std::size_t             m_amount            = 0;

    long long               m_random_state      = RANDOM_STATE_CURRENT_TIME;

    mutable std::mt19937    m_generator;

    mutable index_storage   m_available_indexes = { };

public:
    /**
     *
     * @brief Default constructor to create random center initializer.
     *
     */
    random_center_initializer() = default;

    /**
     *
     * @brief    Constructor of center initializer algorithm K-Means++.
     *
     * @param[in] p_amount: amount of centers that should initialized.
     * @param[in] p_random_state: seed for random state (by default is `RANDOM_STATE_CURRENT_TIME`, current system time is used).
     *
     */
    explicit random_center_initializer(const std::size_t p_amount, const long long p_random_state);

    /**
     *
     * @brief Default copy constructor to create random center initializer.
     *
     */
    random_center_initializer(const random_center_initializer & p_other) = default;

    /**
     *
     * @brief Default move constructor to create random center initializer.
     *
     */
    random_center_initializer(random_center_initializer && p_other) = default;

    /**
     *
     * @brief Default destructor to destroy random center initializer.
     *
     */
    ~random_center_initializer() = default;

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

private:
    /**
    *
    * @brief    Creates random center and place it to specified storage.
    *
    * @param[in]  p_data: data for that centers are calculated.
    * @param[out] p_centers: storage where new center should be placed.
    *
    */
    void create_center(const dataset & p_data, dataset & p_centers) const;

    /**
    *
    * @brief    Assigns seed to the random generator that is used by the algorithm.
    *
    */
    void initialize_random_generator();
};


}

}