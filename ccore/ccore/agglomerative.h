/**************************************************************************************************************

Cluster analysis algorithm: Agglomerative

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

#ifndef _AGGLOMERATIVE_HPP_
#define _AGGLOMERATIVE_HPP_

#include <vector>

typedef std::vector<double>         point;
typedef std::vector<unsigned int>   cluster;

typedef enum type_link {
    SINGLE_LINK     = 0,
    COMPLETE_LINK   = 1,
    AVERAGE_LINK    = 2,
    CENTROID_LINK   = 3
} type_link;

class agglomerative {
private:
    unsigned int            m_number_clusters;
    type_link               m_similarity;

    std::vector<point>      m_centers;
    std::vector<cluster>    m_clusters;

    std::vector<point> *    m_ptr_data;

public:
    agglomerative(void);

    agglomerative(const unsigned int number_clusters, const type_link link);

    ~agglomerative(void);

public:
    void initialize(const unsigned int number_clusters, const type_link link);

    void process(const std::vector<point> & data);

public:
    inline void get_clusters(std::vector<std::vector<unsigned int> > & output_clusters) const {
        output_clusters.clear();
        output_clusters.resize(m_clusters.size());

        std::copy(m_clusters.begin(), m_clusters.end(), output_clusters.begin());
    }

private:
    void merge_similar_clusters(void);

    void merge_by_average_link(void);

    void merge_by_centroid_link(void);

    void merge_by_complete_link(void);

    void merge_by_signle_link(void);

    void calculate_center(const cluster & cluster, point & center);
};

#endif
