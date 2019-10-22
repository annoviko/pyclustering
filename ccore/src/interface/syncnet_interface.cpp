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

#include <pyclustering/interface/syncnet_interface.h>

#include <pyclustering/cluster/syncnet.hpp>


using namespace pyclustering::clst;
using namespace pyclustering::nnet;


void * syncnet_create_network(const pyclustering_package * const p_sample, const double p_connectivity_radius, const bool p_enable_conn_weight, const unsigned int p_initial_phases) {
    pyclustering::dataset input_data;
    p_sample->extract(input_data);

    return new syncnet(&input_data, p_connectivity_radius, p_enable_conn_weight, (initial_type) p_initial_phases);
}


void syncnet_destroy_network(const void * p_pointer_network) {
    delete (syncnet *) p_pointer_network;
}


void * syncnet_process(const void * p_pointer_network, const double p_order, const unsigned int p_solver, const bool p_collect_dynamic) {
    syncnet * network = (syncnet *) p_pointer_network;

    syncnet_analyser * analyser = new syncnet_analyser();
    network->process(p_order, (solve_type) p_solver, p_collect_dynamic, (*analyser));

    ensemble_data<sync_ensemble> ensembles;
    analyser->allocate_sync_ensembles(0.1, ensembles);

    return analyser;
}


void syncnet_analyser_destroy(const void * p_pointer_analyser) {
    delete (syncnet_analyser *) p_pointer_analyser;
}