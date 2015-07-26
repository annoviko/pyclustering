#ifndef _UTEST_LEGION_
#define _UTEST_LEGION_

#include "ccore/legion.h"

#include "gtest/gtest.h"

static void template_create_delete(const unsigned int num_osc, const conn_type type) {
	legion_parameters parameters;
	legion_network * network = new legion_network(num_osc, type, parameters);

	ASSERT_EQ(num_osc, network->size());

	delete network;
}

TEST(utest_legion, create_10_oscillators_none_conn) {
	template_create_delete(10, conn_type::NONE);
}

TEST(utest_legion, create_25_oscillators_grid_four_conn) {
	template_create_delete(25, conn_type::GRID_FOUR);
}

TEST(utest_legion, create_25_oscillators_grid_eight_conn) {
	template_create_delete(25, conn_type::GRID_EIGHT);
}

TEST(utest_legion, create_10_oscillators_bidir_conn) {
	template_create_delete(10, conn_type::LIST_BIDIR);
}

TEST(utest_legion, create_10_oscillators_all_to_all_conn) {
	template_create_delete(10, conn_type::ALL_TO_ALL);
}

TEST(utest_legion, create_10_oscillators_dynamic_conn) {
	template_create_delete(10, conn_type::DYNAMIC);
}


static void template_dynamic_simulation(const legion_stimulus & stimulus, const conn_type type, const solve_type solver, const unsigned int steps, const double time) {
	legion_parameters parameters;
	legion_network network(stimulus.size(), type, parameters);

	legion_dynamic output_legion_dynamic;
	network.simulate(steps, time, solver, true, stimulus, output_legion_dynamic);

	ASSERT_EQ(steps, output_legion_dynamic.size());
}

TEST(utest_legion, one_unstimulated_oscillator_rk4) {
	template_dynamic_simulation({ 0 }, conn_type::NONE, solve_type::RK4, 10, 100);
}

TEST(utest_legion, one_stimulated_oscillator_rk4) {
	template_dynamic_simulation({ 1 }, conn_type::GRID_FOUR, solve_type::RK4, 10, 100);
}

TEST(utest_legion, dynamic_simulation_grid_four_rk4) {
	template_dynamic_simulation({ 1, 1, 1, 0, 0, 0, 1, 1, 1 }, conn_type::GRID_FOUR, solve_type::RK4, 10, 100);
}

TEST(utest_legion, dynamic_simulation_grid_eight_rk4) {
	template_dynamic_simulation({ 1, 1, 1, 0, 0, 0, 1, 1, 1 }, conn_type::GRID_EIGHT, solve_type::RK4, 10, 100);
}

#endif
