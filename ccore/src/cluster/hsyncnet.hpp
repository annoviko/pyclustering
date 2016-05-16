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

#ifndef _HSYNCNET_H_
#define _HSYNCNET_H_

#include <vector>

#include "cluster/syncnet.hpp"


typedef std::vector<unsigned int>			hsyncnet_cluster;
typedef ensemble_data<hsyncnet_cluster>		hsyncnet_cluster_data;
typedef syncnet_analyser					hsyncnet_analyser;


class hsyncnet: public syncnet {
private:
	unsigned int m_number_clusters;
    unsigned int m_initial_neighbors;
    double m_increase_persent;

public:
	hsyncnet(std::vector<std::vector<double> > * input_data, 
        const unsigned int cluster_number, 
        const initial_type initial_phases);

    hsyncnet(std::vector<std::vector<double> > * input_data,
        const unsigned int cluster_number,
        const initial_type initial_phasesconst,
        const unsigned int initial_neighbors,
        const double increase_persent);
	
	virtual ~hsyncnet(void);

	virtual void process(const double order, const solve_type solver, const bool collect_dynamic, hsyncnet_analyser & analyser);
};


#endif
