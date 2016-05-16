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

#include "container/kdtree.hpp"

#include "utils.hpp"


namespace container {

kdnode::kdnode(std::vector<double> * p_data, void * p_payload,  kdnode * p_left, kdnode * p_right, kdnode * p_parent, unsigned int disc) :
	data(p_data), payload(p_payload), left(p_left), right(p_right), parent(p_parent), discriminator(disc)
	{ }


kdnode::~kdnode() { }


kdtree::kdtree() : root(nullptr), dimension(0) { }


kdtree::kdtree(const std::vector< std::vector<double> *> * data, const std::vector<void *> * payloads) {
	root = nullptr;
	dimension = (*(*data)[0]).size();

	if (payloads) {
		if (data->size() != payloads->size()) {
			throw std::runtime_error("Number of points should be equal to number of according payloads");
		}

		for (unsigned int index = 0; index < data->size(); index++) {
			insert((*data)[index], (*payloads)[index]);
		}
	}
	else {
		for (unsigned int index = 0; index < data->size(); index++) {
			insert((*data)[index], nullptr);
		}
	}
}


kdtree::~kdtree(void) {
	if (root != nullptr) {
		recursive_destroy(root);
	}
}


void kdtree::recursive_destroy(kdnode * node) {
	if (node->get_right() != nullptr) {
		recursive_destroy(node->get_right());
	}
	
	if (node->get_left() != nullptr) {
		recursive_destroy(node->get_left());
	}

	delete node;
	node = nullptr;
}


kdnode * kdtree::insert(std::vector<double> * point, void * payload) {
	if (root == nullptr) {
		kdnode * node = new kdnode(point, payload, nullptr, nullptr, nullptr, 0);

		root = node;
		dimension = node->get_data()->size();

		return node;
	}
	else {
		kdnode * cur_node = root;

		while(true) {
			/* If new node is greater or equal than current node then check right leaf */
			if (*cur_node <= *point) {
				if (cur_node->get_right() == nullptr) {
					unsigned int discriminator = cur_node->get_discriminator() + 1;
					if (discriminator >= dimension) {
						discriminator = 0;
					}

					cur_node->set_right(new kdnode(point, payload, nullptr, nullptr, cur_node, discriminator));
					return cur_node->get_right();
				}
				else {
					cur_node = cur_node->get_right();
				}
			}
			/* If new node is less than current then check left leaf */
			else {
				if (cur_node->get_left() == nullptr) {
					unsigned int discriminator = cur_node->get_discriminator() + 1;
					if (discriminator >= dimension) {
						discriminator = 0;
					}

					cur_node->set_left(new kdnode(point, payload, nullptr, nullptr, cur_node, discriminator));
					return cur_node->get_left();
				}
				else {
					cur_node = cur_node->get_left();
				}
			}
		}
	}
}


void kdtree::remove(std::vector<double> * point) {
	kdnode * node_for_remove = find_node(point);
	if (node_for_remove == nullptr) {
		return;
	}

	remove(node_for_remove);

	delete node_for_remove;
	node_for_remove = nullptr;
}


void kdtree::remove(kdnode * node_for_remove) {
	kdnode * parent = node_for_remove->get_parent();
	kdnode * node = recursive_remove(node_for_remove);

	if (parent == nullptr) {
		root = node;

		/* if tree is almost destroyed */
		if (node != nullptr) {
			node->set_parent(nullptr);
		}
	}
	else {
		if (parent->get_left() == node_for_remove) {
			parent->set_left(node);
		}
		else if (parent->get_right() == node_for_remove) {
			parent->set_right(node);
		}
		else {
			throw std::runtime_error("Structure of KD Tree is corrupted");
		}
	}
}


kdnode * kdtree::recursive_remove(kdnode * node) {
	if ( (node->get_right() == nullptr) && (node->get_left() == nullptr) ) {
		return nullptr;
	}

	unsigned int discriminator = node->get_discriminator();

	/* Check if only left branch exist */
	if (node->get_right() == nullptr) {
		node->set_right(node->get_left());
		node->set_left(nullptr);
	}

	/* Find minimal node in line with coordinate that is defined by discriminator */
	kdnode * minimal_node = find_minimal_node(node->get_right(), discriminator);
	kdnode * parent = minimal_node->get_parent();

	if (parent->get_left() == minimal_node) {
		parent->set_left(recursive_remove(minimal_node));
	}
	else if (parent->get_right() == minimal_node) {
		parent->set_right(recursive_remove(minimal_node));
	}
	else {
		throw std::runtime_error("Structure of KD Tree is corrupted");
	}

	minimal_node->set_parent(node->get_parent());
	minimal_node->set_discriminator(node->get_discriminator());
	minimal_node->set_right(node->get_right());
	minimal_node->set_left(node->get_left());

	/* Update parent for successors of previous parent */
	if (minimal_node->get_right() != nullptr) {
		minimal_node->get_right()->set_parent(minimal_node);
	}

	if (minimal_node->get_left() != nullptr) {
		minimal_node->get_left()->set_parent(minimal_node);
	}

	return minimal_node;
}


kdnode * kdtree::find_minimal_node(kdnode * node, unsigned int discriminator) {

	std::stack <kdnode *> stack;
	kdnode * minimal_node = node;
	std::vector<kdnode *> candidates;
	bool is_done = false;

	while (!is_done) {
		if (node != nullptr) {
			stack.push(node);
			node = node->get_left();
		}
		else {
			if (stack.size() != 0) {
				node = stack.top();
				candidates.push_back(node);
				stack.pop();
				node = node->get_right();
			}
			else {
				is_done = true;
			}
		}
	}

	for (size_t i = 0; i < candidates.size(); i++) {
		if (candidates[i]->get_value(discriminator) <= minimal_node->get_value(discriminator)) {
			minimal_node = candidates[i];
		}
	}

	return minimal_node;
}


kdnode * kdtree::find_node(std::vector<double> * point) {
	return find_node(point, root);
}


kdnode * kdtree::find_node(std::vector<double> * point, kdnode * node) {
	kdnode * req_node = nullptr;
	kdnode * cur_node = node;

	if (node == nullptr) { return nullptr; }

	while(true) {
		if (*cur_node <= *point) {
			if (cur_node->get_data() == point) {
				req_node = cur_node;
				break;
			}

			if (cur_node->get_right() != nullptr) {
				cur_node = cur_node->get_right();
			}
			else {
				return nullptr;
			}
		}
		else {
			if (cur_node->get_left() != nullptr) {
				cur_node = cur_node->get_left();
			}
			else {
				return nullptr;
			}
		}
	}

	return req_node;
}


unsigned int kdtree::traverse(kdnode * node) {
	unsigned int number_nodes = 0;

	if (node != nullptr) {
		if (node->get_left() != nullptr) {
			number_nodes += traverse(node->get_left());
		}

		if (node->get_right() != nullptr) {
			number_nodes += traverse(node->get_right());
		}

		number_nodes++;
	}

	return number_nodes;
}


kdtree_searcher::kdtree_searcher() : distance(0), sqrt_distance(0), initial_node(nullptr), search_point(nullptr) { }


kdtree_searcher::~kdtree_searcher() {
	if (nodes_distance != nullptr) {
		delete nodes_distance;
		nodes_distance = nullptr;
	}

	if (nearest_nodes != nullptr) {
		delete nearest_nodes;
		nearest_nodes = nullptr;
	}
}


kdtree_searcher::kdtree_searcher(std::vector<double> * point, kdnode * node, const double radius_search) {
	initialize(point, node, radius_search);
}


void kdtree_searcher::initialize(std::vector<double> * point, kdnode * node, const double radius_search) {
	distance = radius_search;
	sqrt_distance = radius_search * radius_search;

	initial_node = node;
	search_point = point;
}


void kdtree_searcher::prepare_storages() {
	if (nodes_distance == nullptr) {
		nodes_distance = new std::vector<double>();
	}

	nearest_nodes = new std::vector<kdnode *>();
}


void kdtree_searcher::recursive_nearest_nodes(kdnode * node) {
	double minimum = node->get_value() - distance;
	double maximum = node->get_value() + distance;

	if (node->get_right() != nullptr) {
		if ((*search_point)[node->get_discriminator()] >= minimum) {
			recursive_nearest_nodes(node->get_right());
		}
	}

	if (node->get_left() != nullptr) {
		if ((*search_point)[node->get_discriminator()] < maximum) {
			recursive_nearest_nodes(node->get_left());
		}
	}

	double candidate_distance = euclidean_distance_sqrt(search_point, node->get_data());
	if (candidate_distance <= sqrt_distance) {
		nearest_nodes->push_back(node);
		nodes_distance->push_back(candidate_distance);
	}
}


std::vector<kdnode *> * kdtree_searcher::find_nearest_nodes(std::vector<double> * distances) {
	if (distances != nullptr) {
		nodes_distance = distances;
	}

	prepare_storages();

	std::vector<kdnode *> * result = nearest_nodes;

	recursive_nearest_nodes(initial_node);

	nearest_nodes = nullptr; /* application responds for the vector */

	if (distances != nullptr) {
		distances = nodes_distance; /* application responds for the vector */
		nodes_distance = nullptr;
	}
	else {
		delete nodes_distance;
		nodes_distance = nullptr;
	}

	return result;
}


kdnode * kdtree_searcher::find_nearest_node() {
	prepare_storages();

	kdnode * node = nullptr;

	recursive_nearest_nodes(initial_node);

	if (nodes_distance->size() > 0) {
		double minimal_distance = (*nodes_distance)[0];
		for (unsigned int index = 1; index < nodes_distance->size(); index++) {
			if ((*nodes_distance)[index] < minimal_distance) {
				minimal_distance = (*nodes_distance)[index];
				node = (*nearest_nodes)[index];
			}
		}
	}

	delete nearest_nodes;
	nearest_nodes = nullptr;

	delete nodes_distance;
	nodes_distance = nullptr;

	return node;
}

}
