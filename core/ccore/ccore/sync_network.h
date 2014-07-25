#ifndef _SYNC_NETWORK_H_
#define _SYNC_NETWORK_H_

#include <vector>


class sync_network {
private:
	unsigned int			num_osc;
	std::vector<double>		phases;
	std::vector<double>		frequency;
	double					weight;
};

#endif