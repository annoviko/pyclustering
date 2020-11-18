/*!

@authors Andrei Novikov (pyclustering@yandex.ru)
@date 2014-2020
@copyright BSD-3-Clause

*/

#include <gtest/gtest.h>

#include <pyclustering/interface/dbscan_interface.h>
#include <pyclustering/interface/pyclustering_package.hpp>

#include "utenv_utils.hpp"

#include <memory>


using namespace pyclustering;


TEST(utest_interface_dbscan, dbscan_algorithm) {
    std::shared_ptr<pyclustering_package> sample = pack(dataset({ { 1.0, 1.0 }, { 1.1, 1.0 }, { 1.2, 1.4 }, { 10.0, 10.3 }, { 10.1, 10.2 }, { 10.2, 10.4 } }));

    pyclustering_package * result = dbscan_algorithm(sample.get(), 4, 2, 0);
    ASSERT_EQ(3U, result->size); /* allocated clustes + noise */

    delete result;
}