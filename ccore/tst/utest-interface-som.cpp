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

#include "interface/som_interface.h"
#include "interface/pyclustering_interface.h"
#include "interface/pyclustering_package.hpp"

#include "utenv_utils.hpp"

#include <memory>


using namespace ccore::nnet;


static void CHECK_FREE_PACKAGE(pyclustering_package * package, const std::size_t size = 0) {
    ASSERT_NE(nullptr, package);
    if (size > 0)
      ASSERT_EQ(size, package->size);
    else
      ASSERT_TRUE(package->size > 0);

    free_pyclustering_package(package);
}


TEST(utest_interface_som, som_api) {
    som_parameters params;

    void * network = som_create(1, 3, 0, &params);
    ASSERT_NE(nullptr, network);

    dataset input_data = { {1.0}, {1.2}, {1.3}, {3.2}, {3.5}, {3.2} };
    pyclustering_package * package_dataset = create_package(&input_data);
    size_t iterations = som_train(network, package_dataset, 100, true);
    ASSERT_LT(0U, iterations);
    free_pyclustering_package(package_dataset);

    pattern input_pattern = {2.3};
    pyclustering_package * package_pattern = create_package(&input_pattern);
    size_t index_winner = som_simulate(network, package_pattern);
    ASSERT_LE(0U, index_winner);
    ASSERT_GT(3U, index_winner);
    free_pyclustering_package(package_pattern);

    size_t amount_winners = som_get_winner_number(network);
    ASSERT_LE(0U, amount_winners);

    size_t network_size = som_get_size(network);
    ASSERT_EQ(3U, network_size);

    pyclustering_package * weights = som_get_weights(network);
    CHECK_FREE_PACKAGE(weights, 3);

    pyclustering_package * objects = som_get_capture_objects(network);
    CHECK_FREE_PACKAGE(objects, 3);

    pyclustering_package * awards = som_get_awards(network);
    CHECK_FREE_PACKAGE(awards, 3);

    pyclustering_package * neighbors = som_get_neighbors(network);
    CHECK_FREE_PACKAGE(neighbors, 3);

    som_destroy(network);
}