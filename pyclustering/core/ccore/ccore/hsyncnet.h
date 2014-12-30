#ifndef _HSYNCNET_H_
#define _HSYNCNET_H_

#include <vector>

#include "syncnet.h"

class hsyncnet: public syncnet {
private:
	unsigned int number_clusters;

public:
	hsyncnet(std::vector<std::vector<double> > * input_data, const unsigned int cluster_number, const initial_type initial_phases);
	
	virtual ~hsyncnet(void);

	virtual std::vector< std::vector<sync_dynamic> * > * process(const double order, const solve_type solver, const bool collect_dynamic);
};

#endif
