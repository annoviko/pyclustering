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

#ifndef _INTERFACE_NETWORK_H_
#define _INTERFACE_NETWORK_H_

typedef enum initial_type {
	RANDOM_GAUSSIAN,
	EQUIPARTITION,
	TOTAL_NUMBER_INITIAL_TYPES
} initial_type;


typedef enum solve_type {
	FAST,
	RK4,
	RKF45,
	TOTAL_NUMBER_SOLVE_TYPES
} solve_type;

#endif
