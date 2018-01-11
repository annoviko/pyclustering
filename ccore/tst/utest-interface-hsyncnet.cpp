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
#include "interface/hsyncnet_interface.h"
#include "interface/pyclustering_interface.h"
#include "interface/pyclustering_package.hpp"

#include "cluster/hsyncnet.hpp"

#include "utenv_utils.hpp"


static void CHECK_FREE_PACKAGE(pyclustering_package * package) {
    ASSERT_NE(nullptr, package);
    ASSERT_TRUE(package->size > 0);

    free_pyclustering_package(package);
}

TEST(utest_interface_hsyncnet, hsyncnet_api) {
    std::shared_ptr<pyclustering_package> sample = pack(dataset({ { 1 }, { 2 }, { 3 }, { 10 }, { 11 }, { 12 } }));
    void * network_pointer = hsyncnet_create_network(sample.get(), 3, (unsigned int) initial_type::EQUIPARTITION, 3, 0.1);
    ASSERT_NE(nullptr, network_pointer);

    void * analyser_pointer = hsyncnet_process(network_pointer, 0.995, (unsigned int) solve_type::FORWARD_EULER, true);
    ASSERT_NE(nullptr, analyser_pointer);

    pyclustering_package * package = sync_dynamic_allocate_sync_ensembles(analyser_pointer, 0.1, sync_dynamic_get_size(analyser_pointer) - 1);
    CHECK_FREE_PACKAGE(package);

    package = sync_dynamic_allocate_correlation_matrix(analyser_pointer, sync_dynamic_get_size(analyser_pointer) - 1);
    CHECK_FREE_PACKAGE(package);

    package = sync_dynamic_get_time(analyser_pointer);
    CHECK_FREE_PACKAGE(package);

    package = sync_dynamic_get_output(analyser_pointer);
    CHECK_FREE_PACKAGE(package);

    hsyncnet_destroy_network(network_pointer);
    hsyncnet_analyser_destroy(analyser_pointer);
}