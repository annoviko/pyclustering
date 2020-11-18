/*!

@authors Andrei Novikov (pyclustering@yandex.ru)
@date 2014-2020
@copyright BSD-3-Clause

*/

#include <pyclustering/interface/kmedians_interface.h>

#include <pyclustering/cluster/kmedians.hpp>


pyclustering_package * kmedians_algorithm(const pyclustering_package * const p_sample, 
                                          const pyclustering_package * const p_initial_medians, 
                                          const double p_tolerance,
                                          const std::size_t p_itermax,
                                          const void * const p_metric)
{
    pyclustering::dataset data, medians;

    p_sample->extract(data);
    p_initial_medians->extract(medians);

    distance_metric<pyclustering::point> * metric = ((distance_metric<pyclustering::point> *) p_metric);
    distance_metric<pyclustering::point> default_metric = distance_metric_factory<pyclustering::point>::euclidean_square();

    if (!metric) {
        metric = &default_metric;
    }

    pyclustering::clst::kmedians algorithm(medians, p_tolerance, p_itermax, *metric);

    pyclustering::clst::kmedians_data output_result;
    algorithm.process(data, output_result);

    pyclustering_package * package = create_package_container(KMEDIANS_PACKAGE_SIZE);
    ((pyclustering_package **) package->data)[KMEDIANS_PACKAGE_INDEX_CLUSTERS] = create_package(&output_result.clusters());
    ((pyclustering_package **) package->data)[KMEDIANS_PACKAGE_INDEX_MEDIANS] = create_package(&output_result.medians());

    return package;
}
