/*!

@authors Andrei Novikov (pyclustering@yandex.ru)
@date 2014-2020
@copyright BSD-3-Clause

*/


#include <pyclustering/interface/bsas_interface.h>
#include <pyclustering/interface/ttsas_interface.h>

#include <pyclustering/cluster/ttsas.hpp>

#include <pyclustering/utils/metric.hpp>


using namespace pyclustering::utils::metric;


pyclustering_package * ttsas_algorithm(const pyclustering_package * const p_sample,
                                       const double p_threshold1,
                                       const double p_threshold2,
                                       const void * const p_metric)
{
    distance_metric<pyclustering::point> * metric = ((distance_metric<pyclustering::point> *) p_metric);
    distance_metric<pyclustering::point> default_metric = distance_metric_factory<pyclustering::point>::euclidean_square();

    if (!metric) {
        metric = &default_metric;
    }

    pyclustering::clst::ttsas algorithm(p_threshold1, p_threshold2, *metric);

    pyclustering::dataset input_dataset;
    p_sample->extract(input_dataset);

    pyclustering::clst::ttsas_data output_result;
    algorithm.process(input_dataset, output_result);

    pyclustering_package * package = new pyclustering_package(pyclustering_data_t::PYCLUSTERING_TYPE_LIST);
    package->size = BSAS_PACKAGE_SIZE;
    package->data = new pyclustering_package * [BSAS_PACKAGE_SIZE];

    ((pyclustering_package **) package->data)[BSAS_PACKAGE_INDEX_CLUSTERS] = create_package(&output_result.clusters());
    ((pyclustering_package **) package->data)[BSAS_PACKAGE_INDEX_REPRESENTATIVES] = create_package(&output_result.representatives());

    return package;
}