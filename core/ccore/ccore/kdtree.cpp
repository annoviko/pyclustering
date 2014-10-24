#include "kdtree.h"
#include "support.h"

kdnode::kdnode(std::vector<double> * p_data, void * p_payload,  kdnode * p_left, kdnode * p_right, kdnode * p_parent, unsigned int disc) :
	data(p_data), payload(p_payload), left(p_left), right(p_right), parent(p_parent), discriminator(disc)
	{ }

kdnode::~kdnode() { }


/***********************************************************************************************
*
* @brief   Default constructor.
*
***********************************************************************************************/
kdtree::kdtree() : root(NULL), dimension(0) { }

/***********************************************************************************************
*
* @brief   Constructor of kd tree with pre-defined information.
*
* @param   data               - coordinates that describe nodes in tree.
* @param   payloads           - payloads of nodes (can be NULL if it's not required).
*
***********************************************************************************************/
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

/***********************************************************************************************
*
* @brief   Default destructor.
*
***********************************************************************************************/
kdtree::~kdtree(void) {
	/* traverse tree and remove each node */
}

/***********************************************************************************************
*
* @brief   Insert new node in the tree.
*
* @param   point              - coordinates that describe node in tree.
* @param   payload            - payloads of node (can be NULL if it's not required).
*
* @return  Pointer to added node in the tree.
*
***********************************************************************************************/
kdnode * kdtree::insert(std::vector<double> * point, void * payload) {
	if (root == NULL) {
		kdnode * node = new kdnode(point, payload, NULL, NULL, NULL, 0);
		root = node;
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

/***********************************************************************************************
*
* @brief   Remove point with specified coordinates.
*
* @param   point              - coordinates that describe node in tree.
*
***********************************************************************************************/
void kdtree::remove(std::vector<double> * point) {
	kdnode * node_for_remove = find_node(point);
	if (node_for_remove == NULL) {
		return;
	}

	remove(node_for_remove);
}

/***********************************************************************************************
*
* @brief   Remove node from the tree.
*
* @param   node_for_remove    - pointer to node that is located in tree.
*
***********************************************************************************************/
void kdtree::remove(kdnode * node_for_remove) {
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

/***********************************************************************************************
*
* @brief   Recursive remove of node in tree.
*
* @param   node            - node that should be removed.
*
* @return  Node that should replace removed node (if it's not leaf).
*
***********************************************************************************************/
kdnode * kdtree::recursive_remove(kdnode * node) {
	/* Check if it's a leaf */
	if ( (node->get_right() == NULL) && (node->get_left() == NULL) ) {
		return NULL;
	}

	unsigned int discriminator = node->get_discriminator();

	/* Check if only left branch exist */
	if (node->get_right() == NULL) {
		node->set_right(node->get_left());
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

/***********************************************************************************************
*
* @brief   Find minimal node in subtree in line with specified discriminator.
*
* @param   node            - root of subtree where searching should be performed.
* @param   discriminator   - discriminator that is used for comparison of nodes.
*
* @return  Return the smallest node in specified subtree in line with discriminator.
*
***********************************************************************************************/
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

/***********************************************************************************************
*
* @brief   Find node in tree using coordinates.
*
* @param   point              - coordinates of searched node.
*
* @return  Pointer to found node in tree.
*
***********************************************************************************************/
kdnode * kdtree::find_node(std::vector<double> * point) {
	return find_node(point, root);
}

/***********************************************************************************************
*
* @brief   Find node in tree using coordinates in subtree.
*
* @param   point              - coordinates of searched node.
* @param   cur_node           - root of subtree.
*
* @return  Pointer to found node in tree.
*
***********************************************************************************************/
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


/***********************************************************************************************
*
* @brief   Default constructor. Search will not be performed until it's initialized.
*
***********************************************************************************************/
kdtree_searcher::kdtree_searcher() : distance(0), sqrt_distance(0), initial_node(NULL), search_point(NULL) { }

/***********************************************************************************************
*
* @brief   Default destructor.
*
***********************************************************************************************/
kdtree_searcher::~kdtree_searcher() {
	if (nodes_distance != NULL) {
		delete nodes_distance;
		nodes_distance = NULL;
	}

	if (nearest_nodes != NULL) {
		delete nearest_nodes;
		nearest_nodes = NULL;
	}
}

/***********************************************************************************************
*
* @brief   Constructor of searcher with request for searching.
*
* @param   (in) point              - point for which nearest nodes should be found.
* @param   (in) node               - initial node in tree from which searching should started.
* @param   (in) radius_search      - allowable distance for searching from the point.
*
***********************************************************************************************/
kdtree_searcher::kdtree_searcher(std::vector<double> * point, kdnode * node, const double radius_search) {
	initialize(point, node, radius_search);
}

/***********************************************************************************************
*
* @brief   Initialization of new request for searching.
*
* @param   (in) point              - point for which nearest nodes should be found.
* @param   (in) node               - initial node in tree from which searching should started.
* @param   (in) radius_search      - allowable distance for searching from the point.
*
***********************************************************************************************/
void kdtree_searcher::initialize(std::vector<double> * point, kdnode * node, const double radius_search) {
	distance = radius_search;
	sqrt_distance = radius_search * radius_search;

	initial_node = node;
	search_point = point;
}

/***********************************************************************************************
*
* @brief   Prepare storages that are required for searching.
*
***********************************************************************************************/
void kdtree_searcher::prepare_storages() {
	nodes_distance = new std::vector<double>();
	nearest_nodes = new std::vector<kdnode *>();
}

/***********************************************************************************************
*
* @brief   Recursive method for searching nodes that satisfy the request.
*
* @param   node               - initial node in tree from which searching should performed.
*
***********************************************************************************************/
void kdtree_searcher::recursive_nearest_nodes(kdnode * node) {
	double minimum = node->get_value() - distance;
	double maximum = node->get_value() + distance;

	if (node->get_right() != NULL) {
		if ((*search_point)[node->get_discriminator()] >= minimum) {
			recursive_nearest_nodes(node->get_right());
		}
	}

	if (node->get_left() != NULL) {
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

/***********************************************************************************************
*
* @brief   Search nodes that are located in specified distance from specified point.
*
* @return  Return vector of found nodes in kd tree that satisfy the request.
*
***********************************************************************************************/
std::vector<kdnode *> * kdtree_searcher::find_nearest_nodes(std::vector<double> * distances) {
	prepare_storages();

	std::vector<kdnode *> * result = nearest_nodes;

	recursive_nearest_nodes(initial_node);

	nearest_nodes = NULL; /* application responds for the vector */

	if (distances != NULL) {
		distances = nodes_distance; /* application responds for the vector */
		nodes_distance = NULL;
	}
	else {
		delete nodes_distance;
		nodes_distance = NULL;
	}

	return result;
}

/***********************************************************************************************
*
* @brief   Search the nearest node in specified location for specified point in the request.
*
* @return  Return pointer to the nearest node in kd tree that satisfy the request.
*
***********************************************************************************************/
kdnode * kdtree_searcher::find_nearest_node() {
	prepare_storages();

	kdnode * node = NULL;

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
	nearest_nodes = NULL;

	delete nodes_distance;
	nodes_distance = NULL;

	return node;
}
