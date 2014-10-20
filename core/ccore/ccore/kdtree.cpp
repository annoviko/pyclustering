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
			throw std::runtime_error("KD Tree is corrupted");
		}
	}
}