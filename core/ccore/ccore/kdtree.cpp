#include "kdtree.h"

kdnode::kdnode(std::vector<double> * p_data, void * p_payload,  kdnode * p_left, kdnode * p_right, kdnode * p_parent, unsigned int disc) :
	data(p_data), payload(p_payload), left(p_left), right(p_right), parent(p_parent), discriminator(disc)
	{ }

kdnode::~kdnode() { }


kdtree::kdtree() : root(NULL), dimension(0) { }

kdtree::kdtree(const std::vector< std::vector<double> *> * data, const std::vector<void *> * payloads) {
	root = NULL;
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
			insert((*data)[index], NULL);
		}
	}
}

kdtree::~kdtree(void) {
	/* traverse tree and remove each node */
}

kdnode * kdtree::insert(std::vector<double> * point, void * payload) {
	if (root == NULL) {
		kdnode * node = new kdnode(point, payload, NULL, NULL, NULL, 0);
		return node;
	}
	else {
		kdnode * cur_node = root;

		while(true) {
			/* If new node is greater or equal than current node then check right leaf */
			if (*cur_node <= *point) {
				if (cur_node->get_right() == NULL) {
					unsigned int discriminator = cur_node->get_discriminator() + 1;
					if (discriminator >= dimension) {
						discriminator = 0;
					}

					cur_node->set_right(new kdnode(point, payload, NULL, NULL, cur_node, discriminator));
					return cur_node->get_right();
				}
				else {
					cur_node = cur_node->get_right();
				}
			}
			/* If new node is less than current then check left leaf */
			else {
				if (cur_node->get_left() == NULL) {
					unsigned int discriminator = cur_node->get_discriminator() + 1;
					if (discriminator >= dimension) {
						discriminator = 0;
					}

					cur_node->set_left(new kdnode(point, payload, NULL, NULL, cur_node, discriminator));
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
	if (node_for_remove == NULL) {
		return;
	}

	kdnode * parent = node_for_remove->get_parent();
	kdnode * node = recursive_remove(node_for_remove);
	if (parent == NULL) {
		root = node;

		/* if tree is almost destroyed */
		if (node != NULL) {
			node->set_parent(NULL);
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
	/* Check if it's a leaf */
	if ( (node->get_right() == NULL) && (node->get_left() == NULL) ) {
		return NULL;
	}

	unsigned int discriminator = node->get_discriminator();

	/* Check if only left branch exist */
	if (node->get_right() == NULL) {
		node->set_right(node->get_left);
		node->set_left(NULL);
	}

	/* Find minimal node in line with coordinate that is defined by discriminator */
	kdnode * minimal_node = find_minimal_node(node->get_right(), discriminator);
	kdnode * parent = minimal_node->get_parent();

	if (parent->get_left() == minimal_node) {
		parent->set_left(recursive_remove(minimal_node));
	}
	else if (parent->get_right() == minimal_node) {
		parent->set_left(recursive_remove(minimal_node));
	}
	else {
		throw std::runtime_error("Structure of KD Tree is corrupted");
	}

	minimal_node->set_parent(node->get_parent());
	minimal_node->set_discriminator(node->get_discriminator());
	minimal_node->set_right(node->get_right());
	minimal_node->set_left(node->get_left());

	/* Update parent for successors of previous parent */
	if (minimal_node->get_right() != NULL) {
		minimal_node->get_right()->set_parent(minimal_node);
	}

	if (minimal_node->get_left() != NULL) {
		minimal_node->get_left()->set_parent(minimal_node);
	}

	return minimal_node;
}

kdnode * kdtree::find_minimal_node(kdnode * node, unsigned int discriminator) {
	kdnode * minimal_node = node;

	std::vector<kdnode *> * children = node->get_children();
	for (unsigned int index_children = 0; index_children < children->size(); index_children++) {
		kdnode * candidate = find_minimal_node((*children)[index_children], discriminator);

		if (candidate->get_value(discriminator) < minimal_node->get_value(discriminator)) {
			minimal_node = candidate;
		}
	}

	delete children;
	children = NULL;

	return minimal_node;
}

kdnode * kdtree::find_node(std::vector<double> * point) {
	return find_node(point, root);
}

kdnode * kdtree::find_node(std::vector<double> * point, kdnode * node) {
	kdnode * req_node = NULL;
	kdnode * cur_node = node;

	while(true) {
		if (*cur_node <= *point) {
			if (*cur_node == *point) {
				req_node = cur_node;
				break;
			}

			if (cur_node->get_right() != NULL) {
				cur_node = cur_node->get_right();
			}
			else {
				throw std::runtime_error("Structure of KD Tree is corrupted");
			}
		}
		else {
			if (cur_node->get_left() != NULL) {
				cur_node = cur_node->get_left();
			}
			else {
				throw std::runtime_error("Structure of KD Tree is corrupted");
			}
		}
	}

	return req_node;
}

/*
def find_nearest_dist_nodes(self, point, distance):
    "Return list of neighbors such as tuple (distance, node) that is located in area that is covered by distance"
    best_nodes = [];
    self.__recursive_nearest_nodes(point, distance, distance ** 2, self.__root, best_nodes);
        
    return best_nodes;
*/
