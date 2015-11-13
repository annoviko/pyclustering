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

TEST(utest_network, create_four_grid_correct) {
    network network_grid_structure_10_10(100, conn_type::GRID_FOUR, 10, 10);
    network network_grid_structure_5_20(100, conn_type::GRID_FOUR, 5, 20);
    network network_grid_structure_1_100(100, conn_type::GRID_FOUR, 1, 100);

    network network_grid_structure_3_5(15, conn_type::GRID_FOUR, 3, 5);
    network network_grid_structure_5_3(15, conn_type::GRID_FOUR, 5, 3);
    network network_grid_structure_15_1(15, conn_type::GRID_FOUR, 15, 1);
    network network_grid_structure_1_15(15, conn_type::GRID_FOUR, 1, 15);
}

TEST(utest_network, create_four_grid_incorrect) {
    ASSERT_ANY_THROW(network network_grid_structure(100, conn_type::GRID_FOUR, 0, 0));
    ASSERT_ANY_THROW(network network_grid_structure(100, conn_type::GRID_FOUR, 6, 20));
    ASSERT_ANY_THROW(network network_grid_structure(100, conn_type::GRID_FOUR, 0, 1000));
    ASSERT_ANY_THROW(network network_grid_structure(100, conn_type::GRID_FOUR, 15, 2));
}

TEST(utest_network, create_eight_grid_correct) {
    network network_eight_structure_10_10(100, conn_type::GRID_EIGHT, 10, 10);
    network network_eight_structure_5_20(100, conn_type::GRID_EIGHT, 5, 20);
    network network_eight_structure_1_100(100, conn_type::GRID_EIGHT, 1, 100);

    network network_eight_structure_3_5(15, conn_type::GRID_EIGHT, 3, 5);
    network network_eight_structure_5_3(15, conn_type::GRID_EIGHT, 5, 3);
    network network_eight_structure_15_1(15, conn_type::GRID_EIGHT, 15, 1);
    network network_eight_structure_1_15(15, conn_type::GRID_EIGHT, 1, 15);
}

TEST(utest_network, create_four_eight_incorrect) {
    ASSERT_ANY_THROW(network network_eight_structure(100, conn_type::GRID_EIGHT, 0, 0));
    ASSERT_ANY_THROW(network network_eight_structure(100, conn_type::GRID_EIGHT, 6, 20));
    ASSERT_ANY_THROW(network network_eight_structure(100, conn_type::GRID_EIGHT, 0, 1000));
    ASSERT_ANY_THROW(network network_eight_structure(100, conn_type::GRID_EIGHT, 15, 2));
}

TEST(utest_network, create_various_connections_with_incorrect_height_width) {
    network network_all_to_all_structure(100, conn_type::ALL_TO_ALL, 1, 10);
    network network_dynamic_structure(100, conn_type::DYNAMIC, 0, 3);
    network network_list_bidir_structure(100, conn_type::LIST_BIDIR, 7, 9);
    network network_none_structure(100, conn_type::NONE, 1, 3);
}

TEST(utest_network, all_to_all_connections) {
	network net(100, conn_type::ALL_TO_ALL);
	for (size_t i = 0; i < net.size(); i++) {
		for (size_t j = 0; j < net.size(); j++) {
			if (i == j) {
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

static void template_grid_connections(const network & net, const unsigned int number_oscillators, const conn_type connections) {
	int base = net.width();
	
	for (int index = 0; index < net.size(); index++) {
		const int upper_index = index - base;
        const int upper_left_index = index - base - 1;
        const int upper_right_index = index - base + 1;
            
        const int lower_index = index + base;
        const int lower_left_index = index + base - 1;
        const int lower_right_index = index + base + 1;
            
        const int left_index = index - 1;
        const int right_index = index + 1;
            
        const int node_row_index = std::ceil(index / base);
        const int upper_row_index = node_row_index - 1;
        const int lower_row_index = node_row_index + 1;

		std::vector<size_t> neighbors;
		net.get_neighbors(index, neighbors);

		if (upper_index >= 0) {
			ASSERT_EQ(1, net.get_connection(index, upper_index));
			ASSERT_TRUE(neighbors.cend() != std::find(neighbors.cbegin(), neighbors.cend(), upper_index));
		}

		if (lower_index < net.size()) {
			ASSERT_EQ(1, net.get_connection(index, lower_index));
			ASSERT_TRUE(neighbors.cend() != std::find(neighbors.cbegin(), neighbors.cend(), lower_index));
		}

		if ( (left_index >= 0) && (std::ceil(left_index / base) == node_row_index) ) {
			ASSERT_EQ(1, net.get_connection(index, left_index));
			ASSERT_TRUE(neighbors.cend() != std::find(neighbors.cbegin(), neighbors.cend(), left_index));
		}

		if ( (right_index < net.size()) && (std::ceil(right_index / base) == node_row_index) ) {
			ASSERT_EQ(1, net.get_connection(index, right_index));
			ASSERT_TRUE(neighbors.cend() != std::find(neighbors.cbegin(), neighbors.cend(), right_index));
		}

		if (connections == conn_type::GRID_EIGHT) {
			if ( (upper_left_index >= 0) && (std::floor(upper_left_index / base) == upper_row_index) ) {
				ASSERT_EQ(1, net.get_connection(index, upper_left_index));
				ASSERT_TRUE(neighbors.cend() != std::find(neighbors.cbegin(), neighbors.cend(), upper_left_index));
			}

			if ( (upper_right_index >= 0) && (std::floor(upper_right_index / base) == upper_row_index) ) {
				ASSERT_EQ(1, net.get_connection(index, upper_right_index));
				ASSERT_TRUE(neighbors.cend() != std::find(neighbors.cbegin(), neighbors.cend(), upper_right_index));
			}

			if ( (lower_left_index < net.size()) && (std::floor(lower_left_index / base) == lower_row_index) ) {
				ASSERT_EQ(1, net.get_connection(index, lower_left_index));
				ASSERT_TRUE(neighbors.cend() != std::find(neighbors.cbegin(), neighbors.cend(), lower_left_index));
			}

			if ( (lower_right_index < net.size()) && (std::floor(lower_right_index / base) == lower_row_index) ) {
				ASSERT_EQ(1, net.get_connection(index, lower_right_index));
				ASSERT_TRUE(neighbors.cend() != std::find(neighbors.cbegin(), neighbors.cend(), lower_right_index));
			}

			for (unsigned int j = 0; j < net.size(); j++) {
				if ( (j != index) && 
					 (j != upper_index) && (j != lower_index) && (j != left_index) && (j != right_index) &&
					 (j != upper_left_index) && (j != upper_right_index) && (j != lower_left_index) && (j != lower_right_index) ) {

					ASSERT_EQ(0, net.get_connection(index, j));
					ASSERT_TRUE(neighbors.cend() == std::find(neighbors.cbegin(), neighbors.cend(), j));
				}
			}
		}
		else {
			for (unsigned int j = 0; j < net.size(); j++) {
				if ( (j != index) && (j != upper_index) && (j != lower_index) && (j != left_index) && (j != right_index) ) {
					ASSERT_EQ(0, net.get_connection(index, j));
					ASSERT_TRUE(neighbors.cend() == std::find(neighbors.cbegin(), neighbors.cend(), j));
				}
			}			
		}
	}
}

static void template_grid_four_connections(unsigned int number_oscillators) {
    network net(number_oscillators, conn_type::GRID_FOUR);
    template_grid_connections(net, number_oscillators, conn_type::GRID_FOUR);
}

static void template_grid_eight_connections(unsigned int number_oscillators) {
    network net(number_oscillators, conn_type::GRID_EIGHT);
	template_grid_connections(net, number_oscillators, conn_type::GRID_EIGHT);
}

static void template_grid_four_rectange_connections(unsigned int number_oscillators, size_t height, size_t width) {
    network net(number_oscillators, conn_type::GRID_FOUR, height, width);
    template_grid_connections(net, number_oscillators, conn_type::GRID_FOUR);
}

static void template_grid_eight_rectange_connections(unsigned int number_oscillators, size_t height, size_t width) {
    network net(number_oscillators, conn_type::GRID_EIGHT, height, width);
    template_grid_connections(net, number_oscillators, conn_type::GRID_EIGHT);
}

TEST(utest_network, grid_four_connections_25) {
	template_grid_four_connections(25);
}

TEST(utest_network, grid_four_connections_81) {
	template_grid_four_connections(81);
}

TEST(utest_network, grid_four_connections_100) {
	template_grid_four_connections(100);
}

TEST(utest_network, grid_eight_connections_25) {
	template_grid_eight_connections(25);
}

TEST(utest_network, grid_eight_connections_81) {
	template_grid_eight_connections(81);
}

TEST(utest_network, grid_eight_connections_100) {
	template_grid_eight_connections(100);
}

TEST(utest_network, grid_four_rectangle_connections_25) {
    template_grid_four_rectange_connections(25, 5, 5);
}

TEST(utest_network, grid_four_rectangle_connections_80) {
    template_grid_four_rectange_connections(80, 20, 4);
    template_grid_four_rectange_connections(80, 4, 20);
}

TEST(utest_network, grid_four_rectangle_connections_100) {
    template_grid_four_rectange_connections(100, 10, 10);
    template_grid_four_rectange_connections(100, 25, 4);
    template_grid_four_rectange_connections(100, 1, 100);
}

TEST(utest_network, grid_eight_rectangle_connections_25) {
    template_grid_eight_rectange_connections(25, 5, 5);
}

TEST(utest_network, grid_eight_rectangle_connections_80) {
    template_grid_eight_rectange_connections(80, 20, 4);
    template_grid_eight_rectange_connections(80, 4, 20);
}

TEST(utest_network, grid_eight_rectangle_connections_100) {
    template_grid_eight_rectange_connections(100, 10, 10);
    template_grid_eight_rectange_connections(100, 25, 4);
    template_grid_eight_rectange_connections(100, 1, 100);
}

TEST(utest_network, bidir_connections) {
	const unsigned int number_oscillators = 100;
	network net(number_oscillators, conn_type::LIST_BIDIR);

	for (size_t i = 0; i < number_oscillators; i++) {
		std::vector<size_t> neighbors;
		net.get_neighbors(i, neighbors);

		if (i > 0) {
			ASSERT_EQ(1, net.get_connection(i, i - 1));
			ASSERT_EQ(1, net.get_connection(i - 1, i));

			ASSERT_TRUE(neighbors.cend() != std::find(neighbors.cbegin(), neighbors.cend(), i - 1));
		}

		if (i < (number_oscillators - 1)) {
			ASSERT_EQ(1, net.get_connection(i, i + 1));
			ASSERT_EQ(1, net.get_connection(i + 1, i));

			ASSERT_TRUE(neighbors.cend() != std::find(neighbors.cbegin(), neighbors.cend(), i + 1));
		}

		for (unsigned int j = 0; j < number_oscillators; j++) {
			if ( (i != j) && (j != (i + 1)) && (j != (i - 1)) ) {
				ASSERT_EQ(0, net.get_connection(i, j));
				ASSERT_TRUE(neighbors.cend() == std::find(neighbors.cbegin(), neighbors.cend(), j));
			}
		}
	}
}

#endif
