/**
*
* Copyright (C) 2014-2016    Andrei Novikov (pyclustering@yandex.ru)
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

#ifndef _UTEST_LEGION_
#define _UTEST_LEGION_


#include "gtest/gtest.h"

#include "nnet/legion.hpp"


static void template_create_delete(const unsigned int num_osc, const connection_t type) {
	legion_parameters parameters;
	legion_network * network = new legion_network(num_osc, type, parameters);

	ASSERT_EQ(num_osc, network->size());

	delete network;
}

TEST(utest_legion, create_10_oscillators_none_conn) {
	template_create_delete(10, connection_t::CONNECTION_NONE);
}

TEST(utest_legion, create_25_oscillators_grid_four_conn) {
	template_create_delete(25, connection_t::CONNECTION_GRID_FOUR);
}

TEST(utest_legion, create_25_oscillators_grid_eight_conn) {
	template_create_delete(25, connection_t::CONNECTION_GRID_EIGHT);
}

TEST(utest_legion, create_10_oscillators_bidir_conn) {
	template_create_delete(10, connection_t::CONNECTION_LIST_BIDIRECTIONAL);
}

TEST(utest_legion, create_10_oscillators_all_to_all_conn) {
	template_create_delete(10, connection_t::CONNECTION_ALL_TO_ALL);
}


static void template_dynamic_simulation(const legion_stimulus & stimulus, const connection_t type, const solve_type solver, const unsigned int steps, const double time) {
	legion_parameters parameters;
	legion_network network(stimulus.size(), type, parameters);

	legion_dynamic output_legion_dynamic;
	network.simulate(steps, time, solver, true, stimulus, output_legion_dynamic);

	ASSERT_EQ(steps, output_legion_dynamic.size());
}

TEST(utest_legion, one_unstimulated_oscillator_rk4) {
	template_dynamic_simulation({ 0 }, connection_t::CONNECTION_NONE, solve_type::RK4, 10, 100);
}

TEST(utest_legion, one_stimulated_oscillator_rk4) {
	template_dynamic_simulation({ 1 }, connection_t::CONNECTION_GRID_FOUR, solve_type::RK4, 10, 100);
}

TEST(utest_legion, dynamic_simulation_grid_four_rk4) {
	template_dynamic_simulation({ 1, 1, 1, 0, 0, 0, 1, 1, 1 }, connection_t::CONNECTION_GRID_FOUR, solve_type::RK4, 10, 100);
}

TEST(utest_legion, dynamic_simulation_grid_eight_rk4) {
	template_dynamic_simulation({ 1, 1, 1, 0, 0, 0, 1, 1, 1 }, connection_t::CONNECTION_GRID_EIGHT, solve_type::RK4, 10, 100);
}

#endif
