/*!

@authors Andrei Novikov (pyclustering@yandex.ru)
@date 2014-2020
@copyright BSD-3-Clause

*/

#include <gtest/gtest.h>

#include <pyclustering/interface/cure_interface.h>
#include <pyclustering/interface/pyclustering_package.hpp>

#include "samples.hpp"
#include "utenv_utils.hpp"
#include "utenv_check.hpp"

#include <memory>


using namespace pyclustering;


TEST(utest_interface_cure, cure_api) {
    std::shared_ptr<pyclustering_package> sample = pack(dataset({ { 1 }, { 2 }, { 3 }, { 10 }, { 11 }, { 12 } }));

    void * cure_result = cure_algorithm(sample.get(), 2, 1, 0.5);
    ASSERT_NE(nullptr, cure_result);

    std::shared_ptr<pyclustering_package> clusters(cure_get_clusters(cure_result));
    ASSERT_EQ(2U, clusters->size);

    std::shared_ptr<pyclustering_package> representors(cure_get_representors(cure_result));
    ASSERT_EQ(2U, representors->size);

    std::shared_ptr<pyclustering_package> means(cure_get_means(cure_result));
    ASSERT_EQ(2U, means->size);

    cure_data_destroy(cure_result);
}


TEST(utest_interface_cure, cure_api_long_result) {
    auto sample_sptr = fcps_sample_factory::create_sample(FCPS_SAMPLE::HEPTA);
    std::shared_ptr<pyclustering_package> sample = pack(*sample_sptr);

    void * cure_result = cure_algorithm(sample.get(), 7, 1, 0.3);
    ASSERT_NE(nullptr, cure_result);

    std::shared_ptr<pyclustering_package> clusters(cure_get_clusters(cure_result));
    ASSERT_EQ(7U, clusters->size);

    std::shared_ptr<pyclustering_package> representors(cure_get_representors(cure_result));
    ASSERT_EQ(7U, representors->size);

    std::shared_ptr<pyclustering_package> means(cure_get_means(cure_result));
    ASSERT_EQ(7U, means->size);

    cure_data_destroy(cure_result);
}