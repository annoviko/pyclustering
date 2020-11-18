/*!

@authors Andrei Novikov (pyclustering@yandex.ru)
@date 2014-2020
@copyright BSD-3-Clause

*/

#include <pyclustering/interface/dbscan_interface.h>

#include <pyclustering/cluster/dbscan.hpp>


pyclustering_package * dbscan_algorithm(const pyclustering_package * const p_sample, 
                                        const double p_radius,
                                        const size_t p_minumum_neighbors,
                                        const size_t p_data_type)
{
    pyclustering::dataset input_dataset;
    p_sample->extract(input_dataset);

    pyclustering::clst::dbscan solver(p_radius, p_minumum_neighbors);

    pyclustering::clst::dbscan_data output_result;

    solver.process(input_dataset, (pyclustering::clst::dbscan_data_t) p_data_type, output_result);

    pyclustering_package * package = new pyclustering_package(pyclustering_data_t::PYCLUSTERING_TYPE_LIST);
    package->size = output_result.size() + 1;   /* the last for noise */
    package->data = new pyclustering_package * [package->size + 1];

    for (std::size_t i = 0; i < package->size - 1; i++) {
        ((pyclustering_package **) package->data)[i] = create_package(&output_result[i]);
    }

    ((pyclustering_package **) package->data)[package->size - 1] = create_package(&output_result.noise());

    return package;
}
