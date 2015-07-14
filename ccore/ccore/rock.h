/**************************************************************************************************************

Cluster analysis algorithm: ROCK

Based on article description:
 - S.Guha, R.Rastogi, K.Shim. ROCK: A Robust Clustering Algorithm for Categorical Attributes. 1999.

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

#ifndef _ROCK_H_
#define _ROCK_H_

#include <vector>
#include <list>

class rock {
private:
	std::vector<std::vector<double> >			* dataset;
	std::vector<std::vector<unsigned int> >		* adjacency_matrix;

	std::vector<std::vector<unsigned int> *>	* vector_clusters;		/* created only at the end of processing */
	std::list<std::vector<unsigned int> *>		* clusters;				/* removed when processing is over */

	double			degree_normalization;
	unsigned int	number_clusters;

public:
	rock(const std::vector<std::vector<double> > * const dataset, const double radius, const unsigned int number_clusters, const double threshold);

	~rock(void);

	void process(void);

	inline const std::vector<std::vector<unsigned int> *> * const get_clusters(void) const {
		return vector_clusters;
	}

private:
	bool merge_cluster(void);

	std::vector<unsigned int> * find_pair_clusters(void) const;

	unsigned int calculate_links(std::list<std::vector<unsigned int> *>::iterator & cluster1, std::list<std::vector<unsigned int> *>::iterator & cluster2) const;

	double calculate_goodness(std::list<std::vector<unsigned int> *>::iterator & cluster1, std::list<std::vector<unsigned int> *>::iterator & cluster2) const;
};

#endif
