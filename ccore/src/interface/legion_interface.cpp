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

#include <pyclustering/interface/legion_interface.h>

#include <pyclustering/nnet/legion.hpp>


using namespace pyclustering::nnet;


void * legion_create(const unsigned int p_size, const unsigned int p_connection_type, const void * const p_parameters) {
    legion_network * network = new legion_network(p_size, (connection_t) p_connection_type, *((legion_parameters *) p_parameters));
    return (void *) network;
}


void legion_destroy(const void * p_network_pointer) {
    delete (legion_network *) p_network_pointer;
}


void * legion_simulate( const void * p_network_pointer,
                        const unsigned int p_steps, 
                        const double p_time,
                        const unsigned int p_solver,
                        const bool p_collect_dynamic,
                        const pyclustering_package * const p_stimulus)
{
  legion_stimulus stimulus_vector((double *)p_stimulus->data, ((double *)p_stimulus->data) + p_stimulus->size);

  legion_dynamic * dynamic = new legion_dynamic();
  ((legion_network *) p_network_pointer)->simulate(p_steps, p_time, (solve_type) p_solver, p_collect_dynamic, stimulus_vector, (*dynamic));

  return dynamic;
}


std::size_t legion_get_size(const void * p_network_pointer) {
    return ((legion_network *) p_network_pointer)->size();
}


void legion_dynamic_destroy(const void * p_dynamic_pointer) {
    delete (legion_dynamic *) p_dynamic_pointer;
}


pyclustering_package * legion_dynamic_get_output(const void * p_dynamic_pointer) {
    legion_dynamic & dynamic = *((legion_dynamic *) p_dynamic_pointer);

    pyclustering_package * package = new pyclustering_package(pyclustering_data_t::PYCLUSTERING_TYPE_LIST);
    package->size = dynamic.size();
    package->data = new pyclustering_package * [package->size];

    for (std::size_t i = 0; i < package->size; i++) {
        ((pyclustering_package **) package->data)[i] = create_package(&dynamic[i].m_output);
    }

    return package;
}


pyclustering_package * legion_dynamic_get_inhibitory_output(const void * p_dynamic_pointer) {
    legion_dynamic & dynamic = *((legion_dynamic *) p_dynamic_pointer);

    pyclustering_package * package = new pyclustering_package(pyclustering_data_t::PYCLUSTERING_TYPE_DOUBLE);
    package->size = dynamic.size();
    package->data = new double[package->size];

    for (std::size_t i = 0; i < package->size; i++) {
        ((double *) package->data)[i] = dynamic[i].m_inhibitor;
    }

    return package;
}


pyclustering_package * legion_dynamic_get_time(const void * p_dynamic_pointer) {
    legion_dynamic & dynamic = *((legion_dynamic *) p_dynamic_pointer);

    pyclustering_package * package = new pyclustering_package(pyclustering_data_t::PYCLUSTERING_TYPE_DOUBLE);
    package->size = dynamic.size();
    package->data = new double[package->size];

    for (std::size_t i = 0; i < package->size; i++) {
        ((double *) package->data)[i] = dynamic[i].m_time;
    }

    return package;
}


std::size_t legion_dynamic_get_size(const void * p_dynamic_pointer) {
    return ((legion_dynamic *) p_dynamic_pointer)->size();
}
