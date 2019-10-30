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


#include <pyclustering/interface/sync_interface.h>

#include <pyclustering/nnet/sync.hpp>


using namespace pyclustering::nnet;


void * sync_create_network(const unsigned int size, const double weight_factor, const double frequency_factor, const unsigned int connection_type, const unsigned int initial_phases) {
    return new sync_network(size, weight_factor, frequency_factor, (connection_t) connection_type, (initial_type) initial_phases);
}


std::size_t sync_get_size(const void * pointer_network) {
    return ((sync_network *) pointer_network)->size();
}


void sync_destroy_network(const void * pointer_network) {
    if (pointer_network != nullptr) {
        delete (sync_network *) pointer_network;
    }
}


void * sync_simulate_static(const void * pointer_network, unsigned int steps, const double time, const unsigned int solver, const bool collect_dynamic) {
    sync_network * network = (sync_network *) pointer_network;

    sync_dynamic * dynamic = new sync_dynamic();
    network->simulate_static(steps, time, (solve_type) solver, collect_dynamic, (*dynamic));

    return (void *) dynamic;
}


void * sync_simulate_dynamic(const void * pointer_network, const double order, const unsigned int solver, const bool collect_dynamic, const double step, const double step_int, const double threshold_changes) {
    sync_network * network = (sync_network *) pointer_network;

    sync_dynamic * dynamic = new sync_dynamic();
    network->simulate_dynamic(order, step, (solve_type) solver, collect_dynamic, (*dynamic));

    return (void *) dynamic;
}


double sync_order(const void * pointer_network) {
    return ((sync_network *) pointer_network)->sync_order();
}


double sync_local_order(const void * pointer_network) {
    return ((sync_network *) pointer_network)->sync_local_order();
}


pyclustering_package * sync_connectivity_matrix(const void * pointer_network) {
    std::shared_ptr<adjacency_collection> connections = ((sync_network *) pointer_network)->connections();

    pyclustering_package * package = new pyclustering_package(pyclustering_data_t::PYCLUSTERING_TYPE_LIST);
    package->size = ((sync_network *) pointer_network)->size();
    package->data = new pyclustering_package * [package->size];

    for (std::size_t i = 0; i < package->size; i++) {
        pyclustering_package * subpackage = new pyclustering_package(pyclustering_data_t::PYCLUSTERING_TYPE_DOUBLE);
        subpackage->size = ((sync_network *) pointer_network)->size();
        subpackage->data = (void *) new double[subpackage->size];

        for (std::size_t j = 0; j < subpackage->size; j++) {
            ((double *) subpackage->data)[j] = connections->has_connection(i, j) ? 1.0 : 0.0;
        }

        ((pyclustering_package **) package->data)[i] = subpackage;
    }

    return package;
}


std::size_t sync_dynamic_get_size(const void * pointer_dynamic) {
    return ((sync_dynamic *) pointer_dynamic)->size();
}


void sync_dynamic_destroy(const void * pointer_dynamic) {
    delete (sync_dynamic *) pointer_dynamic;
}


pyclustering_package * sync_dynamic_allocate_sync_ensembles(const void * pointer_dynamic, const double tolerance, const std::size_t iteration) {
    ensemble_data<sync_ensemble> ensembles;

    ((sync_dynamic *)pointer_dynamic)->allocate_sync_ensembles(tolerance, iteration, ensembles);

    pyclustering_package * package = create_package(&ensembles);
    return package;
}


pyclustering_package * sync_dynamic_allocate_correlation_matrix(const void * pointer_dynamic, const std::size_t iteration) {
    sync_corr_matrix matrix;
    ((sync_dynamic *) pointer_dynamic)->allocate_correlation_matrix(iteration, matrix);

    pyclustering_package * package = create_package(&matrix);
    return package;
}


pyclustering_package * sync_dynamic_get_time(const void * pointer_dynamic) {
    sync_dynamic & dynamic = *((sync_dynamic *)pointer_dynamic);

    pyclustering_package * package = new pyclustering_package(pyclustering_data_t::PYCLUSTERING_TYPE_DOUBLE);
    package->size = dynamic.size();
    package->data = new double[package->size];

    for (std::size_t i = 0; i < package->size; i++) {
        ((double *) package->data)[i]  = dynamic[i].m_time;
    }

    return package;
}


pyclustering_package * sync_dynamic_get_output(const void * pointer_dynamic) {
    sync_dynamic & dynamic = *((sync_dynamic *)pointer_dynamic);

    pyclustering_package * package = new pyclustering_package(pyclustering_data_t::PYCLUSTERING_TYPE_LIST);
    package->size = dynamic.size();
    package->data = new pyclustering_package * [package->size];

    for (std::size_t i = 0; i < package->size; i++) {
        ((pyclustering_package **) package->data)[i] = create_package(&dynamic[i].m_phase);
    }

    return package;
}


pyclustering_package * sync_dynamic_calculate_order(const void * p_pointer, const std::size_t p_start, const std::size_t p_stop) {
    sync_dynamic & dynamic = *((sync_dynamic *) p_pointer);

    std::vector<double> order_evolution;
    dynamic.calculate_order_parameter(p_start, p_stop, order_evolution);

    pyclustering_package * package = create_package(&order_evolution);
    return package;
}


pyclustering_package * sync_dynamic_calculate_local_order(const void * p_dynamic_pointer, const void * p_network_pointer, const std::size_t p_start, const std::size_t p_stop) {
    sync_dynamic & dynamic = *((sync_dynamic *) p_dynamic_pointer);
    sync_network & network = *((sync_network *) p_network_pointer);

    std::vector<double> local_order_evolution;
    dynamic.calculate_local_order_parameter(network.connections(), p_start, p_stop, local_order_evolution);

    pyclustering_package * package = create_package(&local_order_evolution);
    return package;
}