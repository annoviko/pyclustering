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

#ifndef _KDTREE_H_
#define _KDTREE_H_


#include <vector>


namespace container {

/***********************************************************************************************
 *
 * @brief   Node of KD Tree.
 *
 ***********************************************************************************************/
class kdnode {
private:
	const std::vector<double> * 	data;
	void * 							payload;

	kdnode  *		left;
	kdnode  *		right;
	kdnode  *		parent;
	unsigned int	discriminator;

public:
	kdnode(std::vector<double> * p_data, void * p_payload,  kdnode * p_left, kdnode * p_right, kdnode * p_parent, unsigned int disc);

	~kdnode(void);

	inline void set_left(kdnode * node) { left = node; }
	inline void set_right(kdnode * node) { right = node; }
	inline void set_parent(kdnode * node) { parent = node; }
	inline void set_discriminator(const unsigned int disc) { discriminator = disc; }

	inline kdnode * get_left(void) { return left; }
	inline kdnode * get_right(void) { return right; }
	inline kdnode * get_parent(void) { return parent; }

	inline void * get_payload(void) { return payload; }
	inline const std::vector<double> * get_data(void) { return data; }

	inline double get_value(void) const { return (*data)[discriminator]; }
	inline double get_value(const unsigned int discr) { return (*data)[discr]; }
	inline unsigned int get_discriminator(void) const { return discriminator; }

	inline std::vector<kdnode *> * get_children(void) {
		std::vector<kdnode *> * children = new std::vector<kdnode *>();
		if (left != nullptr) { children->push_back(left); }
		if (right != nullptr) { children->push_back(right); }

		return children;
	}
};


inline bool operator < (const kdnode & node, const std::vector<double> & point) { return node.get_value() < point[node.get_discriminator()]; }
inline bool operator < (const std::vector<double> & point, const kdnode & node) { return point[node.get_discriminator()] < node.get_value(); }

inline bool operator > (const kdnode & node, const std::vector<double> & point) { return point[node.get_discriminator()] < node.get_value(); }
inline bool operator > (const std::vector<double> & point, const kdnode & node) { return node.get_value() < point[node.get_discriminator()]; }

inline bool operator <= (const kdnode & node, const std::vector<double> & point) { return !(node.get_value() > point[node.get_discriminator()]); }
inline bool operator <= (const std::vector<double> & point, const kdnode & node) { return !(point[node.get_discriminator()] > node.get_value()); }

inline bool operator >= (const kdnode & node, const std::vector<double> & point) { return !(node.get_value() < point[node.get_discriminator()]); }
inline bool operator >= (const std::vector<double> & point, const kdnode & node) { return !(point[node.get_discriminator()] < node.get_value()); }

inline bool operator == (const kdnode & node, const std::vector<double> & point) { return node.get_value() == point[node.get_discriminator()]; }
inline bool operator == (const std::vector<double> & point, const kdnode & node) { return node == point; }


/***********************************************************************************************
 *
 * @brief   KD Tree - structure for storing data where fast distance searching is required.
 *
 ***********************************************************************************************/
class kdtree {
private:
	kdnode *		root;
	unsigned int	dimension;

private:
	/***********************************************************************************************
	*
	* @brief   Recursive remove of node in tree.
	*
	* @param   node            - node that should be removed.
	*
	* @return  Node that should replace removed node (if it's not leaf).
	*
	***********************************************************************************************/
	kdnode * recursive_remove(kdnode * node);

	/***********************************************************************************************
	*
	* @brief   Recursive destroy tree (used by destructor).
	*
	* @param   node            - node that should be destroyed.
	*
	***********************************************************************************************/
	void recursive_destroy(kdnode * node);

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
	kdnode * find_minimal_node(kdnode * cur_node, unsigned int discriminator);

public:
	/***********************************************************************************************
	*
	* @brief   Default constructor.
	*
	***********************************************************************************************/
	kdtree(void);

	/***********************************************************************************************
	*
	* @brief   Constructor of kd tree with pre-defined information.
	*
	* @param   data               - coordinates that describe nodes in tree.
	* @param   payloads           - payloads of nodes (can be nullptr if it's not required).
	*
	***********************************************************************************************/
	kdtree(const std::vector< std::vector<double> *> * data, const std::vector<void *> * payloads);

	/***********************************************************************************************
	*
	* @brief   Default destructor.
	*
	***********************************************************************************************/
	~kdtree(void);

	/***********************************************************************************************
	*
	* @brief   Insert new node in the tree.
	*
	* @param   point              - coordinates that describe node in tree.
	* @param   payload            - payloads of node (can be nullptr if it's not required).
	*
	* @return  Pointer to added node in the tree.
	*
	***********************************************************************************************/
	kdnode * insert(std::vector<double> * point, void * payload);

	/***********************************************************************************************
	*
	* @brief   Remove point with specified coordinates.
	*
	* @param   point              - coordinates that describe node in tree.
	*
	***********************************************************************************************/
	void remove(std::vector<double> * point);

	/***********************************************************************************************
	*
	* @brief   Remove node from the tree.
	*
	* @param   node_for_remove    - pointer to node that is located in tree.
	*
	***********************************************************************************************/
	void remove(kdnode * node_for_remove);

	/***********************************************************************************************
	*
	* @brief   Find node in tree using coordinates.
	*
	* @param   point              - coordinates of searched node.
	*
	* @return  Pointer to found node in tree.
	*
	***********************************************************************************************/
	kdnode * find_node(std::vector<double> * point);

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
	kdnode * find_node(std::vector<double> * point, kdnode * cur_node);

	/***********************************************************************************************
	*
	* @brief   Traverse tree from specified node and returns number of nodes in subtree.
	*
	* @param   node               - pointer to node of tree.
	*
	* @return  Returns number of nodes in subtree.
	*
	***********************************************************************************************/
	unsigned int traverse(kdnode * node);

	/***********************************************************************************************
	*
	* @brief   Return root of the tree.
	*
	* @return  Returns pointer to root of the tree.
	*
	***********************************************************************************************/
	inline kdnode * get_root(void) { return root; }
};


/***********************************************************************************************
 *
 * @brief   Searcher in KD Tree provides services related to searching in KD Tree.
 *
 ***********************************************************************************************/
class kdtree_searcher {
private:
	std::vector<double>	*	nodes_distance;
	std::vector<kdnode *> * nearest_nodes;

	double					distance;
	double					sqrt_distance;
	kdnode *				initial_node;
	std::vector<double> *	search_point;

private:
	/***********************************************************************************************
	*
	* @brief   Recursive method for searching nodes that satisfy the request.
	*
	* @param   node               - initial node in tree from which searching should performed.
	*
	***********************************************************************************************/
	void recursive_nearest_nodes(kdnode * node);

	/***********************************************************************************************
	*
	* @brief   Prepare storages that are required for searching.
	*
	***********************************************************************************************/
	void prepare_storages(void);

public:
	/***********************************************************************************************
	*
	* @brief   Default constructor. Search will not be performed until it's initialized.
	*
	***********************************************************************************************/
	kdtree_searcher(void);

	/***********************************************************************************************
	*
	* @brief   Constructor of searcher with request for searching.
	*
	* @param   (in) point              - point for which nearest nodes should be found.
	* @param   (in) node               - initial node in tree from which searching should started.
	* @param   (in) radius_search      - allowable distance for searching from the point.
	*
	***********************************************************************************************/
	kdtree_searcher(std::vector<double> * point, kdnode * node, const double radius_search);

	/***********************************************************************************************
	*
	* @brief   Default destructor.
	*
	***********************************************************************************************/
	~kdtree_searcher(void);

	/***********************************************************************************************
	*
	* @brief   Initialization of new request for searching.
	*
	* @param   (in) point              - point for which nearest nodes should be found.
	* @param   (in) node               - initial node in tree from which searching should started.
	* @param   (in) radius_search      - allowable distance for searching from the point.
	*
	***********************************************************************************************/
	void initialize(std::vector<double> * point, kdnode * node, const double radius_search);

	/***********************************************************************************************
	*
	* @brief   Search nodes that are located in specified distance from specified point.
	*
	* @return  Return vector of found nodes in kd tree that satisfy the request. If distances are
	*          specified then it will be filled by corresponding distances.
	*
	***********************************************************************************************/
	std::vector<kdnode *> * find_nearest_nodes(std::vector<double> * distances = nullptr);

	/***********************************************************************************************
	*
	* @brief   Search the nearest node in specified location for specified point in the request.
	*
	* @return  Return pointer to the nearest node in kd tree that satisfy the request.
	*
	***********************************************************************************************/
	kdnode * find_nearest_node(void);
};

}

#endif
