/*!

@authors Andrei Novikov (pyclustering@yandex.ru)
@date 2014-2020
@copyright BSD-3-Clause

*/

#include <pyclustering/interface/gmeans_interface.h>

#include <pyclustering/cluster/gmeans.hpp>


pyclustering_package * gmeans_algorithm(const pyclustering_package * const p_sample, 
                                        const std::size_t p_amount, 
                                        const double p_tolerance,
                                        const std::size_t p_repeat,
                                        const long long p_kmax,
                                        const long long p_random_state)
{
    pyclustering::dataset data;
    p_sample->extract(data);

    pyclustering::clst::gmeans algorithm(p_amount, p_tolerance, p_repeat, p_kmax, p_random_state);

    pyclustering::clst::gmeans_data output_result;
    algorithm.process(data, output_result);

    std::vector<double> wce_storage(1, output_result.wce());

    pyclustering_package * package = create_package_container(GMEANS_PACKAGE_SIZE);
    ((pyclustering_package **) package->data)[GMEANS_PACKAGE_INDEX_CLUSTERS] = create_package(&output_result.clusters());
    ((pyclustering_package **) package->data)[GMEANS_PACKAGE_INDEX_CENTERS] = create_package(&output_result.centers());
    ((pyclustering_package **) package->data)[GMEANS_PACKAGE_INDEX_WCE] = create_package(&wce_storage);

    return package;
}
