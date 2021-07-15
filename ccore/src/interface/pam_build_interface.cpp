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


boost::python::list pam_build_algorithm_2(const boost::python::list & p_sample, const std::size_t p_amount, const void * const p_metric, const std::size_t p_data_type) {
    distance_metric<pyclustering::point> * metric = ((distance_metric<pyclustering::point> *) p_metric);
    distance_metric<pyclustering::point> default_metric = distance_metric_factory<pyclustering::point>::euclidean_square();


    if (!metric) {
        metric = &default_metric;
    }

    /* copy-paste */
    pyclustering::dataset input_dataset;

    std::size_t length_data = boost::python::len(p_sample);
    std::size_t length_point = boost::python::len(p_sample[0]);
    input_dataset.reserve(length_data);

    for (std::size_t i = 0; i < length_data; i++) {
        pyclustering::point point;
        for (std::size_t j = 0; j < length_point; j++) {
            point.push_back(boost::python::extract<double>(p_sample[i][j]));
        }

        input_dataset.push_back(std::move(point));
    }

    std::vector<std::size_t> initial_medoids;
    pyclustering::clst::pam_build(p_amount, *metric).initialize(input_dataset, static_cast<pyclustering::clst::data_t>(p_data_type), initial_medoids);

    /* copy paste results */
    boost::python::list result;
    for (std::size_t i = 0; i < initial_medoids.size(); i++) {
        result.append(initial_medoids[i]);
    }

    return result;
}