#ifndef _KDTREE_H_
#define _KDTREE_H_

#include <vector>

class kdnode {
private:
	const std::vector<double> * 	data;
	const void * 					payload;

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

	inline double get_value(void) const { return (*data)[discriminator]; }
	inline double get_value(const unsigned int discr) { return (*data)[discr]; }
	inline unsigned int get_discriminator(void) const { return discriminator; }

	inline std::vector<kdnode *> * get_children(void) {
		std::vector<kdnode *> * children = new std::vector<kdnode *>();
		if (left != NULL) { children->push_back(left); }
		if (right != NULL) { children->push_back(right); }

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


class kdtree {
private:
	kdnode *		root;
	unsigned int	dimension;

private:
	kdnode * recursive_remove(kdnode * node);

	kdnode * find_minimal_node(kdnode * cur_node, unsigned int discriminator);

public:
	kdtree(void);

	kdtree(const std::vector< std::vector<double> *> * data, const std::vector<void *> * payloads);

	~kdtree(void);

	kdnode * insert(std::vector<double> * point, void * payload);

	void remove(std::vector<double> * point);

	kdnode * find_node(std::vector<double> * point);

	kdnode * find_node(std::vector<double> * point, kdnode * cur_node);
};


class kdtree_searcher {
private:
	double minimal_distance;
	double distance;
	kdnode * intial_node;
	std::vector<double> * req_point;

private:


public:
	kdtree_searcher(std::vector<double> * point, kdnode * node, const double radius_search);

	~kdtree_searcher(void);

	void initialize(std::vector<double> * point, kdnode * node, const double radius_search);

	std::vector<kdnode *> * find_nearest_nodes(void);

	kdnode * find_nearest_node(void);
};

#endif
