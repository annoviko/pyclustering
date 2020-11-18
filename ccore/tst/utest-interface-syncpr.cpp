/*!

@authors Andrei Novikov (pyclustering@yandex.ru)
@date 2014-2020
@copyright BSD-3-Clause

*/


#include <gtest/gtest.h>

#include <pyclustering/interface/syncpr_interface.h>
#include <pyclustering/interface/pyclustering_interface.h>
#include <pyclustering/interface/pyclustering_package.hpp>

#include <pyclustering/nnet/syncpr.hpp>

#include "utenv_utils.hpp"


using namespace pyclustering;
using namespace pyclustering::nnet;


static void CHECK_FREE_PACKAGE(pyclustering_package * package) {
    ASSERT_NE(nullptr, package);
    ASSERT_TRUE(package->size > 0);

    free_pyclustering_package(package);
}

TEST(utest_interface_syncpr, syncpr_api) {
    void * network_pointer = syncpr_create(9, 5.0, 5.0);
    ASSERT_NE(nullptr, network_pointer);

    std::shared_ptr<pyclustering_package> patterns = pack(std::vector<syncpr_pattern>({ { 1, 1, -1, 1, 1, -1, 1, 1, -1 } }));
    syncpr_train(network_pointer, patterns.get());

    std::shared_ptr<pyclustering_package> pattern = pack(syncpr_pattern({ 1, 1, -1, 1, 1, -1, 1, 1, -1 }));
    void * dynamic1 = syncpr_simulate_static(network_pointer, 10, 10, pattern.get(), (unsigned) solve_type::FORWARD_EULER, true);
    ASSERT_NE(nullptr, dynamic1);

    void * dynamic2 = syncpr_simulate_dynamic(network_pointer, pattern.get(), 0.95, (unsigned) solve_type::FORWARD_EULER, true, 0.1);
    ASSERT_NE(nullptr, dynamic2);

    double memory_order = syncpr_memory_order(network_pointer, pattern.get());
    ASSERT_GT(memory_order, 0);

    pyclustering_package * package = syncpr_dynamic_allocate_sync_ensembles(dynamic1, 0.1);
    CHECK_FREE_PACKAGE(package);

    package = syncpr_dynamic_get_time(dynamic1);
    CHECK_FREE_PACKAGE(package);

    package = syncpr_dynamic_get_output(dynamic1);
    CHECK_FREE_PACKAGE(package);

    syncpr_destroy(network_pointer);
    syncpr_dynamic_destroy(dynamic1);
    syncpr_dynamic_destroy(dynamic2);
}