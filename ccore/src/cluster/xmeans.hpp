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

#ifndef _XMEANS_H_
#define _XMEANS_H_

#include <vector>

#define FAST_SOLUTION

class xmeans {
private:
    std::vector<std::vector<double> >           * m_dataset;
    std::vector<std::vector<unsigned int> >	    m_clusters;
    std::vector<std::vector<double> >           m_centers;

	unsigned int    m_maximum_clusters;
	double          m_tolerance;

public:
	xmeans(const std::vector<std::vector<double> > & data, const std::vector<std::vector<double> > & initial_centers, const unsigned int kmax, const double minimum_change);

	~xmeans(void);

	void process(void);

	inline void get_clusters(std::vector<std::vector<unsigned int> > & output_clusters) const {
		output_clusters.clear();
		output_clusters.resize(m_clusters.size());

		std::copy(m_clusters.begin(), m_clusters.end(), output_clusters.begin());
	}

private:
	void update_clusters(std::vector<std::vector<unsigned int> > & clusters, const std::vector<std::vector<double> > & centers, const std::vector<unsigned int> & available_indexes);

	double update_centers(const std::vector<std::vector<unsigned int> > & clusters, std::vector<std::vector<double> > & centers);

	void improve_structure(void);

	void improve_parameters(std::vector<std::vector<unsigned int> > & clusters, std::vector<std::vector<double> > & centers, const std::vector<unsigned int> & available_indexes);

	double splitting_criterion(const std::vector<std::vector<unsigned int> > & clusters, const std::vector<std::vector<double> > & centers) const;

	unsigned int find_proper_cluster(const std::vector<std::vector<double> > & analysed_centers, const std::vector<double> & point) const;
};

#endif
