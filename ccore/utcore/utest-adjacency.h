#pragma once

#include "ccore/adjacency.h"

#include "gtest/gtest.h"

#include <algorithm>


void template_set_connection(adjacency_collection & collection) {
	for (size_t i = 0; i < collection.size(); i++) {
		for (size_t j = i + 1; j < collection.size(); j++) {
			ASSERT_EQ(false, collection.has_connection(i, j));

			collection.set_connection(i, j);

			ASSERT_EQ(true, collection.has_connection(i, j));
			ASSERT_EQ(false, collection.has_connection(j, i));

			collection.set_connection(j, i);

			ASSERT_EQ(true, collection.has_connection(j, i));
		}
	}
}


void template_has_no_connection(adjacency_collection & collection) {
	for (size_t i = 0; i < collection.size(); i++) {
		for (size_t j = 0; j < collection.size(); j++) {
			ASSERT_EQ(false, collection.has_connection(i, j));
		}
	}
}


void template_has_all_connection(adjacency_collection & collection) {
	for (size_t i = 0; i < collection.size(); i++) {
		for (size_t j = 0; j < collection.size(); j++) {
			collection.set_connection(i, j);
		}
	}

	for (size_t i = 0; i < collection.size(); i++) {
		for (size_t j = 0; j < collection.size(); j++) {
			ASSERT_EQ(true, collection.has_connection(i, j));
		}
	}
}


void template_erase_connection(adjacency_collection & collection) {
	for (size_t i = 0; i < collection.size(); i++) {
		for (size_t j = i + 1; j < collection.size(); j++) {
			collection.set_connection(i, j);
			collection.set_connection(j, i);
		}
	}

	for (size_t i = 0; i < collection.size(); i++) {
		for (size_t j = i + 1; j < collection.size(); j++) {
			ASSERT_EQ(true, collection.has_connection(i, j));
			ASSERT_EQ(true, collection.has_connection(j, i));

			collection.erase_connection(i, j);

			ASSERT_EQ(false, collection.has_connection(i, j));
			ASSERT_EQ(true, collection.has_connection(j, i));

			collection.erase_connection(j, i);

			ASSERT_EQ(false, collection.has_connection(i, j));
			ASSERT_EQ(false, collection.has_connection(j, i));
		}
	}
}


void template_get_neighbors_sizes(adjacency_collection & collection) {
	std::vector<size_t> node_neighbors;

	for (size_t i = 0; i < collection.size(); i++) {
		for (size_t j = i + 1; j < collection.size(); j++) {
			collection.set_connection(i, j);
			collection.set_connection(j, i);

			collection.get_neighbors(i, node_neighbors);
			ASSERT_EQ(j, node_neighbors.size());

			collection.get_neighbors(j, node_neighbors);
			ASSERT_EQ(i + 1, node_neighbors.size());
		}
	}
}


void template_get_neighbors_indexes(adjacency_collection & collection) {
	std::vector<size_t> node_neighbors;

	for (size_t i = 0; i < collection.size(); i++) {
		for (size_t j = i + 1; j < collection.size(); j++) {
			collection.set_connection(i, j);
			collection.set_connection(j, i);
		}
	}

	for (size_t i = 0; i < collection.size(); i++) {
		collection.get_neighbors(i, node_neighbors);
		ASSERT_EQ(collection.size() - 1, node_neighbors.size());

		std::vector<bool> index_neighbor_checker(collection.size(), false);
		for (size_t j = 0; j < node_neighbors.size(); j++) {
			size_t neighbor_index = node_neighbors[j];
			index_neighbor_checker[neighbor_index] = true;
		}

		for (size_t j = 0; j < node_neighbors.size(); j++) {
			if (i != j) {
				ASSERT_EQ(true, index_neighbor_checker[j]);
			}
			else {
				ASSERT_EQ(false, index_neighbor_checker[i]);
			}
		}
	}
}


void template_no_get_neighbors(adjacency_collection & collection) {
	std::vector<size_t> node_neighbors;

	for (size_t i = 0; i < collection.size(); i++) {
		collection.get_neighbors(i, node_neighbors);
		ASSERT_EQ(0, node_neighbors.size());
	}
}


void template_all_get_neighbors(adjacency_collection & collection) {
	std::vector<size_t> node_neighbors;

	for (size_t i = 0; i < collection.size(); i++) {
		for (size_t j = 0; j < collection.size(); j++) {
			collection.set_connection(i, j);
		}
	}

	for (size_t i = 0; i < collection.size(); i++) {
		for (size_t j = 0; j < collection.size(); j++) {
			collection.get_neighbors(i, node_neighbors);
			ASSERT_EQ(collection.size(), node_neighbors.size());

			std::sort(node_neighbors.begin(), node_neighbors.end());
			for (size_t index = 0; index < collection.size(); index++) {
				ASSERT_EQ(index, node_neighbors[index]);
			}
		}
	}
}


void template_get_neighbors_after_erase(adjacency_collection & collection) {
	/* full insert */
	for (size_t i = 0; i < collection.size(); i++) {
		for (size_t j = 0; j < collection.size(); j++) {
			collection.set_connection(i, j);
		}
	}

	/* full erase */
	for (size_t i = 0; i < collection.size(); i++) {
		for (size_t j = 0; j < collection.size(); j++) {
			collection.erase_connection(i, j);
		}
	}

	/* check that there is no neighbors */
	for (size_t i = 0; i < collection.size(); i++) {
		std::vector<size_t> node_neighbors;
		collection.get_neighbors(i, node_neighbors);

		ASSERT_EQ(0, node_neighbors.size());
	}
}