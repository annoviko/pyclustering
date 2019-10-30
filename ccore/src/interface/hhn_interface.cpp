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


#include <fstream>

#include <pyclustering/interface/hhn_interface.h>

#include <pyclustering/differential/solve_type.hpp>

#include <pyclustering/nnet/hhn.hpp>


using namespace pyclustering::nnet;


void * hhn_create(const std::size_t p_size, const void * const p_params) {
    hhn_network * network = new hhn_network(p_size, *((hnn_parameters *) p_params));
    return network;
}


void hhn_destroy(const void * p_network_pointer) {
    delete (hhn_network *) p_network_pointer;
}


void * hhn_dynamic_create(bool p_collect_membrane, bool p_collect_active_cond_sodium, bool p_collect_inactive_cond_sodium, bool p_collect_active_cond_potassium) {
    hhn_dynamic * output_dynamic = new hhn_dynamic();
    output_dynamic->disable_all();

    if (p_collect_membrane) {
        output_dynamic->enable(hhn_dynamic::collect::MEMBRANE_POTENTIAL);
    }

    if (p_collect_active_cond_sodium) {
        output_dynamic->enable(hhn_dynamic::collect::ACTIVE_COND_SODIUM);
    }

    if (p_collect_inactive_cond_sodium) {
        output_dynamic->enable(hhn_dynamic::collect::INACTIVE_COND_SODIUM);
    }

    if (p_collect_active_cond_potassium) {
        output_dynamic->enable(hhn_dynamic::collect::ACTIVE_COND_POTASSIUM);
    }

    return output_dynamic;
}


void hhn_dynamic_destroy(const void * p_dynamic) {
    delete (hhn_dynamic *) p_dynamic;
}


void hhn_simulate(const void * p_network_pointer,
                  const std::size_t p_steps,
                  const double p_time,
                  const std::size_t p_solver,
                  const pyclustering_package * const p_stimulus,
                  const void * p_output_dynamic)
{
    hhn_network * network = (hhn_network *) p_network_pointer;
    hhn_dynamic * dynamic = (hhn_dynamic *) p_output_dynamic;

    hhn_stimulus stimulus_vector((double *)p_stimulus->data, ((double *)p_stimulus->data) + p_stimulus->size);

    network->simulate(p_steps, p_time, (solve_type) p_solver, stimulus_vector, *dynamic);
}


pyclustering_package * hhn_dynamic_get_peripheral_evolution(const void * p_output_dynamic, const std::size_t p_collection_index) {
    hhn_dynamic * dynamic = (hhn_dynamic *) p_output_dynamic;
    hhn_dynamic::evolution_dynamic & evolution = dynamic->get_peripheral_dynamic((hhn_dynamic::collect) p_collection_index);

    pyclustering_package * package = create_package(&evolution);
    return package;
}


pyclustering_package * hhn_dynamic_get_central_evolution(const void * p_output_dynamic, const std::size_t p_collection_index) {
    hhn_dynamic * dynamic = (hhn_dynamic *) p_output_dynamic;
    hhn_dynamic::evolution_dynamic & evolution = dynamic->get_central_dynamic((hhn_dynamic::collect) p_collection_index);

    pyclustering_package * package = create_package(&evolution);
    return package;
}


pyclustering_package * hhn_dynamic_get_time(const void * p_output_dynamic) {
    hhn_dynamic * dynamic = (hhn_dynamic *) p_output_dynamic;
    hhn_dynamic::value_dynamic_ptr evolution = dynamic->get_time();

    pyclustering_package * package = create_package(evolution.get());
    return package;
}


void hhn_dynamic_write(const void * p_output_dynamic, const char * p_filename) {
    hhn_dynamic * dynamic = (hhn_dynamic *) p_output_dynamic;
    std::ofstream file_stream(p_filename);
    file_stream << *dynamic;
    file_stream.close();
}


void * hhn_dynamic_read(const char * p_filename) {
    hhn_dynamic * output_dynamic = new hhn_dynamic();
    hhn_dynamic_reader(p_filename).read(*output_dynamic);
    return output_dynamic;
}
