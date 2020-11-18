/*!

@authors Andrei Novikov (pyclustering@yandex.ru)
@date 2014-2020
@copyright BSD-3-Clause

*/

#include <pyclustering/container/adjacency_factory.hpp>

#include <pyclustering/container/adjacency_bit_matrix.hpp>
#include <pyclustering/container/adjacency_list.hpp>
#include <pyclustering/container/adjacency_matrix.hpp>
#include <pyclustering/container/adjacency_weight_list.hpp>


namespace pyclustering {

namespace container {


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
        throw std::runtime_error("Unknown type of adjacency collection without weights is required from the factory.");
    }

    /* establish structures between nodes */
    adjacency_connector<adjacency_collection> connector;
    connector.create_structure(structure_type, *collection);

    return std::shared_ptr<adjacency_collection>(collection);
}


std::shared_ptr<adjacency_weight_collection> adjacency_weight_factory::create_collection(const size_t amount_nodes, const adjacency_weight_t storing_type, const connection_t structure_type, const std::function<double()> & weight_value_generator) {
    adjacency_weight_collection * collection = nullptr;

    switch(storing_type) {
    case adjacency_weight_t::ADJACENCY_LIST:
        collection = new adjacency_weight_list(amount_nodes);
        break;

    case adjacency_weight_t::ADJACENCY_MATRIX:
        collection = new adjacency_matrix(amount_nodes);
        break;

    default:
        throw std::runtime_error("Unknown type of adjacency collection without weights is required from the factory.");
    }

    /* establish structures between nodes */
    adjacency_weight_connector<adjacency_weight_collection> connector(weight_value_generator);
    connector.create_structure(structure_type, *collection);

    return std::shared_ptr<adjacency_weight_collection>(collection);
}


}

}