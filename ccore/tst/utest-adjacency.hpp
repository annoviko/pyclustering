/*!

@authors Andrei Novikov (pyclustering@yandex.ru)
@date 2014-2020
@copyright BSD-3-Clause

*/


#pragma once


#include <pyclustering/container/adjacency.hpp>


using namespace pyclustering::container;


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