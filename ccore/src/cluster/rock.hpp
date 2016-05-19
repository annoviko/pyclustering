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

#ifndef _ROCK_H_
#define _ROCK_H_


#include <vector>
#include <list>

#include "container/adjacency_matrix.hpp"

#include "cluster/cluster_algorithm.hpp"

#include "definitions.hpp"


using namespace container;


namespace cluster_analysis {


using rock_data = cluster_data;


class rock : public cluster_algorithm {
private:
    /* for optimization list representation is of clusters is used and than
     * it is moved to output result */
    using rock_cluster_sequence = std::list<cluster>;

private:
    adjacency_matrix        m_adjacency_matrix;

    double                  m_radius;

    double                  m_degree_normalization;

    size_t                  m_number_clusters;

    rock_cluster_sequence   m_clusters;

public:
    rock(void);

    rock(const double radius, const size_t number_clusters, const double threshold);

    virtual ~rock(void);

public:
    virtual void process(const dataset & p_data, cluster_data & p_result);

private:
    void create_adjacency_matrix(const dataset & p_data);

    bool merge_cluster(void);

    std::vector<unsigned int> * find_pair_clusters(void) const;

    unsigned int calculate_links(const cluster & cluster1, const cluster & cluster2) const;

    double calculate_goodness(const cluster & cluster1, const cluster & cluster2) const;
};


}


#endif
