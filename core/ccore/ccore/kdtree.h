#ifndef _KDTREE_H_
#define _KDTREE_H_

#include <vector>

template <class TData>
class kdnode {
private:
	const std::vector<TData *> * 	data;
	const void * 					payload;

	kdnode  *		left;
	kdnode  *		right;
	kdnode  *		parent;
	unsigned int	discriminator;

public:
	kdnode(std::vector<TData *> * p_data, void * p_payload,  kdnode * p_left, kdnode * p_right, kdnode * p_parent, unsigned int disc);
	~kdnode(void);

	inline void set_left(kdnode * node) { left = node; }
	inline void set_right(kdnode * node) { right = node; }
	inline void set_parent(kdnode * node) { parent = node; }

	inline kdnode * get_left(void) { return left; }
	inline kdnode * get_right(void) { return right; }
	inline kdnode * get_parent(void) { return parent; }

	inline TData * get_value(void) { return data[discriminator]; }

	std::vector<kdnode *> * get_children(void);

	inline bool operator < (const & kdnode node1, const & kdnode node2) { return *(node1.get_value()) < *(node2.get_value()); }
	inline bool operator > (const & kdnode node1, const & kdnode node2) { return node2 < node1; }
	inline bool operator <= (const & kdnode node1, const & kdnode node2) { return !(node1 > node2); }
	inline bool operator >= (const & kdnode node1, const & kdnode node2) { return !(node1 < node2); }
};


template <class TData>
class kdtree {
private:
	kdnode<TData> * root;
	unsigned int	dimension;

public:
	kdtree(const std::vector<TData *> * data, const std::vector<void *> payloads);

	~kdtree(void);

	kdnode * insert(TData * point, void * payload);

	void remove(kdnode * node);

	kdnode * find_minimal_node(kdnode * cur_node, unsigned int discriminator);

	kdnode * find_node(TData * point, kdnode * cur_node);

	kdnode * find_nearest_dist_node(TData * point, double distance);

	std::vector<kdnode *> * find_nearest_dist_nodes(TData * point, double distance);
};

#endif
