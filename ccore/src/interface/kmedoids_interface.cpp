/*!

@authors Andrei Novikov (pyclustering@yandex.ru)
@date 2014-2020
@copyright BSD-3-Clause

*/

#include <pyclustering/interface/kmedoids_interface.h>

#include <pyclustering/cluster/kmedoids.hpp>

#include <pyclustering/utils/metric.hpp>


using namespace pyclustering::utils::metric;


pyclustering_package * kmedoids_algorithm(const pyclustering_package * const p_sample,
                                          const pyclustering_package * const p_medoids,
                                          const double p_tolerance,
                                          const std::size_t p_itermax,
                                          const void * const p_metric,
                                          const std::size_t p_type)
{
    pyclustering::clst::medoid_sequence medoids;
    p_medoids->extract(medoids);

    distance_metric<pyclustering::point> * metric = ((distance_metric<pyclustering::point> *) p_metric);
    distance_metric<pyclustering::point> default_metric = distance_metric_factory<pyclustering::point>::euclidean_square();

    if (!metric) {
        metric = &default_metric;
    }

    pyclustering::clst::kmedoids algorithm(medoids, p_tolerance, p_itermax, *metric);

    pyclustering::dataset input_dataset;
    p_sample->extract(input_dataset);

    pyclustering::clst::kmedoids_data output_result;
    algorithm.process(input_dataset, (pyclustering::clst::kmedoids_data_t) p_type, output_result);

    pyclustering_package * package = create_package_container(KMEDOIDS_PACKAGE_SIZE);
    ((pyclustering_package **) package->data)[KMEDOIDS_PACKAGE_INDEX_CLUSTERS] = create_package(&output_result.clusters());
    ((pyclustering_package **) package->data)[KMEDOIDS_PACKAGE_INDEX_MEDOIDS] = create_package(&output_result.medoids());

    return package;
}

