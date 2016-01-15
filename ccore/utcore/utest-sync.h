#ifndef _UTEST_SYNC_
#define _UTEST_SYNC_

#include "ccore/sync.h"

#include "gtest/gtest.h"

static void template_create_delete(const conn_type type, const initial_type initial) {
	sync_network * network = new sync_network(25, 1, 1, type, initial);

	ASSERT_EQ(25, network->size());
	delete network;
}

TEST(utest_sync, create_delete_all_to_all_equipatition) {
	template_create_delete(conn_type::ALL_TO_ALL, initial_type::EQUIPARTITION);
}

TEST(utest_sync, create_delete_all_to_all_gaussian) {
	template_create_delete(conn_type::ALL_TO_ALL, initial_type::RANDOM_GAUSSIAN);
}

TEST(utest_sync, create_delete_list_bidir_equipatition) {
	template_create_delete(conn_type::LIST_BIDIR, initial_type::EQUIPARTITION);
}

TEST(utest_sync, create_delete_list_bidir_gaussian) {
	template_create_delete(conn_type::LIST_BIDIR, initial_type::RANDOM_GAUSSIAN);
}

TEST(utest_sync, create_delete_grid_four_equipatition) {
	template_create_delete(conn_type::GRID_FOUR, initial_type::EQUIPARTITION);
}

TEST(utest_sync, create_delete_grid_four_gaussian) {
	template_create_delete(conn_type::GRID_FOUR, initial_type::RANDOM_GAUSSIAN);
}

TEST(utest_sync, create_delete_grid_eight_equipatition) {
	template_create_delete(conn_type::GRID_EIGHT, initial_type::EQUIPARTITION);
}

TEST(utest_sync, create_delete_grid_eight_gaussian) {
	template_create_delete(conn_type::GRID_EIGHT, initial_type::RANDOM_GAUSSIAN);
}

TEST(utest_sync, create_delete_none_equipatition) {
	template_create_delete(conn_type::NONE, initial_type::EQUIPARTITION);
}

TEST(utest_sync, create_delete_none_gaussian) {
	template_create_delete(conn_type::NONE, initial_type::RANDOM_GAUSSIAN);
}


static void template_dynamic_convergence(const unsigned int number_oscillators, const solve_type solver, const conn_type type, const initial_type initial) {
	sync_network network(number_oscillators, 1, 0, type, initial);

	sync_dynamic output_dynamic;
	network.simulate_dynamic(0.998, 0.1, solver, false, output_dynamic);

	ensemble_data<sync_ensemble> ensembles;
	output_dynamic.allocate_sync_ensembles(0.1, ensembles);

	ASSERT_EQ(1, ensembles.size());
}

TEST(utest_sync, dynamic_convergance_10_oscillators_all_to_all) {
	template_dynamic_convergence(10, solve_type::FAST, conn_type::ALL_TO_ALL, initial_type::EQUIPARTITION);
}

TEST(utest_sync, dynamic_convergance_20_oscillators_all_to_all) {
	template_dynamic_convergence(10, solve_type::FAST, conn_type::ALL_TO_ALL, initial_type::EQUIPARTITION);
}

TEST(utest_sync, dynamic_convergance_16_oscillators_grid_four) {
	template_dynamic_convergence(16, solve_type::FAST, conn_type::GRID_FOUR, initial_type::EQUIPARTITION);
}

TEST(utest_sync, dynamic_convergance_16_oscillators_grid_eight) {
	template_dynamic_convergence(16, solve_type::FAST, conn_type::GRID_EIGHT, initial_type::EQUIPARTITION);
}

TEST(utest_sync, dynamic_convergance_5_oscillators_list_bidir) {
	template_dynamic_convergence(5, solve_type::FAST, conn_type::LIST_BIDIR, initial_type::EQUIPARTITION);
}


static void template_static_convergence(const unsigned int number_oscillators, const solve_type solver, const conn_type type, const initial_type initial) {
	sync_network network(number_oscillators, 1.0, 0, type, initial);

	sync_dynamic output_dynamic;
	network.simulate_static(25, 10, solver, false, output_dynamic);

	ensemble_data<sync_ensemble> ensembles;
	output_dynamic.allocate_sync_ensembles(0.1, ensembles);

	ASSERT_EQ(1, ensembles.size());
}

TEST(utest_sync, static_convergance_10_oscillators_all_to_all) {
	template_static_convergence(10, solve_type::FAST, conn_type::ALL_TO_ALL, initial_type::EQUIPARTITION);
}

TEST(utest_sync, static_convergance_20_oscillators_all_to_all) {
	template_static_convergence(10, solve_type::FAST, conn_type::ALL_TO_ALL, initial_type::EQUIPARTITION);
}

TEST(utest_sync, static_convergance_9_oscillators_grid_four) {
	template_static_convergence(9, solve_type::FAST, conn_type::GRID_FOUR, initial_type::EQUIPARTITION);
}

TEST(utest_sync, static_convergance_9_oscillators_grid_eight) {
	template_static_convergence(9, solve_type::FAST, conn_type::GRID_EIGHT, initial_type::EQUIPARTITION);
}

TEST(utest_sync, static_convergance_3_oscillators_list_bidir) {
	template_static_convergence(3, solve_type::FAST, conn_type::LIST_BIDIR, initial_type::EQUIPARTITION);
}


TEST(utest_sync, static_simulation_runge_kutta_4) {
	template_static_convergence(2, solve_type::RK4, conn_type::ALL_TO_ALL, initial_type::EQUIPARTITION);
}

TEST(utest_sync, static_simulation_runge_kutta_fehlberg_45) {
	template_static_convergence(2, solve_type::RKF45, conn_type::ALL_TO_ALL, initial_type::EQUIPARTITION);
}

TEST(utest_sync, dynamic_simulation_runge_kutta_4) {
	template_dynamic_convergence(2, solve_type::RK4, conn_type::ALL_TO_ALL, initial_type::EQUIPARTITION);
}

TEST(utest_sync, dynamic_simulation_runge_kutta_fehlberg_45) {
	template_dynamic_convergence(2, solve_type::RKF45, conn_type::ALL_TO_ALL, initial_type::EQUIPARTITION);
}


static void template_static_collecting_dynamic(const unsigned int steps) {
	sync_network network(10, 1, 0, conn_type::ALL_TO_ALL, initial_type::EQUIPARTITION);

	sync_dynamic output_dynamic;
	network.simulate_static(steps, 0.1, solve_type::FAST, true, output_dynamic);

	ASSERT_EQ(10, output_dynamic.number_oscillators());
	ASSERT_EQ(steps + 1, output_dynamic.size());
}

TEST(utest_sync, static_collecting_dynamic_25_oscillators) {
    template_static_collecting_dynamic(25);
}


TEST(utest_sync, static_collecting_dynamic_100_oscillators) {
    template_static_collecting_dynamic(100);
}

TEST(utest_sync, dynamic_collecting_dynamic) {
	sync_network network(10, 1, 0, conn_type::ALL_TO_ALL, initial_type::EQUIPARTITION);

	sync_dynamic output_dynamic;
	network.simulate_dynamic(0.998, 0.1, solve_type::FAST, true, output_dynamic);
	
	ASSERT_EQ(10, output_dynamic.number_oscillators());
	ASSERT_GT(output_dynamic.size(), 1);
}

TEST(utest_sync, dynamic_around_zero) {
    sync_dynamic output_dynamic;
    output_dynamic.push_back(sync_network_state(10.0, { 0.01, 0.02, 0.03, 6.25, 6.26, 6.27 }));

    ensemble_data<sync_ensemble> ensembles;
    output_dynamic.allocate_sync_ensembles(0.1, ensembles);

    ASSERT_EQ(1, ensembles.size());

    output_dynamic.allocate_sync_ensembles(0.2, ensembles);

    ASSERT_EQ(1, ensembles.size());

    output_dynamic.clear();
    output_dynamic.push_back(sync_network_state(20.0, { 1.02, 1.05, 1.52, 5.87, 5.98, 5.14 }));

    output_dynamic.allocate_sync_ensembles(2.0, ensembles);

    ASSERT_EQ(1, ensembles.size());
}

#endif
