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


class ordering_analyser {
private:
	ordering_ptr	m_ordering;

public:
	ordering_analyser(void) = default;

	ordering_analyser(const ordering_analyser & p_other) = default;

	ordering_analyser(ordering_analyser && p_other) = default;

	ordering_analyser(ordering_ptr & p_ordering);

	~ordering_analyser(void) = default;

public:
	double calculate_connvectivity_radius(const std::size_t p_amount_clusters) const;

	std::size_t extract_cluster_amount(const double p_radius) const;

public:
	inline ordering_ptr ordering(void) const { return m_ordering; }
};


}