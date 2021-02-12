/*!

@authors Andrei Novikov (pyclustering@yandex.ru)
@date 2014-2020
@copyright BSD-3-Clause

*/

#include <pyclustering/interface/pam_build_interface.h>

#include <pyclustering/cluster/pam_build.hpp>

#include <pyclustering/utils/metric.hpp>


using namespace pyclustering::utils::metric;


pyclustering_package * pam_build_algorithm(const pyclustering_package * const p_sample,
                                           const std::size_t p_amount,
                                           const void * const p_metric,
                                           const std::size_t p_data_type)
try {
    distance_metric<pyclustering::point> * metric = ((distance_metric<pyclustering::point> *) p_metric);
    distance_metric<pyclustering::point> default_metric = distance_metric_factory<pyclustering::point>::euclidean_square();

    if (!metric) {
        metric = &default_metric;
    }

    pyclustering::dataset input_dataset;
    p_sample->extract(input_dataset);

    std::vector<std::size_t> initial_medoids;
    pyclustering::clst::pam_build(p_amount, *metric).initialize(input_dataset, static_cast<pyclustering::clst::data_t>(p_data_type), initial_medoids);

    pyclustering_package * package = create_package_container(PAM_BUILD_PACKAGE_SIZE);
    ((pyclustering_package **)package->data)[PAM_BUILD_PACKAGE_INDEX_MEDOIDS] = create_package(&initial_medoids);

    return package;
}
catch (std::exception & p_exception) {
    return create_package(p_exception.what());
}