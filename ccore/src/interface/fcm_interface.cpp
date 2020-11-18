/*!

@authors Andrei Novikov (pyclustering@yandex.ru)
@date 2014-2020
@copyright BSD-3-Clause

*/


#include <pyclustering/interface/fcm_interface.h>

#include <pyclustering/cluster/fcm.hpp>


pyclustering_package * fcm_algorithm(const pyclustering_package * const p_sample, 
                                     const pyclustering_package * const p_centers, 
                                     const double p_m,
                                     const double p_tolerance,
                                     const std::size_t p_itermax)
{
    pyclustering::dataset data, centers;

    p_sample->extract(data);
    p_centers->extract(centers);

    pyclustering::clst::fcm algorithm(centers, p_m, p_tolerance, p_itermax);

    pyclustering::clst::fcm_data output_result;
    algorithm.process(data, output_result);

    pyclustering_package * package = create_package_container(FCM_PACKAGE_SIZE);
    ((pyclustering_package **) package->data)[FCM_PACKAGE_INDEX_CLUSTERS] = create_package(&output_result.clusters());
    ((pyclustering_package **) package->data)[FCM_PACKAGE_INDEX_CENTERS] = create_package(&output_result.centers());
    ((pyclustering_package **) package->data)[FCM_PACKAGE_INDEX_MEMBERSHIP] = create_package(&output_result.membership());

    return package;
}