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

#ifndef _KMEANS_H_
#define _KMEANS_H_

#include <vector>

class kmeans {
private:
	std::vector<std::vector<double> >			* dataset;
	std::vector<std::vector<unsigned int> *>	* clusters;
	std::vector<std::vector<double> >			* centers;

	double										tolerance;

public:
	kmeans(const std::vector<std::vector<double> > * const data, const std::vector<std::vector<double> > * const centers, const double tolerance);

	~kmeans(void);

	void process(void);

	inline const std::vector<std::vector<unsigned int> *> * const get_clusters(void) const {
		return clusters;
	}

private:
	void update_clusters(void);

	double update_centers(void);
};

#endif
