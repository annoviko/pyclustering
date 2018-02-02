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

#include "interface/legion_interface.h"
#include "interface/pyclustering_interface.h"
#include "interface/pyclustering_package.hpp"

#include "nnet/legion.hpp"

#include "utenv_utils.hpp"


using namespace ccore::nnet;


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