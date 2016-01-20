#ifndef _ADJACENCY_FACTORY_H_
#define _ADJACENCY_FACTORY_H_

#include "adjacency.h"

#include <memory>


enum adjacency_t {
	ADJACENCY_BIT_MATRIX,
    ADJACENCY_MATRIX,
	ADJACENCY_LIST
};


enum adjacency_weight_t {
    ADJACENCY_WEIGHT_MATRIX,
    ADJACENCY_WEIGHT_LIST
};


enum connection_t {
    CONNECTION_NONE,
    CONNECTION_GRID_FOUR,
    CONNECTION_GRID_EIGHT,
    CONNECTION_ALL_TO_ALL,
    CONNECTION_LIST_BIDIRECTIONAL,
};


class adjacency_factory {
public:
    std::shared_ptr<adjacency_collection> create_collection(const adjacency_t storing_type);

    std::shared_ptr<adjacency_collection> create_collection(const adjacency_t storing_type, const connection_t structure_type);
};


class adjacency_weight_factory {
public:
    std::shared_ptr<adjacency_weight_collection> create_collection(const adjacency_weight_t type);

    std::shared_ptr<adjacency_weight_collection> create_collection(const adjacency_weight_t storing_type, const connection_t structure_type);
};

#endif