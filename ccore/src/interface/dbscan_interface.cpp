#include "interface/dbscan_interface.h"

#include "cluster/dbscan.hpp"


pyclustering_package * dbscan_algorithm(const data_representation * const sample, const double radius, const size_t minumum_neighbors) {
    std::unique_ptr<dataset> input_dataset(read_sample(sample));

    cluster_analysis::dbscan solver(radius, minumum_neighbors);

    cluster_analysis::dbscan_data output_result;
    solver.process(*input_dataset, output_result);

    pyclustering_package * package = new pyclustering_package((unsigned int) pyclustering_type_data::PYCLUSTERING_TYPE_LIST);
    package->size = output_result.size() + 1;   /* the last for noise */
    package->data = new pyclustering_package * [package->size + 1];

    for (unsigned int i = 0; i < package->size - 1; i++) {
        ((pyclustering_package **) package->data)[i] = create_package(&output_result[i]);
    }

    ((pyclustering_package **) package->data)[package->size - 1] = create_package(output_result.noise().get());

    return package;
}
