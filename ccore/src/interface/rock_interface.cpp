/*!

@authors Andrei Novikov (pyclustering@yandex.ru)
@date 2014-2020
@copyright BSD-3-Clause

*/

#include <pyclustering/interface/rock_interface.h>

#include <pyclustering/cluster/rock.hpp>


pyclustering_package * rock_algorithm(const pyclustering_package * const p_sample, const double p_radius, const size_t p_number_clusters, const double p_threshold) {
    pyclustering::dataset input_dataset;
    p_sample->extract(input_dataset);

    pyclustering::clst::rock solver(p_radius, p_number_clusters, p_threshold);

    pyclustering::clst::rock_data output_result;
    solver.process(input_dataset, output_result);

    pyclustering_package * package = create_package(&output_result.clusters());
    return package;
}
