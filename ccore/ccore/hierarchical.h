/**************************************************************************************************************

Cluster analysis algorithm: Classical Hierarchical Algorithm

Based on article description:
 - K.Anil, J.C.Dubes, R.C.Dubes. Algorithms for Clustering Data. 1988.

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

#ifndef _HIERARCHICAL_H_
#define _HIERARCHICAL_H_

#include <vector>
#include <list>

class hierarchical_cluster {
private:
	std::vector<std::vector<double> >	* dataset;	/* pointer to input data set */
	std::vector<unsigned int>		* indexes; 	/* indexes of objects in input data set */
	std::vector<double>			* center; 	/* center of the cluster */

public:
	hierarchical_cluster(const std::vector<std::vector<double> > * const data, const unsigned int index, const std::vector<double> * const point);

	~hierarchical_cluster(void);

	void append(const hierarchical_cluster * const cluster2);

	inline const std::vector<double> * const get_center(void) const {
		return center;
	}

	inline const std::vector<unsigned int> * const get_indexes(void) const {
		return indexes;
	}
};


class hierarchical {
private:
	std::list<hierarchical_cluster *>		* clusters;
	std::vector<std::vector<unsigned int> * >	* standard_clusters;
	std::vector<std::vector<double> >		* data;
	unsigned int 					number_clusters;

public:
	hierarchical(const std::vector<std::vector<double> > * const dataset, unsigned int cluster_number);

	~hierarchical(void);

	void process(void);

	inline const std::vector<std::vector<unsigned int> *> * const get_clusters(void) const {
		return standard_clusters;
	}

private:
	void merge_nearest_clusters(void);
};

#endif
