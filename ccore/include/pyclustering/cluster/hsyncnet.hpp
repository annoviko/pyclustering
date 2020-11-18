/*!

@authors Andrei Novikov (pyclustering@yandex.ru)
@date 2014-2020
@copyright BSD-3-Clause

*/

#pragma once


#include <vector>

#include <pyclustering/definitions.hpp>
#include <pyclustering/cluster/syncnet.hpp>


namespace pyclustering {

namespace clst {


typedef std::vector<std::size_t>            hsyncnet_cluster;
typedef ensemble_data<hsyncnet_cluster>     hsyncnet_cluster_data;
typedef syncnet_analyser                    hsyncnet_analyser;


/*!

@class   hsyncnet hsyncnet.hpp pyclustering/cluster/hsyncnet.hpp

@brief   Oscillatory neural network based on Kuramoto model for cluster analysis.

@see hsyncnet_analyser

*/
class hsyncnet: public syncnet {
private:
    std::size_t m_number_clusters;
    std::size_t m_initial_neighbors;
    double m_increase_persent;
    double m_time;

private:
    const static double         DEFAULT_TIME_STEP;
    const static std::size_t    DEFAULT_INCREASE_STEP;

public:
    /*!

    @brief    Constructor of HSyncNet (Hierarchical Sync Network) algorithm.

    @param[in] input_data: input data for cluster analysis.
    @param[in] cluster_number: amount of clusters that should be allocated.
    @param[in] initial_phases: initial phases for oscillators.

    */
    hsyncnet(dataset * input_data, 
        const std::size_t cluster_number, 
        const initial_type initial_phases);

    /*!

    @brief    Constructor of HSyncNet (Hierarchical Sync Network) algorithm.

    @param[in] input_data: input data for cluster analysis.
    @param[in] cluster_number: amount of clusters that should be allocated.
    @param[in] initial_phases: initial phases for oscillators.
    @param[in] initial_neighbors: defines initial connectivity-radius by average distance to connect specified amount of oscillators (points).
    @param[in] increase_persent: percent of increasing of connectivity-radius on each iteration (input values in range (0.0; 1.0) correspond to (0%; 100%)).
    
    */
    hsyncnet(dataset * input_data,
        const std::size_t cluster_number,
        const initial_type initial_phases,
        const std::size_t initial_neighbors,
        const double increase_persent);

    /*!

    @brief    Default destructor of HSyncNet (Hierarchical Sync Network) algorithm.

    */
    virtual ~hsyncnet() = default;

public:
    /*!

    @brief Performs cluster analysis by the network simulation.

    @param[in]  order: order of synchronization that is used as indication for stopping processing, the `order` value should be in range `(0, 1)`.
    @param[in]  solver: specified type of solving diff. equation.
    @param[in]  collect_dynamic: specified requirement to collect whole dynamic of the network.
    @param[out] analyser: analyser of sync results of clustering.

    */
    virtual void process(const double order, const solve_type solver, const bool collect_dynamic, hsyncnet_analyser & analyser) override;

private:
    void store_state(sync_network_state & state, hsyncnet_analyser & analyser);

    double calculate_radius(const double radius, const std::size_t amount_neighbors) const;
};


}

}