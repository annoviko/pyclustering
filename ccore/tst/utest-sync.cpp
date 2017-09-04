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


#include "gtest/gtest.h"

#include "nnet/sync.hpp"

#include <cmath>


static void template_create_delete(const connection_t type, const initial_type initial) {
    sync_network * network = new sync_network(25, 1, 1, type, initial);

    ASSERT_EQ(25, network->size());
    delete network;
}

TEST(utest_sync, create_delete_all_to_all_equipatition) {
    template_create_delete(connection_t::CONNECTION_ALL_TO_ALL, initial_type::EQUIPARTITION);
}

TEST(utest_sync, create_delete_all_to_all_gaussian) {
    template_create_delete(connection_t::CONNECTION_ALL_TO_ALL, initial_type::RANDOM_GAUSSIAN);
}

TEST(utest_sync, create_delete_list_bidir_equipatition) {
    template_create_delete(connection_t::CONNECTION_LIST_BIDIRECTIONAL, initial_type::EQUIPARTITION);
}

TEST(utest_sync, create_delete_list_bidir_gaussian) {
    template_create_delete(connection_t::CONNECTION_LIST_BIDIRECTIONAL, initial_type::RANDOM_GAUSSIAN);
}

TEST(utest_sync, create_delete_grid_four_equipatition) {
    template_create_delete(connection_t::CONNECTION_GRID_FOUR, initial_type::EQUIPARTITION);
}

TEST(utest_sync, create_delete_grid_four_gaussian) {
    template_create_delete(connection_t::CONNECTION_GRID_FOUR, initial_type::RANDOM_GAUSSIAN);
}

TEST(utest_sync, create_delete_grid_eight_equipatition) {
    template_create_delete(connection_t::CONNECTION_GRID_EIGHT, initial_type::EQUIPARTITION);
}

TEST(utest_sync, create_delete_grid_eight_gaussian) {
    template_create_delete(connection_t::CONNECTION_GRID_EIGHT, initial_type::RANDOM_GAUSSIAN);
}

TEST(utest_sync, create_delete_none_equipatition) {
    template_create_delete(connection_t::CONNECTION_NONE, initial_type::EQUIPARTITION);
}

TEST(utest_sync, create_delete_none_gaussian) {
    template_create_delete(connection_t::CONNECTION_NONE, initial_type::RANDOM_GAUSSIAN);
}


static void template_dynamic_convergence(const unsigned int number_oscillators, const solve_type solver, const connection_t type, const initial_type initial) {
    sync_network network(number_oscillators, 1, 0, type, initial);

    sync_dynamic output_dynamic;
    network.simulate_dynamic(0.998, 0.1, solver, false, output_dynamic);

    ensemble_data<sync_ensemble> ensembles;
    output_dynamic.allocate_sync_ensembles(0.1, ensembles);

    ASSERT_EQ(1, ensembles.size());
}

TEST(utest_sync, dynamic_convergance_10_oscillators_all_to_all) {
    template_dynamic_convergence(10, solve_type::FAST, connection_t::CONNECTION_ALL_TO_ALL, initial_type::EQUIPARTITION);
}

TEST(utest_sync, dynamic_convergance_20_oscillators_all_to_all) {
    template_dynamic_convergence(10, solve_type::FAST, connection_t::CONNECTION_ALL_TO_ALL, initial_type::EQUIPARTITION);
}

TEST(utest_sync, dynamic_convergance_16_oscillators_grid_four) {
    template_dynamic_convergence(16, solve_type::FAST, connection_t::CONNECTION_GRID_FOUR, initial_type::EQUIPARTITION);
}

TEST(utest_sync, dynamic_convergance_16_oscillators_grid_eight) {
    template_dynamic_convergence(16, solve_type::FAST, connection_t::CONNECTION_GRID_EIGHT, initial_type::EQUIPARTITION);
}

TEST(utest_sync, dynamic_convergance_5_oscillators_list_bidir) {
    template_dynamic_convergence(5, solve_type::FAST, connection_t::CONNECTION_LIST_BIDIRECTIONAL, initial_type::EQUIPARTITION);
}


static void template_static_convergence(const unsigned int number_oscillators, const solve_type solver, const connection_t type, const initial_type initial) {
    sync_network network(number_oscillators, 1.0, 0, type, initial);

    sync_dynamic output_dynamic;
    network.simulate_static(25, 10, solver, false, output_dynamic);

    ensemble_data<sync_ensemble> ensembles;
    output_dynamic.allocate_sync_ensembles(0.1, ensembles);

    ASSERT_EQ(1, ensembles.size());
}

TEST(utest_sync, static_convergance_10_oscillators_all_to_all) {
    template_static_convergence(10, solve_type::FAST, connection_t::CONNECTION_ALL_TO_ALL, initial_type::EQUIPARTITION);
}

TEST(utest_sync, static_convergance_20_oscillators_all_to_all) {
    template_static_convergence(10, solve_type::FAST, connection_t::CONNECTION_ALL_TO_ALL, initial_type::EQUIPARTITION);
}

TEST(utest_sync, static_convergance_9_oscillators_grid_four) {
    template_static_convergence(9, solve_type::FAST, connection_t::CONNECTION_GRID_FOUR, initial_type::EQUIPARTITION);
}

TEST(utest_sync, static_convergance_9_oscillators_grid_eight) {
    template_static_convergence(9, solve_type::FAST, connection_t::CONNECTION_GRID_EIGHT, initial_type::EQUIPARTITION);
}

TEST(utest_sync, static_convergance_3_oscillators_list_bidir) {
    template_static_convergence(3, solve_type::FAST, connection_t::CONNECTION_LIST_BIDIRECTIONAL, initial_type::EQUIPARTITION);
}


TEST(utest_sync, static_simulation_runge_kutta_4) {
    template_static_convergence(2, solve_type::RK4, connection_t::CONNECTION_ALL_TO_ALL, initial_type::EQUIPARTITION);
}

TEST(utest_sync, static_simulation_runge_kutta_fehlberg_45) {
    template_static_convergence(2, solve_type::RKF45, connection_t::CONNECTION_ALL_TO_ALL, initial_type::EQUIPARTITION);
}

TEST(utest_sync, dynamic_simulation_runge_kutta_4) {
    template_dynamic_convergence(2, solve_type::RK4, connection_t::CONNECTION_ALL_TO_ALL, initial_type::EQUIPARTITION);
}

TEST(utest_sync, dynamic_simulation_runge_kutta_fehlberg_45) {
    template_dynamic_convergence(2, solve_type::RKF45, connection_t::CONNECTION_ALL_TO_ALL, initial_type::EQUIPARTITION);
}


static void template_static_collecting_dynamic(const unsigned int steps) {
    sync_network network(10, 1, 0, connection_t::CONNECTION_ALL_TO_ALL, initial_type::EQUIPARTITION);

    sync_dynamic output_dynamic;
    network.simulate_static(steps, 0.1, solve_type::FAST, true, output_dynamic);

    ASSERT_EQ(10, output_dynamic.oscillators());
    ASSERT_EQ(steps + 1, output_dynamic.size());
}

TEST(utest_sync, static_collecting_dynamic_25_oscillators) {
    template_static_collecting_dynamic(25);
}


TEST(utest_sync, static_collecting_dynamic_100_oscillators) {
    template_static_collecting_dynamic(100);
}

TEST(utest_sync, dynamic_collecting_dynamic) {
    sync_network network(10, 1, 0, connection_t::CONNECTION_ALL_TO_ALL, initial_type::EQUIPARTITION);

    sync_dynamic output_dynamic;
    network.simulate_dynamic(0.998, 0.1, solve_type::FAST, true, output_dynamic);

    ASSERT_EQ(10, output_dynamic.oscillators());
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


static void template_correlation_matrix(const sync_network_state p_state) {
    sync_dynamic output_dynamic;
    output_dynamic.push_back(p_state);

    sync_corr_matrix corr_matrix;
    output_dynamic.allocate_correlation_matrix(corr_matrix);

    ASSERT_EQ(p_state.size(), corr_matrix.size());
    ASSERT_EQ(p_state.size(), corr_matrix[0].size());

    for (size_t i = 0; i < p_state.size(); i++) {
        for (size_t j = 0; j < p_state.size(); j++) {
            double expected_value = std::abs((double) std::sin(p_state.m_phase[i] - p_state.m_phase[j]));
            ASSERT_NEAR(expected_value, corr_matrix[i][j], 0.00001);
        }
    }
}

TEST(utest_sync, correlation_matrix_similar) {
    template_correlation_matrix(sync_network_state(0, {0.0, 0.0, 0.0}));
}

TEST(utest_sync, correlation_matrix_not_similar_1) {
    template_correlation_matrix(sync_network_state(0, {1.0, 2.0, 3.0}));
}

TEST(utest_sync, correlation_matrix_not_similar_2) {
    template_correlation_matrix(sync_network_state(0, {1.0, 2.0, 3.0, 4.0, 5.0, 6.0}));
}

TEST(utest_sync, correlation_matrix_one_oscillator) {
    template_correlation_matrix(sync_network_state(0, {1.0}));
}


static void template_sync_ordering(const std::size_t p_size, const std::size_t p_steps, const double p_time) {
    sync_network network(p_size, 1, 0, connection_t::CONNECTION_ALL_TO_ALL, initial_type::EQUIPARTITION);

    sync_dynamic output_dynamic;
    network.simulate_static(p_steps, p_time, solve_type::FAST, true, output_dynamic);

    double order_parameter = sync_ordering::calculate_sync_order(output_dynamic[0].m_phase);
    double local_order_parameter = sync_ordering::calculate_local_sync_order(network.connections(), output_dynamic[0].m_phase);

    ASSERT_GT(0.8, order_parameter);
    ASSERT_GT(0.8, local_order_parameter);

    order_parameter = sync_ordering::calculate_sync_order(output_dynamic.back().m_phase);
    local_order_parameter = sync_ordering::calculate_local_sync_order(network.connections(), output_dynamic.back().m_phase);

    ASSERT_LT(0.9, order_parameter);
    ASSERT_LT(0.9, local_order_parameter);
}

TEST(utest_sync, sync_ordering_20_steps) {
    template_sync_ordering(10, 20, 5.0);
}

TEST(utest_sync, sync_ordering_50_steps) {
    template_sync_ordering(10, 50, 5.0);
}


static void template_sync_order_sequence(
        const std::size_t p_size,
        const std::size_t p_steps,
        const double p_time,
        const std::size_t p_start,
        const std::size_t p_stop,
        const bool p_check_result) {

    sync_network network(p_size, 1, 0, connection_t::CONNECTION_ALL_TO_ALL, initial_type::EQUIPARTITION);

    sync_dynamic output_dynamic;
    network.simulate_static(p_steps, p_time, solve_type::FAST, true, output_dynamic);

    std::vector<double> order_sequence;
    std::vector<double> local_order_sequence;

    output_dynamic.calculate_order_parameter(p_start, p_stop, order_sequence);
    output_dynamic.calculate_local_order_parameter(network.connections(), p_start, p_stop, local_order_sequence);

    ASSERT_EQ(p_stop - p_start, order_sequence.size());
    ASSERT_EQ(p_stop - p_start, local_order_sequence.size());

    ASSERT_EQ(p_steps + 1, output_dynamic.size());
    ASSERT_GE(output_dynamic.size(), order_sequence.size());

    if (p_check_result) {
        ASSERT_GT(0.8, order_sequence.front());
        ASSERT_GT(0.8, local_order_sequence.front());

        ASSERT_LT(0.9, order_sequence.back());
        ASSERT_LT(0.9, local_order_sequence.back());
    }
}

TEST(utest_sync, sync_sequence_ordering_10_steps_full) {
    template_sync_order_sequence(10, 10, 5.0, 0, 11 /* the initial state of the network */, true);
}

TEST(utest_sync, sync_sequence_ordering_10_steps_20_size_full) {
    template_sync_order_sequence(20, 10, 5.0, 0, 11 /* the initial state of the network */, true);
}

TEST(utest_sync, sync_sequence_ordering_10_steps_100_size_full) {
    template_sync_order_sequence(100, 10, 5.0, 0, 11 /* the initial state of the network */, true);
}

TEST(utest_sync, sync_sequence_ordering_30_steps_200_size_full) {
    template_sync_order_sequence(200, 30, 5.0, 0, 11 /* the initial state of the network */, true);
}

TEST(utest_sync, sync_sequence_ordering_20_steps_full) {
    template_sync_order_sequence(10, 20, 5.0, 0, 21 /* the initial state of the network */, true);
}

TEST(utest_sync, sync_sequence_ordering_50_steps_full) {
    template_sync_order_sequence(10, 50, 5.0, 0, 51 /* the initial state of the network */, true);
}

TEST(utest_sync, sync_sequence_ordering_200_steps_full) {
    template_sync_order_sequence(10, 200, 5.0, 0, 201 /* the initial state of the network */, true);
}

TEST(utest_sync, sync_sequence_ordering_10_oscillators_partial) {
    template_sync_order_sequence(10, 20, 5.0, 10, 15, false);
}

TEST(utest_sync, sync_sequence_ordering_20_oscillators_partial) {
    template_sync_order_sequence(20, 20, 5.0, 10, 15, false);
}

TEST(utest_sync, sync_sequence_ordering_40_oscillators_partial) {
    template_sync_order_sequence(40, 20, 5.0, 10, 15, false);
}

TEST(utest_sync, sync_sequence_ordering_one_back) {
    template_sync_order_sequence(10, 20, 5.0, 10, 11, false);
}

TEST(utest_sync, sync_sequence_ordering_one_front) {
    template_sync_order_sequence(10, 20, 5.0, 0, 1, false);
}

TEST(utest_sync, sync_sequence_ordering_one_middle) {
    template_sync_order_sequence(10, 20, 5.0, 5, 6, false);
}
