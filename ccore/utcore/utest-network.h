#ifndef _UTEST_NETWORK_
#define _UTEST_NETWORK_

#include "ccore/network.h"

#include "gtest/gtest.h"

#include <cmath>

TEST(utest_network, create_delete) {
	network * net = new network(100, conn_type::ALL_TO_ALL);
	
	ASSERT_EQ(100, net->size());

	delete net;
}

TEST(utest_network, all_to_all_connections) {
	network net(100, conn_type::ALL_TO_ALL);
	for (size_t i = 0; i < net.size(); i++) {
		for (size_t j = 0; j < net.size(); j++) {
			if (i != j) {
				ASSERT_EQ(0, net.get_connection(i, j));
			}
			else {
				ASSERT_EQ(1, net.get_connection(i, j));
			}
		}
	}
}

TEST(utest_network, none_connections) {
	 network net(100, conn_type::NONE);

	 for (size_t i = 0; i < net.size(); i++) {
		for (size_t j = 0; j < net.size(); j++) {
			ASSERT_EQ(0, net.get_connection(i, j));
		}
	}
}

static void template_grid_four_connections(unsigned int number_oscillators) {
	network net(number_oscillators, conn_type::GRID_FOUR);
	int base = std::sqrt(number_oscillators);
	
	for (int index = 0; index < net.size(); index++) {
		int upper_index = index - base;
		int lower_index = index + base;
		int left_index = index - 1;
		int right_index = index + 1;

		int node_row_index = std::ceil(index / base);
		bool node_neighbour = false;

		if (upper_index >= 0) {
			node_neighbour = true;
			ASSERT_EQ(1, net.get_connection(index, upper_index));
		}

		if (lower_index < net.size()) {
			node_neighbour = true;
			ASSERT_EQ(1, net.get_connection(index, lower_index));
		}

		if ( (left_index >= 0) && (std::ceil(left_index / base) == node_row_index) ) {
			node_neighbour = true;
			ASSERT_EQ(1, net.get_connection(index, left_index));
		}

		if ( (right_index < net.size()) && (std::ceil(right_index / base) == node_row_index) ) {
			node_neighbour = true;
			ASSERT_EQ(1, net.get_connection(index, right_index));
		}

		for (unsigned int j = 0; j < net.size(); j++) {
			if ( (j != index) && (j != upper_index) && (j != lower_index) && (j != left_index) && (j != right_index) ) {
				ASSERT_EQ(0, net.get_connection(index, j));
			}
		}
	}
}

TEST(utest_network, grid_four_connections_25) {
	template_grid_four_connections(25);
}

TEST(utest_network, grid_four_connections_81) {
	template_grid_four_connections(81);
}

TEST(utest_network, grid_four_connections_625) {
	template_grid_four_connections(81);
}

TEST(utest_network, grid_four_bit_representation) {
	unsigned int maximum_matrix_repr_base = std::ceil(std::sqrt(MAXIMUM_OSCILLATORS_MATRIX_REPRESENTATION));
	unsigned int number_oscillators = std::pow(maximum_matrix_repr_base, 2);
	template_grid_four_connections(number_oscillators);
}

#endif