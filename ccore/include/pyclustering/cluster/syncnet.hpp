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


#include <vector>

#include <pyclustering/nnet/sync.hpp>


using namespace pyclustering::nnet;


namespace pyclustering {

namespace clst {


using syncnet_cluster       = std::vector<std::size_t>;
using syncnet_cluster_data  = ensemble_data<syncnet_cluster>;


/*

@brief   Analyser for syncnet - oscillatory neural network based on Kuramoto model for cluster analysis.

@see syncnet

*/
class syncnet_analyser: public sync_dynamic {
public:
    syncnet_analyser() = default;

    virtual ~syncnet_analyser() = default;

public:
    void allocate_clusters(const double eps, syncnet_cluster_data & data);
};


/*

@brief   Oscillatory neural network based on Kuramoto model for cluster analysis.

@see syncnet_analyser

 */
class syncnet: public sync_network {
protected:
    std::vector<std::vector<double> >    * oscillator_locations;
    std::vector<std::vector<double> >    * distance_conn_weights;
    double                                connection_weight;

public:
    /*
    
    @brief   Contructor of the adapted oscillatory network SYNC for cluster analysis.
    
    @param[in] input_data: input data for clustering.
    @param[in] connectivity_radius: connectivity radius between points.
    @param[in] enable_conn_weight: if True - enable mode when strength between oscillators 
                depends on distance between two oscillators. Otherwise all connection between 
                oscillators have the same strength.
    @param[in] initial_phases: type of initialization of initial phases of oscillators.
    
    */
    syncnet(std::vector<std::vector<double> > * input_data, const double connectivity_radius, const bool enable_conn_weight, const initial_type initial_phases);

    /*
    
    @brief   Copy-contructor of the sync-net algorithm is forbidden.
    
    @param[in] p_other: other syncnet instance.
    
    */
    syncnet(const syncnet & p_other) = delete;

    /*
    
    @brief   Default destructor.
    
    */
    virtual ~syncnet();

    /*
    
    @brief Network is trained via achievement sync state between the oscillators using the radius of coupling.
    
    @param[in]  order: order of synchronization that is used as indication for stopping processing.
    @param[in]  solver: specified type of solving diff. equation. 
    @param[in]  collect_dynamic: specified requirement to collect whole dynamic of the network.
    @param[out] analyser: analyser of sync results of clustering.
    
    */
    virtual void process(const double order, const solve_type solver, const bool collect_dynamic, syncnet_analyser & analyser);

    /*
    
    @brief   Overrided method for calculation of oscillator phase.
    
    @param[in] t: current value of phase.
    @param[in] teta: time (can be ignored). 
    @param[in] argv: index of oscillator whose phase represented by argument teta.
    
    @return  Return new value of phase of oscillator with index 'argv'.
    
    */
    virtual double phase_kuramoto(const double t, const double teta, const std::vector<void *> & argv) const override;

    virtual void phase_kuramoto_equation(const double t, const differ_state<double> & inputs, const differ_extra<void *> & argv, differ_state<double> & outputs) const override;

public:
    /*
    
    @brief   Assignment operator for the sync-net algorithm is forbidden.
    
    @param[in] p_other: other syncnet instance.
    
    */
    syncnet & operator=(const syncnet & p_other) = delete;

protected:
    /*
    
    @brief   Create connections between oscillators in line with input radius of connectivity.
    
    
    @param[in] connectivity_radius: connectivity radius between oscillators.
    @param[in] enable_conn_weight: if True - enable mode when strength between oscillators 
                depends on distance between two oscillators. Otherwise all connection between 
                oscillators have the same strength.
     
    */
    void create_connections(const double connectivity_radius, const bool enable_conn_weight);
};


}

}