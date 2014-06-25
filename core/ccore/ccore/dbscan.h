#ifndef _DBSCAN_H_
#define _DBSCAN_H_

#include <cmath>
#include <vector>
#include <algorithm>

#include <iostream>

typedef std::vector<std::vector<double> >  	matrix;
typedef std::vector<unsigned int>			cluster;

class dbscan {
private:
	std::vector<std::vector<double> >			* data;
	std::vector<bool>							* visited;
	std::vector<bool>							* belong;
	std::vector<std::vector<unsigned int> *>	* clusters;
	std::vector<unsigned int>					* noise;
	std::vector<std::vector<unsigned int> *>	* matrix_neighbors;

	double					radius;
	unsigned int			neighbors;

public:
	dbscan(std::vector<std::vector<double> > * input_data, const double radius_connectivity, const unsigned int minimum_neighbors);

	~dbscan();

	void process(void);

	const std::vector<std::vector<unsigned int> *> * const get_clusters(void) const;

	const std::vector<unsigned int> * const get_noise(void) const;

private:
	std::vector<std::vector<unsigned int> * > * create_neighbor_matrix(void);
};

#endif