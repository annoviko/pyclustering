#include "adjacency_factory.h"

#include "adjacency_bit_matrix.h"
#include "adjacency_list.h"
#include "adjacency_matrix.h"
#include "adjacency_weight_list.h"


std::shared_ptr<adjacency_collection> adjacency_unweight_factory::create_collection(const size_t amount_nodes, const adjacency_unweight_t storing_type) {
    return create_collection(amount_nodes, storing_type, connection_t::CONNECTION_NONE);
}

std::shared_ptr<adjacency_collection> adjacency_unweight_factory::create_collection(const size_t amount_nodes, const adjacency_unweight_t storing_type, const connection_t structure_type) {
    adjacency_collection * collection = nullptr;

    switch(storing_type) {
    case adjacency_unweight_t::ADJACENCY_BIT_MATRIX:
        collection = new adjacency_bit_matrix(amount_nodes);
        break;

    case adjacency_unweight_t::ADJACENCY_LIST:
        collection = new adjacency_list(amount_nodes);
        break;

    case adjacency_unweight_t::ADJACENCY_MATRIX:
        collection = new adjacency_matrix(amount_nodes);
        break;

    default:
        throw new std::runtime_error("Unknown type of adjacency collection without weights is required from the factory.");
    }

    /* establish structures between nodes */
    adjacency_connector connector;
    connector.create_structure(structure_type, *collection);

    return std::unique_ptr<adjacency_collection>(collection);
}