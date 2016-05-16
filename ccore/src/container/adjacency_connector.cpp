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

#include "container/adjacency_connector.hpp"


namespace container {

std::ostream & operator<<(std::ostream & p_stream, const connection_t & p_structure) {
	switch (p_structure) {
	case connection_t::CONNECTION_ALL_TO_ALL:
		p_stream << "all-to-all";
		break;

	case connection_t::CONNECTION_GRID_EIGHT:
		p_stream << "grid eight";
		break;

	case connection_t::CONNECTION_GRID_FOUR:
		p_stream << "grid four";
		break;

	case connection_t::CONNECTION_LIST_BIDIRECTIONAL:
		p_stream << "bidirectional list";
		break;

	case connection_t::CONNECTION_NONE:
		p_stream << "none structure";
		break;

	default:
		p_stream << "unknown structure";
		break;
	}

    return p_stream;
}

}
