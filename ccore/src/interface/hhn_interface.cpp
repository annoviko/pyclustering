/**
*
* Copyright (C) 2014-2017    Andrei Novikov (pyclustering@yandex.ru)
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


#include "interface/hhn_interface.h"

#include "nnet/hhn.hpp"


using namespace ccore::nnet;


void * hhn_create(const std::size_t p_size, const void * const p_params) {
    (void) p_size;
    (void) p_params;

    return nullptr;
}


void hhn_destroy(const void * p_network_pointer) {
    (void) p_network_pointer;
}


void * hhn_create_dynamic(bool p_collect_membrane,
                          bool p_collect_active_cond_sodium,
                          bool p_collect_inactive_cond_sodium,
                          bool p_collect_active_cond_potassium)
{
    (void) p_collect_membrane;
    (void) p_collect_active_cond_sodium;
    (void) p_collect_inactive_cond_sodium;
    (void) p_collect_active_cond_potassium;

    return nullptr;
}


void * hhn_destroy_dynamic(const void * p_dynamic) {
    (void) p_dynamic;

    return nullptr;
}


void * hhn_simulate(const void * p_network_pointer,
                    const std::size_t p_steps,
                    const double p_time,
                    const std::size_t p_solver,
                    const pyclustering_package * const p_stimulus,
                    const void * p_output_dynamic)
{
    (void) p_network_pointer;
    (void) p_steps;
    (void) p_time;
    (void) p_solver;
    (void) p_stimulus;
    (void) p_output_dynamic;

    return nullptr;
}


void * hhn_get_dynamic_evolution(const std::size_t p_collection_index) {
    (void) p_collection_index;

    return nullptr;
}