/*!

@authors Andrei Novikov (pyclustering@yandex.ru)
@date 2014-2020
@copyright BSD-3-Clause

*/


#include <pyclustering/interface/bsas_interface.h>

#include <pyclustering/cluster/bsas.hpp>

#include <pyclustering/utils/metric.hpp>


using namespace pyclustering;
using namespace pyclustering::utils::metric;


pyclustering_package * bsas_algorithm(const pyclustering_package * const p_sample,
                                      const std::size_t p_amount,
                                      const double p_threshold,
                                      const void * const p_metric)
{
    distance_metric<point> * metric = ((distance_metric<point> *) p_metric);
    distance_metric<point> default_metric = distance_metric_factory<point>::euclidean_square();

    if (!metric) {
        metric = &default_metric;
    }

    pyclustering::clst::bsas algorithm(p_amount, p_threshold, *metric);

    dataset input_dataset;
    p_sample->extract(input_dataset);

    pyclustering::clst::bsas_data output_result;
    algorithm.process(input_dataset, output_result);

    pyclustering_package * package = new pyclustering_package(pyclustering_data_t::PYCLUSTERING_TYPE_LIST);
    package->size = BSAS_PACKAGE_SIZE;
    package->data = new pyclustering_package * [BSAS_PACKAGE_SIZE];

    ((pyclustering_package **) package->data)[BSAS_PACKAGE_INDEX_CLUSTERS] = create_package(&output_result.clusters());
    ((pyclustering_package **) package->data)[BSAS_PACKAGE_INDEX_REPRESENTATIVES] = create_package(&output_result.representatives());

    return package;
}