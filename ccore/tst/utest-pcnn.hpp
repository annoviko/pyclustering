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

#ifndef _UTEST_PCNN_
#define _UTEST_PCNN_


#include "gtest/gtest.h"

#include "nnet/pcnn.hpp"

#include <unordered_set>


static void template_dynamic_generation_runner(
    pcnn & network,
    const unsigned int steps,
    const connection_t type_conn,
    const pcnn_stimulus & stimulus) {

    pcnn_dynamic dynamic;
    network.simulate(steps, stimulus, dynamic);

    ASSERT_EQ(steps, dynamic.size());

    /* check that each iteration of output dynamic has states for the same number of oscillators */
    for (unsigned int index = 0; index < network.size(); index++) {
        ASSERT_EQ(network.size(), dynamic[index].m_output.size());
        ASSERT_EQ(network.size(), dynamic.dynamic_at(index).size());
    }

    pcnn_time_signal time_signal;
    dynamic.allocate_time_signal(time_signal);

    ASSERT_EQ(steps, time_signal.size());
}

static void template_dynamic_generation(
		const size_t num_osc, 
		const unsigned int steps, 
		const connection_t type_conn,
		const pcnn_stimulus & stimulus) {

	pcnn_parameters parameters;
	pcnn network(num_osc, type_conn, parameters);

    template_dynamic_generation_runner(network, steps, type_conn, stimulus);
}

static void template_rectangle_network_dynamic_generation(
    const size_t num_osc,
    const unsigned int steps,
    const connection_t type_conn,
    const size_t height,
    const size_t width,
    const pcnn_stimulus & stimulus) {

    pcnn_parameters parameters;
    pcnn network(num_osc, type_conn, height, width, parameters);

    template_dynamic_generation_runner(network, steps, type_conn, stimulus);
}


TEST(utest_pcnn, create_delete) {
	pcnn_parameters parameters;
	pcnn * network = new pcnn(100, connection_t::CONNECTION_ALL_TO_ALL, parameters);
	
	ASSERT_EQ(100, network->size());

	delete network;
}

TEST(utest_pcnn, dynamic_generation_none_connections) {
	pcnn_stimulus stimulus { 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 }; 
	template_dynamic_generation(stimulus.size(), 20, connection_t::CONNECTION_NONE, stimulus);
}

TEST(utest_pcnn, dynamic_generation_grid_four_connections) {
	pcnn_stimulus stimulus { 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 }; 
	template_dynamic_generation(stimulus.size(), 20, connection_t::CONNECTION_GRID_FOUR, stimulus);
}

TEST(utest_pcnn, dynamic_generation_grid_four_rectangle_connections) {
    pcnn_stimulus stimulus{ 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 };
    template_rectangle_network_dynamic_generation(stimulus.size(), 20, connection_t::CONNECTION_GRID_FOUR, 2, 8, stimulus);
}

TEST(utest_pcnn, dynamic_generation_grid_eight_connections) {
	pcnn_stimulus stimulus { 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 }; 
	template_dynamic_generation(stimulus.size(), 20, connection_t::CONNECTION_GRID_EIGHT, stimulus);
}

TEST(utest_pcnn, dynamic_generation_grid_eight_rectangle_connections) {
    pcnn_stimulus stimulus{ 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 };
    template_rectangle_network_dynamic_generation(stimulus.size(), 20, connection_t::CONNECTION_GRID_EIGHT, 8, 2, stimulus);
}

TEST(utest_pcnn, dynamic_generation_bidir_list_connections) {
	pcnn_stimulus stimulus { 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 }; 
	template_dynamic_generation(stimulus.size(), 20, connection_t::CONNECTION_LIST_BIDIRECTIONAL, stimulus);
}

TEST(utest_pcnn, dynamic_generation_all_to_all_connections) {
	pcnn_stimulus stimulus { 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 }; 
	template_dynamic_generation(stimulus.size(), 20, connection_t::CONNECTION_ALL_TO_ALL, stimulus);
}

TEST(utest_pcnn, dynamic_none_connections_stimulated) {
	pcnn_stimulus stimulus { 1, 1, 1, 1, 1, 1, 1, 1, 1, 1 }; 
	template_dynamic_generation(stimulus.size(), 20, connection_t::CONNECTION_NONE, stimulus);
}

TEST(utest_pcnn, dynamic_grid_four_connections_stimulated) {
	pcnn_stimulus stimulus { 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1 }; 
	template_dynamic_generation(stimulus.size(), 20, connection_t::CONNECTION_GRID_FOUR, stimulus);
}

TEST(utest_pcnn, dynamic_grid_four_connections_rectangle_stimulated) {
    pcnn_stimulus stimulus{ 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1 };
    template_rectangle_network_dynamic_generation(stimulus.size(), 20, connection_t::CONNECTION_GRID_FOUR, 2, 8, stimulus);
}

TEST(utest_pcnn, dynamic_grid_eight_connections_stimulated) {
	pcnn_stimulus stimulus { 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1 }; 
	template_dynamic_generation(stimulus.size(), 20, connection_t::CONNECTION_GRID_EIGHT, stimulus);
}

TEST(utest_pcnn, dynamic_grid_eight_connections_rectangle_stimulated) {
    pcnn_stimulus stimulus{ 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1 };
    template_rectangle_network_dynamic_generation(stimulus.size(), 20, connection_t::CONNECTION_GRID_EIGHT, 8, 2, stimulus);
}

TEST(utest_pcnn, dynamic_bidir_list_connections_stimulated) {
	pcnn_stimulus stimulus { 1, 1, 1, 1, 1, 1, 1, 1, 1, 1 };  
	template_dynamic_generation(stimulus.size(), 20, connection_t::CONNECTION_LIST_BIDIRECTIONAL, stimulus);
}

TEST(utest_pcnn, dynamic_all_to_all_connections_stimulated) {
	pcnn_stimulus stimulus { 1, 1, 1, 1, 1, 1, 1, 1, 1, 1 }; 
	template_dynamic_generation(stimulus.size(), 20, connection_t::CONNECTION_ALL_TO_ALL, stimulus);
}

static void template_output_activity(
	const size_t num_osc,
	const unsigned int steps,
	const connection_t type_conn, 
	const pcnn_stimulus & stimulus,
	const bool activity_requirement,
	const pcnn_parameters * const params = nullptr) {

	pcnn_parameters parameters;
	if (params != nullptr) {
		parameters = *params;
	}

	pcnn network(num_osc, type_conn, parameters);

	pcnn_dynamic dynamic;
	network.simulate(steps, stimulus, dynamic);

	ensemble_data<pcnn_ensemble> sync_ensembles;
	ensemble_data<pcnn_ensemble> spike_ensembles;
	pcnn_time_signal time_signal;

	dynamic.allocate_sync_ensembles(sync_ensembles);
	dynamic.allocate_spike_ensembles(spike_ensembles);
	dynamic.allocate_time_signal(time_signal);

	ASSERT_EQ(steps, dynamic.size());

	/* check time signal for activity */
	bool output_activity = false;
	for (size_t i = 0; i < time_signal.size(); i++) {
		if (time_signal[i] > 0) {
			output_activity = true;
			break;
		}
	}

	ASSERT_EQ(activity_requirement, output_activity);

	/* if activity exists in time signal then at least one ensemble should be */
	ASSERT_EQ(activity_requirement, (sync_ensembles.size() > 0));
	ASSERT_EQ(activity_requirement, (spike_ensembles.size() > 0));
}

TEST(utest_pcnn, no_output_activity) {
	pcnn_stimulus stimulus { 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 };

	template_output_activity(stimulus.size(), 30, connection_t::CONNECTION_ALL_TO_ALL, stimulus, false);
	template_output_activity(stimulus.size(), 30, connection_t::CONNECTION_GRID_EIGHT, stimulus, false);
	template_output_activity(stimulus.size(), 30, connection_t::CONNECTION_GRID_FOUR, stimulus, false);
	template_output_activity(stimulus.size(), 30, connection_t::CONNECTION_LIST_BIDIRECTIONAL, stimulus, false);
	template_output_activity(stimulus.size(), 30, connection_t::CONNECTION_NONE, stimulus, false);
}

TEST(utest_pcnn, output_activity_full_stimulated) {
	pcnn_stimulus stimulus { 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1 };

	template_output_activity(stimulus.size(), 30, connection_t::CONNECTION_ALL_TO_ALL, stimulus, true);
	template_output_activity(stimulus.size(), 30, connection_t::CONNECTION_GRID_EIGHT, stimulus, true);
	template_output_activity(stimulus.size(), 30, connection_t::CONNECTION_GRID_FOUR, stimulus, true);
	template_output_activity(stimulus.size(), 30, connection_t::CONNECTION_LIST_BIDIRECTIONAL, stimulus, true);
	template_output_activity(stimulus.size(), 30, connection_t::CONNECTION_NONE, stimulus, true);
}

TEST(utest_pcnn, output_activity_partial_stimulated) {
	pcnn_stimulus stimulus { 1, 1, 1, 0, 0, 0, 0, 1, 1, 1, 1, 1, 0, 0, 1, 1, 0, 1, 0, 1, 1, 0, 0, 1, 0 };

	template_output_activity(stimulus.size(), 30, connection_t::CONNECTION_ALL_TO_ALL, stimulus, true);
	template_output_activity(stimulus.size(), 30, connection_t::CONNECTION_GRID_EIGHT, stimulus, true);
	template_output_activity(stimulus.size(), 30, connection_t::CONNECTION_GRID_FOUR, stimulus, true);
	template_output_activity(stimulus.size(), 30, connection_t::CONNECTION_LIST_BIDIRECTIONAL, stimulus, true);
	template_output_activity(stimulus.size(), 30, connection_t::CONNECTION_NONE, stimulus, true);
}

TEST(utest_pcnn, output_activity_one_stimulated) {
	pcnn_stimulus stimulus { 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 };

	template_output_activity(stimulus.size(), 30, connection_t::CONNECTION_ALL_TO_ALL, stimulus, true);
	template_output_activity(stimulus.size(), 30, connection_t::CONNECTION_GRID_EIGHT, stimulus, true);
	template_output_activity(stimulus.size(), 30, connection_t::CONNECTION_GRID_FOUR, stimulus, true);
	template_output_activity(stimulus.size(), 30, connection_t::CONNECTION_LIST_BIDIRECTIONAL, stimulus, true);
	template_output_activity(stimulus.size(), 30, connection_t::CONNECTION_NONE, stimulus, true);
}

static void template_ensemble_allocation(
	const size_t num_osc,
	const unsigned int steps,
	const connection_t type_conn, 
	const pcnn_stimulus & stimulus,
	const pcnn_parameters * const params = nullptr) {

	pcnn_parameters parameters;
	if (params != nullptr) {
		parameters = *params;
	}

	pcnn network(num_osc, type_conn, parameters);

	pcnn_dynamic dynamic;
	network.simulate(steps, stimulus, dynamic);

	ensemble_data<pcnn_ensemble> sync_ensembles;
	ensemble_data<pcnn_ensemble> spike_ensembles;
	pcnn_time_signal time_signal;

	dynamic.allocate_sync_ensembles(sync_ensembles);
	dynamic.allocate_spike_ensembles(spike_ensembles);
	dynamic.allocate_time_signal(time_signal);

	ASSERT_EQ(steps, dynamic.size());

	for (ensemble_data<pcnn_ensemble>::const_iterator iter = spike_ensembles.cbegin(); iter != spike_ensembles.cend(); iter++) {
		const pcnn_ensemble & ensemble = (*iter);
		ASSERT_NE(time_signal.cend(), std::find(time_signal.cbegin(), time_signal.cend(), ensemble.size()));
	}

	std::unordered_set<size_t> traverse_oscillators;

	for (ensemble_data<pcnn_ensemble>::const_iterator iter = sync_ensembles.cbegin(); iter != sync_ensembles.cend(); iter++) {
		const pcnn_ensemble & ensemble = (*iter);

		for (pcnn_ensemble::const_iterator iter_index = ensemble.cbegin(); iter_index != ensemble.cend(); iter_index++) {
			size_t index_oscillator = (*iter_index);

			ASSERT_EQ(traverse_oscillators.end(), traverse_oscillators.find(index_oscillator));
			traverse_oscillators.insert(index_oscillator);
		}
	}
}

TEST(utest_pcnn, ensemble_allocation_all_stimulated) {
	pcnn_stimulus stimulus { 1, 1, 1, 1, 1, 1, 1, 1, 1, 1 }; 
	template_ensemble_allocation(stimulus.size(), 20, connection_t::CONNECTION_ALL_TO_ALL, stimulus);
}

TEST(utest_pcnn, ensemble_allocation_partial_stimulated) {
	pcnn_stimulus stimulus { 1, 0, 0, 1, 1, 1, 0, 0, 1, 1 }; 
	template_ensemble_allocation(stimulus.size(), 20, connection_t::CONNECTION_ALL_TO_ALL, stimulus);
}

TEST(utest_pcnn, ensemble_allocation_unstimulated) {
	pcnn_stimulus stimulus { 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 };
	template_ensemble_allocation(stimulus.size(), 20, connection_t::CONNECTION_ALL_TO_ALL, stimulus);
}

TEST(utest_pcnn, ensemble_allocation_fast_linking) {
	pcnn_stimulus full_stimulus { 1, 1, 1, 1, 1, 1, 1, 1, 1, 1 }; 
	pcnn_stimulus partial_stimulus { 1, 0, 0, 1, 1, 1, 0, 0, 1, 1 };
	pcnn_stimulus no_stimulus { 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 };

	pcnn_parameters params;
	params.FAST_LINKING = true;

	template_ensemble_allocation(full_stimulus.size(), 50, connection_t::CONNECTION_ALL_TO_ALL, full_stimulus, &params);
	template_ensemble_allocation(partial_stimulus.size(), 50, connection_t::CONNECTION_ALL_TO_ALL, partial_stimulus, &params);
	template_ensemble_allocation(no_stimulus.size(), 50, connection_t::CONNECTION_ALL_TO_ALL, no_stimulus, &params);
}

#endif
