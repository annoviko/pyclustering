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


#include "container/adjacency.hpp"


using namespace container;


void template_set_connection(adjacency_collection & collection);

void template_has_no_connection(adjacency_collection & collection);

void template_has_all_connection(adjacency_collection & collection);

void template_erase_connection(adjacency_collection & collection);

void template_get_neighbors_sizes(adjacency_collection & collection);

void template_get_neighbors_indexes(adjacency_collection & collection);

void template_no_get_neighbors(adjacency_collection & collection);

void template_all_get_neighbors(adjacency_collection & collection);

void template_get_neighbors_after_erase(adjacency_collection & collection);

void template_set_weight_connection(adjacency_weight_collection & collection);

void template_set_default_weight_connection(adjacency_weight_collection & collection);

void template_set_negative_weight(adjacency_weight_collection & collection);

void template_get_neighbors_positive_negative(adjacency_weight_collection & collection);