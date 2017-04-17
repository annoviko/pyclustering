/**
*
* Copyright (C) 2014-2017    Andrei Novikov (pyclustering@yandex.ru)
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

#include "definitions.hpp"


enum class splitting_type {
    BAYESIAN_INFORMATION_CRITERION = 0,
    MINIMUM_NOISELESS_DESCRIPTION_LENGTH = 1,
};


class xmeans {
private:
    dataset                                     * m_dataset;
    std::vector<std::vector<unsigned int> >     m_clusters;
    dataset                                     m_centers;

    unsigned int        m_maximum_clusters;
    double              m_tolerance;
    splitting_type      m_criterion;

public:
    xmeans(const dataset & data, const dataset & initial_centers, const unsigned int kmax, const double minimum_change, const splitting_type p_criterion);

    ~xmeans(void);

public:
    void process(void);

    inline void get_clusters(std::vector<std::vector<unsigned int> > & output_clusters) const {
        output_clusters.clear();
        output_clusters.resize(m_clusters.size());

        std::copy(m_clusters.begin(), m_clusters.end(), output_clusters.begin());
    }

private:
    void update_clusters(std::vector<std::vector<unsigned int> > & clusters, const dataset & centers, const std::vector<unsigned int> & available_indexes);

    double update_centers(const std::vector<std::vector<unsigned int> > & clusters, dataset & centers);

    void improve_structure(void);

    void improve_parameters(std::vector<std::vector<unsigned int> > & clusters, dataset & centers, const std::vector<unsigned int> & available_indexes);

    double splitting_criterion(const std::vector<std::vector<unsigned int> > & clusters, const dataset & centers) const;

    unsigned int find_proper_cluster(const dataset & analysed_centers, const point & p_point) const;

    double bayesian_information_criterion(const std::vector<std::vector<unsigned int> > & clusters, const dataset & centers) const;

    double minimum_noiseless_description_length(const std::vector<std::vector<unsigned int> > & clusters, const dataset & centers) const;
};

#endif
