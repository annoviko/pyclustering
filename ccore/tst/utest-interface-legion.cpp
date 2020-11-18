/*!

@authors Andrei Novikov (pyclustering@yandex.ru)
@date 2014-2020
@copyright BSD-3-Clause

*/

#include <gtest/gtest.h>

#include <pyclustering/interface/legion_interface.h>
#include <pyclustering/interface/pyclustering_interface.h>
#include <pyclustering/interface/pyclustering_package.hpp>

#include <pyclustering/nnet/legion.hpp>

#include "utenv_utils.hpp"


using namespace pyclustering::nnet;


static void CHECK_FREE_PACKAGE(pyclustering_package * package) {
    ASSERT_NE(nullptr, package);
    ASSERT_TRUE(package->size > 0);

    free_pyclustering_package(package);
}


TEST(utest_interface_legion, legion_api) {
    std::shared_ptr<pyclustering_package> stimulus = pack(legion_stimulus({ 1, 0, 1, 1, 0, 1, 1, 1, 1, 1 }));
    legion_parameters parameters;

    void * legion_network = legion_create(10, (unsigned int) connection_t::CONNECTION_ALL_TO_ALL, (void *) &parameters);
    ASSERT_NE(nullptr, legion_network);

    void * dynamic = legion_simulate(legion_network, 10, 10, (unsigned) solve_type::RUNGE_KUTTA_4, true, stimulus.get());
    ASSERT_NE(nullptr, dynamic);

    std::size_t size_network = legion_get_size(legion_network);
    ASSERT_EQ(10U, size_network);

    pyclustering_package * package = legion_dynamic_get_output(dynamic);
    CHECK_FREE_PACKAGE(package);

    package = legion_dynamic_get_inhibitory_output(dynamic);
    CHECK_FREE_PACKAGE(package);

    package = legion_dynamic_get_time(dynamic);
    CHECK_FREE_PACKAGE(package);

    std::size_t size_dynamic = legion_dynamic_get_size(dynamic);
    ASSERT_GT(size_dynamic, 0U);

    legion_dynamic_destroy(dynamic);
    legion_destroy(legion_network);
}