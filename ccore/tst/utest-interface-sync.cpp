/**
*
* Copyright (C) 2014-2018    Andrei Novikov (pyclustering@yandex.ru)
*
* GNU_PUBLIC_LICENSE
*   pyclustering is free software: you can redistribute it and/or modify
*   it under the terms of the GNU General Public License as published by
*   the Free Software Foundation, either version 3 of the License, or
*   (at your option) any later version.
*
*   pyclustering is distributed in the hope that it will be useful,
*   but WITHOUT ANY WARRANTY; without even the implied warranty of
*   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
*   GNU General Public License for more details.
*
*   You should have received a copy of the GNU General Public License
*   along with this program.  If not, see <http://www.gnu.org/licenses/>.
*
*/


#include "gtest/gtest.h"

#include "interface/sync_interface.h"
#include "interface/pyclustering_interface.h"
#include "interface/pyclustering_package.hpp"

#include "nnet/sync.hpp"

#include "utenv_utils.hpp"


using namespace ccore::nnet;


static void CHECK_FREE_PACKAGE(pyclustering_package * package, const std::size_t size = 0) {
    ASSERT_NE(nullptr, package);
    if (size > 0)
      ASSERT_EQ(size, package->size);
    else
      ASSERT_TRUE(package->size > 0);

    free_pyclustering_package(package);
}


TEST(utest_interface_sync, sync_api) {
    void * network_pointer = sync_create_network(10, 1, 0, (unsigned int) connection_t::CONNECTION_ALL_TO_ALL, (unsigned int) initial_type::EQUIPARTITION);
    ASSERT_NE(nullptr, network_pointer);

    std::size_t network_size = sync_get_size(network_pointer);
    ASSERT_EQ(10U, network_size);

    void * dynamic_pointer = sync_simulate_static(network_pointer, 20, 10, (unsigned int) solve_type::FORWARD_EULER, true);
    ASSERT_NE(nullptr, dynamic_pointer);

    void * dynamic_flexi_pointer = sync_simulate_dynamic(network_pointer, 0.99, (unsigned int) solve_type::FORWARD_EULER, true, 0.1, 0.01, 0.01);
    ASSERT_GT(sync_dynamic_get_size(dynamic_flexi_pointer), 0U);
    sync_dynamic_destroy(dynamic_flexi_pointer);

    double order_parameter = sync_order(network_pointer);
    ASSERT_LT(0.9, order_parameter);

    double local_order_parameter = sync_local_order(network_pointer);
    ASSERT_LT(0.9, local_order_parameter);

    std::size_t dynamic_size = sync_dynamic_get_size(dynamic_pointer);
    ASSERT_EQ(21U, dynamic_size);

    pyclustering_package * package = sync_connectivity_matrix(network_pointer);
    CHECK_FREE_PACKAGE(package, 10);

    package = sync_dynamic_allocate_sync_ensembles(dynamic_pointer, 0.01, dynamic_size - 1);
    CHECK_FREE_PACKAGE(package, 1);

    package = sync_dynamic_allocate_correlation_matrix(dynamic_pointer, dynamic_size - 1);
    CHECK_FREE_PACKAGE(package, 10);

    package = sync_dynamic_get_time(dynamic_pointer);
    CHECK_FREE_PACKAGE(package, 21);

    package = sync_dynamic_get_output(dynamic_pointer);
    CHECK_FREE_PACKAGE(package, 21);

    package = sync_dynamic_calculate_order(dynamic_pointer, 0, dynamic_size);
    CHECK_FREE_PACKAGE(package, dynamic_size);

    package = sync_dynamic_calculate_local_order(dynamic_pointer, network_pointer, 0, dynamic_size);
    CHECK_FREE_PACKAGE(package, dynamic_size);

    sync_dynamic_destroy(dynamic_pointer);
    sync_destroy_network(network_pointer);
}