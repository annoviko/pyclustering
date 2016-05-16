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

#pragma once


#include "gtest/gtest.h"

#include "container/adjacency.hpp"

#include <algorithm>


using namespace container;


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


void template_set_weight_connection(adjacency_weight_collection & collection) {
	for (size_t i = 0; i < collection.size(); i++) {
		for (size_t j = 0; j < collection.size(); j++) {
			ASSERT_EQ(0.0, collection.get_connection_weight(i, j));
			ASSERT_EQ(false, collection.has_connection(i, j));

			const double weight = (double) i + (double) j / 10.0 + 1.0;
			collection.set_connection_weight(i, j, weight);

			ASSERT_EQ(weight, collection.get_connection_weight(i, j));
			ASSERT_EQ(true, collection.has_connection(i, j));
		}
	}
}


void template_set_default_weight_connection(adjacency_weight_collection & collection) {
	for (size_t i = 0; i < collection.size(); i++) {
		for (size_t j = 0; j < collection.size(); j++) {
			ASSERT_EQ(0.0, collection.get_connection_weight(i, j));
			ASSERT_EQ(false, collection.has_connection(i, j));

			collection.set_connection(i, j);

			ASSERT_NE(0.0, collection.get_connection_weight(i, j));
			ASSERT_EQ(true, collection.has_connection(i, j));
		}
	}
}


void template_set_negative_weight(adjacency_weight_collection & collection) {
	for (size_t i = 0; i < collection.size(); i++) {
		for (size_t j = 0; j < collection.size(); j++) {
			ASSERT_EQ(0.0, collection.get_connection_weight(i, j));
			ASSERT_EQ(false, collection.has_connection(i, j));

			collection.set_connection_weight(i, j, -1.0);

			ASSERT_EQ(-1.0, collection.get_connection_weight(i, j));
			ASSERT_EQ(true, collection.has_connection(i, j));
		}
	}
}


void template_get_neighbors_positive_negative(adjacency_weight_collection & collection) {
	for (size_t i = 0; i < collection.size(); i++) {
		for (size_t j = 0; j < collection.size(); j++) {
			if (i % 2 == 0) {
				collection.set_connection_weight(i, j, 10.0);
			}
			else {
				collection.set_connection_weight(i, j, -10.0);
			}
		}
	}

	for (size_t i = 0; i < collection.size(); i++) {
		std::vector<size_t> node_neighbors;
		collection.get_neighbors(i, node_neighbors);

		ASSERT_EQ(collection.size(), node_neighbors.size());
	}
}
