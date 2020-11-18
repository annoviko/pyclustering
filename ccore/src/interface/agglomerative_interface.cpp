/*

@authors Andrei Novikov (pyclustering@yandex.ru)
@date 2014-2020
@copyright BSD-3-Clause

*/


#include <pyclustering/interface/agglomerative_interface.h>

#include <pyclustering/cluster/agglomerative.hpp>


pyclustering_package * agglomerative_algorithm(const pyclustering_package * const p_sample, const std::size_t p_number_clusters, const std::size_t p_link) {
    pyclustering::clst::agglomerative algorithm(p_number_clusters, (pyclustering::clst::agglomerative::type_link) p_link);

    pyclustering::dataset data;
    p_sample->extract(data);

    pyclustering::clst::agglomerative_data result;
    algorithm.process(data, result);

    pyclustering_package * package = create_package(&result.clusters());

    return package;
} 
