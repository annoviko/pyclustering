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


#pragma once


#include <list>
#include <tuple>

#include "cluster/cluster_algorithm.hpp"
#include "cluster/optics_data.hpp"


namespace cluster_analysis {


struct optics_descriptor {
public:
    std::size_t     m_index = -1;
    double          m_core_distance = 0;
    double          m_reachability_distance = 0;
    bool            m_processed = false;

public:
    optics_descriptor(void) = default;

    optics_descriptor(const optics_descriptor & p_other) = default;

    optics_descriptor(optics_descriptor && p_other) = default;

    optics_descriptor(const std::size_t p_index, const double p_core_distance, const double p_reachability_distance);

    ~optics_descriptor(void) = default;

public:
	void clear(void);
};


class optics : public cluster_algorithm  {
public:
	static const double	NONE_DISTANCE;

private:
    const dataset       * m_data_ptr;

    optics_data         * m_result_ptr;

    double              m_radius;

    std::size_t         m_neighbors;

    std::size_t         m_amount_clusters;

    std::vector<optics_descriptor>      m_optics_objects;

    std::vector<optics_descriptor *>    m_ordered_database;

public:
    optics(void) = default;

    optics(const optics & p_other) = default;

    optics(optics && p_other) = default;

    optics(const double p_radius, const std::size_t p_neighbors);

    optics(const double p_radius, const std::size_t p_neighbors, const std::size_t p_amount_clusters);

    virtual ~optics(void) = default;

public:
    virtual void process(const dataset & p_data, cluster_data & p_result) override;

private:
    void initialize(void);

    void allocate_clusters(void);

    void expand_cluster_order(optics_descriptor & p_object);

    void extract_clusters(void);

    void get_neighbors(const std::size_t p_index, std::vector< std::tuple<std::size_t, double> > & p_neighbors);

	void update_order_seed(const optics_descriptor & p_object, const std::vector< std::tuple<std::size_t, double> > & neighbors, std::list<optics_descriptor *> & order_seed);

	void calculate_ordering(void);

	void calculate_cluster_result(void);
};


}