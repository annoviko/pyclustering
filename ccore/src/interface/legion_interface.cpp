/**
*
* Copyright (C) 2014-2018    Andrei Novikov (pyclustering@yandex.ru)
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

#include "interface/legion_interface.h"

#include "nnet/legion.hpp"


using namespace ccore::nnet;


void * legion_create(const unsigned int size, const unsigned int connection_type, const void * const parameters) {
    legion_network * network = new legion_network(size, (connection_t) connection_type, *((legion_parameters *) parameters));
    return (void *) network;
}


void legion_destroy(const void * pointer) {
    delete (legion_network *) pointer;
}


void * legion_simulate( const void * pointer, 
                        const unsigned int steps, 
                        const double time, 
                        const unsigned int solver, 
                        const bool collect_dynamic, 
                        const void * const stimulus ) 
{
  const pyclustering_package * const package_stimulus = (const pyclustering_package * const) stimulus;
  legion_stimulus stimulus_vector((double *) package_stimulus->data, ((double *) package_stimulus->data) + package_stimulus->size);

  legion_dynamic * dynamic = new legion_dynamic();
  ((legion_network *) pointer)->simulate(steps, time, (solve_type) solver, collect_dynamic, stimulus_vector, (*dynamic));

  return dynamic;
}


std::size_t legion_get_size(const void * pointer) {
    return ((legion_network *) pointer)->size();
}


void legion_dynamic_destroy(const void * pointer) {
    delete (legion_dynamic *) pointer;
}


pyclustering_package * legion_dynamic_get_output(const void * pointer) {
    legion_dynamic & dynamic = *((legion_dynamic *) pointer);

    pyclustering_package * package = new pyclustering_package(pyclustering_type_data::PYCLUSTERING_TYPE_LIST);
    package->size = dynamic.size();
    package->data = new pyclustering_package * [package->size];

    for (unsigned int i = 0; i < package->size; i++) {
        ((pyclustering_package **) package->data)[i] = create_package(&dynamic[i].m_output);
    }

    return package;
}


pyclustering_package * legion_dynamic_get_inhibitory_output(const void * pointer) {
    legion_dynamic & dynamic = *((legion_dynamic *) pointer);

    pyclustering_package * package = new pyclustering_package(pyclustering_type_data::PYCLUSTERING_TYPE_DOUBLE);
    package->size = dynamic.size();
    package->data = new double[package->size];

    for (unsigned int i = 0; i < package->size; i++) {
        ((double *) package->data)[i] = dynamic[i].m_inhibitor;
    }

    return package;
}


pyclustering_package * legion_dynamic_get_time(const void * pointer) {
    legion_dynamic & dynamic = *((legion_dynamic *) pointer);

    pyclustering_package * package = new pyclustering_package(pyclustering_type_data::PYCLUSTERING_TYPE_DOUBLE);
    package->size = dynamic.size();
    package->data = new double[package->size];

    for (unsigned int i = 0; i < package->size; i++) {
        ((double *) package->data)[i] = dynamic[i].m_time;
    }

    return package;
}


std::size_t legion_dynamic_get_size(const void * pointer) {
    return ((legion_dynamic *) pointer)->size();
}
