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

#include <pyclustering/interface/hsyncnet_interface.h>

#include <pyclustering/cluster/hsyncnet.hpp>


using namespace pyclustering::clst;
using namespace pyclustering::nnet;


void * hsyncnet_create_network(const pyclustering_package * const p_sample, 
                               const unsigned int p_number_clusters, 
                               const unsigned int p_initial_phases,
                               const unsigned int p_initial_neighbors,
                               const double p_increase_persent) {

    pyclustering::dataset input_data;
    p_sample->extract(input_data);

    return new hsyncnet(&input_data, p_number_clusters, (initial_type) p_initial_phases, p_initial_neighbors, p_increase_persent);
}


void hsyncnet_destroy_network(const void * p_pointer_network) {
    delete (hsyncnet *) p_pointer_network;
}


void * hsyncnet_process(const void * p_pointer_network, const double p_order, const unsigned int p_solver, const bool p_collect_dynamic) {
    hsyncnet * network = (hsyncnet *) p_pointer_network;

    hsyncnet_analyser * analyser = new hsyncnet_analyser();
    network->process(p_order, (solve_type) p_solver, p_collect_dynamic, *analyser);

    return (void *) analyser;
}


void hsyncnet_analyser_destroy(const void * p_pointer_analyser) {
    delete (hsyncnet_analyser *) p_pointer_analyser;
}