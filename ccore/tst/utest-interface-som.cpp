/*!

@authors Andrei Novikov (pyclustering@yandex.ru)
@date 2014-2020
@copyright BSD-3-Clause

*/

#include <gtest/gtest.h>

#include <pyclustering/interface/som_interface.h>
#include <pyclustering/interface/pyclustering_interface.h>
#include <pyclustering/interface/pyclustering_package.hpp>

#include "utenv_utils.hpp"

#include <memory>


using namespace pyclustering;
using namespace pyclustering::nnet;


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

    /* get network dump and upload it again */
    weights = som_get_weights(network);
    awards = som_get_awards(network);
    objects = som_get_capture_objects(network);

    som_load(network, weights, awards, objects);

    CHECK_FREE_PACKAGE(weights, 3);
    CHECK_FREE_PACKAGE(awards, 3);
    CHECK_FREE_PACKAGE(objects, 3);

    /* destroy network */
    som_destroy(network);
}