/*!

@authors Andrei Novikov (pyclustering@yandex.ru)
@date 2014-2020
@copyright BSD-3-Clause

*/

#include <gtest/gtest.h>

#include <pyclustering/interface/hhn_interface.h>
#include <pyclustering/interface/pyclustering_interface.h>
#include <pyclustering/interface/pyclustering_package.hpp>

#include <pyclustering/nnet/hhn.hpp>

#include "utenv_utils.hpp"


using namespace pyclustering::nnet;


static void CHECK_FREE_PACKAGE(pyclustering_package * package) {
    ASSERT_NE(nullptr, package);
    ASSERT_TRUE(package->size > 0);

    free_pyclustering_package(package);
}


TEST(utest_interface_hhn, hhn_api) {
    std::shared_ptr<pyclustering_package> stimulus = pack(hhn_stimulus({ 20, 20, 30, 30, 40, 40 }));
    hnn_parameters parameters;

    void * network = hhn_create(6, &parameters);
    ASSERT_NE(nullptr, network);

    void * dynamic = hhn_dynamic_create(true, false, false, true);
    ASSERT_NE(nullptr, dynamic);

    hhn_simulate(network, 10, 1.0, 1, stimulus.get(), dynamic);
    ASSERT_EQ(11U, ((hhn_dynamic *) dynamic)->size_dynamic());
    ASSERT_EQ(6U, ((hhn_dynamic *) dynamic)->size_network());

    pyclustering_package * package = hhn_dynamic_get_central_evolution(dynamic, 0);
    CHECK_FREE_PACKAGE(package);

    package = hhn_dynamic_get_peripheral_evolution(dynamic, 0);
    CHECK_FREE_PACKAGE(package);

    package = hhn_dynamic_get_time(dynamic);
    CHECK_FREE_PACKAGE(package);

    hhn_dynamic_write(dynamic, "test_hhn_dynamic.txt");
    void * dynamic_copy = hhn_dynamic_read("test_hhn_dynamic.txt");
    ASSERT_NE(nullptr, dynamic_copy);

    hhn_dynamic_destroy(dynamic);
    hhn_dynamic_destroy(dynamic_copy);

    hhn_destroy(network);
}
