/*!

@authors Andrei Novikov (pyclustering@yandex.ru)
@date 2014-2020
@copyright BSD-3-Clause

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