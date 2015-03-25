#ifndef _UTEST_PCNN_
#define _UTEST_PCNN_

#include "ccore/pcnn.h"
#include "ccore/network.h"

#include "gtest/gtest.h"

static void template_dynamic_generation(
		const unsigned int num_osc, 
		const unsigned int steps, 
		const conn_type type_conn, 
		const std::vector<double> & stimulus) {

	pcnn_parameters parameters;
	pcnn network(num_osc, type_conn, parameters);
	pcnn_dynamic * dynamic = network.simulate(steps, stimulus);

	ASSERT_EQ(steps, dynamic->size());
	
	std::vector<unsigned int> * time_signal = dynamic->allocate_time_signal();

	ASSERT_EQ(steps, time_signal->size());

	delete dynamic;
	delete time_signal;
}

TEST(utest_pcnn, create_delete) {
	pcnn_parameters parameters;
	pcnn * network = new pcnn(100, conn_type::ALL_TO_ALL, parameters);
	
	ASSERT_EQ(100, network->size());

	delete network;
}

TEST(utest_pcnn, dynamic_generation_none_connections) {
	std::vector<double> stimulus { 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 }; 
	template_dynamic_generation(stimulus.size(), 20, conn_type::NONE, stimulus);
}

TEST(utest_pcnn, dynamic_generation_grid_four_connections) {
	std::vector<double> stimulus { 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 }; 
	template_dynamic_generation(stimulus.size(), 20, conn_type::GRID_FOUR, stimulus);
}

TEST(utest_pcnn, dynamic_generation_grid_eight_connections) {
	std::vector<double> stimulus { 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 }; 
	template_dynamic_generation(stimulus.size(), 20, conn_type::GRID_EIGHT, stimulus);
}

TEST(utest_pcnn, dynamic_generation_bidir_list_connections) {
	std::vector<double> stimulus { 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 }; 
	template_dynamic_generation(stimulus.size(), 20, conn_type::LIST_BIDIR, stimulus);
}

TEST(utest_pcnn, dynamic_generation_all_to_all_connections) {
	std::vector<double> stimulus { 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 }; 
	template_dynamic_generation(stimulus.size(), 20, conn_type::ALL_TO_ALL, stimulus);
}



#endif