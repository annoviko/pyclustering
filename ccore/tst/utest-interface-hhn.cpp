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

#include "interface/hhn_interface.h"
#include "interface/pyclustering_interface.h"
#include "interface/pyclustering_package.hpp"

#include "nnet/hhn.hpp"

#include "utenv_utils.hpp"


using namespace ccore::nnet;


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
