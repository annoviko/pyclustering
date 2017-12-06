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


#include "optics_data.hpp"


namespace cluster_analysis {


/**
*
* @brief    Analyzer of cluster ordering data.
*
*/
class ordering_analyser {
private:
    ordering_ptr    m_ordering;

public:
    /**
    *
    * @brief    Default constructor of the analyser.
    *
    */
    ordering_analyser(void) = default;

    /**
    *
    * @brief    Default copy constructor of the analyser.
    *
    */
    ordering_analyser(const ordering_analyser & p_other) = default;

    /**
    *
    * @brief    Default move constructor of the analyser.
    *
    */
    ordering_analyser(ordering_analyser && p_other) = default;

    /**
    *
    * @brief    Creates ordering analyser using specified cluster-ordering.
    *
    */
    explicit ordering_analyser(const ordering_ptr & p_ordering);

    /**
    *
    * @brief    Default destructor.
    *
    */
    ~ordering_analyser(void) = default;

public:
    /**
    *
    * @brief    Calculates connectivity radius of allocation specified amount of clusters using ordering diagram.
    *
    * @param[in] p_amount_clusters: amount of clusters that should be allocated by calculated connectivity radius.
	* @param[in] p_maximum_iterations: maximum number of iteration for searching connectivity radius to allocated 
	*             specified amount of clusters (by default it is restricted by 100 iterations).
    *
    * @return   Value of connectivity radius, it may return value < 0 if connectivity radius hasn't been found for the specified amount of iterations.
    *
    */
    double calculate_connvectivity_radius(const std::size_t p_amount_clusters, const std::size_t p_maximum_iterations = 100) const;

    /**
    *
    * @brief    Obtains amount of clustering that can be allocated by using specified radius for ordering diagram
    *
    * @param[in] p_radius: connectivity radius that is used for cluster allocation.
    *
    * @return   Amount of clusters that can be allocated by the connectivity radius on ordering diagram.
    *
    */
    std::size_t extract_cluster_amount(const double p_radius) const;

public:
    /**
    *
    * @brief    Returns cluster-ordering sequence that used for analysis.
    *
    */
    inline ordering_ptr ordering(void) const { return m_ordering; }
};


}
