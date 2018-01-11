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

#include "interface/pcnn_interface.h"


using namespace ccore::nnet;


void * pcnn_create(const unsigned int p_size, const unsigned int p_connection_type, const unsigned int p_height, const unsigned int p_width, const void * const p_parameters) {
    pcnn * pcnn_network = new pcnn(p_size, (connection_t) p_connection_type, p_height, p_width, *((pcnn_parameters *) p_parameters));
    return (void *) pcnn_network;
}


void pcnn_destroy(const void * pointer) {
    delete (pcnn *) pointer;
}


void * pcnn_simulate(const void * pointer, const unsigned int steps, const void * const stimulus) {
    const pyclustering_package * const package_stimulus = (const pyclustering_package * const) stimulus;
    pcnn_stimulus stimulus_vector((double *) package_stimulus->data, ((double *) package_stimulus->data) + package_stimulus->size);

    pcnn_dynamic * dynamic = new pcnn_dynamic();
    ((pcnn *) pointer)->simulate(steps, stimulus_vector, (*dynamic));

    return dynamic;
}


std::size_t pcnn_get_size(const void * pointer) {
    return ((pcnn *) pointer)->size();
}


void pcnn_dynamic_destroy(const void * pointer) {
    delete (pcnn_dynamic *) pointer;
}


pyclustering_package * pcnn_dynamic_allocate_sync_ensembles(const void * pointer) {
    ensemble_data<pcnn_ensemble> sync_ensembles;
    ((pcnn_dynamic *) pointer)->allocate_sync_ensembles(sync_ensembles);

    pyclustering_package * package = create_package(&sync_ensembles);
    return package;
}


pyclustering_package * pcnn_dynamic_allocate_spike_ensembles(const void * pointer) {
    ensemble_data<pcnn_ensemble> spike_ensembles;
    ((pcnn_dynamic *) pointer)->allocate_spike_ensembles(spike_ensembles);

    pyclustering_package * package = create_package(&spike_ensembles);
    return package;
}


pyclustering_package * pcnn_dynamic_allocate_time_signal(const void * pointer) {
    pcnn_time_signal time_signal;
    ((pcnn_dynamic *) pointer)->allocate_time_signal(time_signal);

    pyclustering_package * package = create_package(&time_signal);
    return package;
}


pyclustering_package * pcnn_dynamic_get_output(const void * pointer) {
    pcnn_dynamic & dynamic = *((pcnn_dynamic *) pointer);

    pyclustering_package * package = new pyclustering_package(pyclustering_type_data::PYCLUSTERING_TYPE_LIST);
    package->size = dynamic.size();
    package->data = new pyclustering_package * [package->size];

    for (unsigned int i = 0; i < package->size; i++) {
        ((pyclustering_package **) package->data)[i] = create_package(&dynamic[i].m_output);
    }

    return package;
}


pyclustering_package * pcnn_dynamic_get_time(const void * pointer) {
    pcnn_dynamic & dynamic = *((pcnn_dynamic *) pointer);

    pyclustering_package * package = new pyclustering_package(pyclustering_type_data::PYCLUSTERING_TYPE_DOUBLE);
    package->size = dynamic.size();
    package->data = new double[package->size];

    for (unsigned int i = 0; i < package->size; i++) {
        ((double *) package->data)[i]  = dynamic[i].m_time;
    }

    return package;
}


size_t pcnn_dynamic_get_size(const void * pointer) {
    return ((pcnn_dynamic *) pointer)->size();
}

