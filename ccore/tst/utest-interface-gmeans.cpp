/*!

@authors Andrei Novikov (pyclustering@yandex.ru)
@date 2014-2020
@copyright BSD-3-Clause

*/


#include <gtest/gtest.h>

#include <pyclustering/interface/gmeans_interface.h>
#include <pyclustering/interface/pyclustering_interface.h>
#include <pyclustering/interface/pyclustering_package.hpp>

#include <pyclustering/cluster/gmeans.hpp>

#include "samples.hpp"
#include "utenv_utils.hpp"

#include <memory>


using namespace pyclustering;
using namespace pyclustering::clst;
using namespace pyclustering::utils::metric;


TEST(utest_interface_gmeans, gmeans_api) {
    std::shared_ptr<pyclustering_package> sample = pack(dataset({ { 1 }, { 2 }, { 3 }, { 10 }, { 11 }, { 12 } }));

    pyclustering_package * gmeans_result = gmeans_algorithm(sample.get(), 2, 0.001, 5, -1, RANDOM_STATE_CURRENT_TIME);
    ASSERT_NE(nullptr, gmeans_result);

    ASSERT_EQ(gmeans_result->size, GMEANS_PACKAGE_SIZE);
    delete gmeans_result;
}


TEST(utest_interface_gmeans, hepta_kmax_08) {
    auto data = fcps_sample_factory::create_sample(FCPS_SAMPLE::HEPTA);
    auto sample = pack(*data);

    pyclustering_package * gmeans_result = gmeans_algorithm(sample.get(), 1, 0.001, 3, 8, 1);
    ASSERT_NE(nullptr, gmeans_result);

    std::size_t amount_clusters = ((pyclustering_package **)gmeans_result->data)[GMEANS_PACKAGE_INDEX_CLUSTERS]->size;
    ASSERT_EQ(7ul, amount_clusters);

    free_pyclustering_package(gmeans_result);
}
