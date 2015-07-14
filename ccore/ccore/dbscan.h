/**************************************************************************************************************

Cluster analysis algorithm: DBSCAN

Based on article description:
 - M.Ester, H.Kriegel, J.Sander, X.Xiaowei. A density-based algorithm for discovering clusters in large spatial 
   databases with noise. 1996.

Copyright (C) 2015    Andrei Novikov (pyclustering@yandex.ru)

pyclustering is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

pyclustering is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.

**************************************************************************************************************/

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

	inline const std::vector<std::vector<unsigned int> *> * const get_clusters(void) const {
		return clusters;
	}

	inline const std::vector<unsigned int> * const get_noise(void) const {
		return noise;
	}

private:
	std::vector<std::vector<unsigned int> * > * create_neighbor_matrix(void);
};

#endif
