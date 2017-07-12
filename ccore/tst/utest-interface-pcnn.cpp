/**
*
* Copyright (C) 2014-2017    Andrei Novikov (pyclustering@yandex.ru)
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

#include "interface/pcnn_interface.h"
#include "interface/pyclustering_interface.h"
#include "interface/pyclustering_package.hpp"

#include "utenv-utils.hpp"


static void CHECK_FREE_PACKAGE(pyclustering_package * package) {
    ASSERT_NE(nullptr, package);
    ASSERT_TRUE(package->size > 0);

    free_pyclustering_package(package);
}


TEST(utest_interface_pcnn, pcnn_api) {
    std::shared_ptr<pyclustering_package> stimulus = pack(pcnn_stimulus({ 1, 0, 1, 1, 0, 1, 1, 1, 1, 1 }));
    pcnn_parameters parameters;

    void * pcnn_network = pcnn_create(10, (unsigned int) connection_t::CONNECTION_ALL_TO_ALL, 0, 0, (void *) &parameters);
    ASSERT_NE(nullptr, pcnn_network);

    void * dynamic = pcnn_simulate(pcnn_network, 10, stimulus.get());
    ASSERT_NE(nullptr, dynamic);

    std::size_t size_network = pcnn_get_size(pcnn_network);
    ASSERT_EQ(10, size_network);

    pyclustering_package * package = pcnn_dynamic_allocate_sync_ensembles(dynamic);
    CHECK_FREE_PACKAGE(package);

    package = pcnn_dynamic_allocate_spike_ensembles(dynamic);
    CHECK_FREE_PACKAGE(package);

    package = pcnn_dynamic_allocate_time_signal(dynamic);
    CHECK_FREE_PACKAGE(package);

    package = pcnn_dynamic_get_output(dynamic);
    CHECK_FREE_PACKAGE(package);

    package = pcnn_dynamic_get_time(dynamic);
    CHECK_FREE_PACKAGE(package);

    std::size_t size_dynamic = pcnn_dynamic_get_size(dynamic);
    ASSERT_GT(size_dynamic, 0);

    pcnn_dynamic_destroy(dynamic);
    pcnn_destroy(pcnn_network);
}
