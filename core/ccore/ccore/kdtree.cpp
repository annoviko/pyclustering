#include <kdtree.h>

kdnode::kdnode(std::vector<TData> * p_data, void * p_payload,  kdnode * p_left, kdnode * p_right, kdnode * p_parent, unsigned int disc) :
data(p_data), payload(p_payload), left(p_left), right(p_right), parent(p_parent), discriminator(disc)
{ }

kdnode::~kdnode(void) { }

std::vector<kdnode *> * kdnode::get_children(void) {
	std::vector<kdnode *> * children = new std::vector<kdnode *>();
	if (left != NULL) { children->push_back(left); }
	if (right != NULL) { children->push_back(right); }

	return children;
}
