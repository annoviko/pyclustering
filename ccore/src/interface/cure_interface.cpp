/*!

@authors Andrei Novikov (pyclustering@yandex.ru)
@date 2014-2020
@copyright BSD-3-Clause

*/

#include <pyclustering/interface/cure_interface.h>

#include <pyclustering/cluster/cure.hpp>


void * cure_algorithm(const pyclustering_package * const sample, const size_t number_clusters, const size_t number_repr_points, const double compression) {
    pyclustering::dataset input_dataset;
    sample->extract(input_dataset);

    pyclustering::clst::cure solver(number_clusters, number_repr_points, compression);

    pyclustering::clst::cure_data * output_result = new pyclustering::clst::cure_data();
    solver.process(input_dataset, *output_result);

    return output_result;
}


void cure_data_destroy(void * pointer_cure_data) {
    delete (pyclustering::clst::cure_data *) pointer_cure_data;
}


pyclustering_package * cure_get_clusters(void * pointer_cure_data) {
    pyclustering::clst::cure_data & output_result = (pyclustering::clst::cure_data &) *((pyclustering::clst::cure_data *)pointer_cure_data);

    pyclustering_package * package = create_package(&output_result.clusters());
    return package;
}


pyclustering_package * cure_get_representors(void * pointer_cure_data) {
    pyclustering::clst::cure_data & output_result = (pyclustering::clst::cure_data &) *((pyclustering::clst::cure_data *)pointer_cure_data);

    pyclustering_package * package = create_package(&output_result.representors());
    return package;
}


pyclustering_package * cure_get_means(void * pointer_cure_data) {
    pyclustering::clst::cure_data & output_result = (pyclustering::clst::cure_data &) *((pyclustering::clst::cure_data *)pointer_cure_data);

    pyclustering_package * package = create_package(&output_result.means());
    return package;
}
