#ifndef _ADJACENCY_FACTORY_H_
#define _ADJACENCY_FACTORY_H_

#include "adjacency.h"
#include "adjacency_connector.h"

#include <memory>


enum class adjacency_unweight_t {
	ADJACENCY_BIT_MATRIX,
    ADJACENCY_MATRIX,
	ADJACENCY_LIST
};


enum class adjacency_weight_t {
    ADJACENCY_MATRIX,
    ADJACENCY_LIST
};


class adjacency_unweight_factory {
public:
    static std::shared_ptr<adjacency_collection> create_collection(const size_t amount_nodes, const adjacency_unweight_t storing_type);

    static std::shared_ptr<adjacency_collection> create_collection(const size_t amount_nodes, const adjacency_unweight_t storing_type, const connection_t structure_type);
};


class adjacency_weight_factory {
public:
    static std::shared_ptr<adjacency_weight_collection> create_collection(const size_t amount_nodes, const adjacency_weight_t storing_type);

    static std::shared_ptr<adjacency_weight_collection> create_collection(const size_t amount_nodes, const adjacency_weight_t storing_type, const connection_t structure_type);

    static std::shared_ptr<adjacency_weight_collection> create_collection(const size_t amount_nodes, const adjacency_weight_t storing_type, const connection_t structure_type, const double default_weight_value);

    static std::shared_ptr<adjacency_weight_collection> create_collection(const size_t amount_nodes, const adjacency_weight_t storing_type, const connection_t structure_type, double (*weight_value_generator)(void));
};

#endif