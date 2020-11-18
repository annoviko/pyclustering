/*!

@authors Andrei Novikov (pyclustering@yandex.ru)
@date 2014-2020
@copyright BSD-3-Clause

*/

#include <gtest/gtest.h>

#include <pyclustering/interface/agglomerative_interface.h>
#include <pyclustering/interface/pyclustering_package.hpp>

#include "utenv_utils.hpp"

#include <memory>


using namespace pyclustering;


TEST(utest_interface_agglomerative, agglomerative_api) {
    std::shared_ptr<pyclustering_package> sample = pack(dataset({ { 1 }, { 2 }, { 3 }, { 10 }, { 11 }, { 12 } }));

    pyclustering_package * agglomerative_result = agglomerative_algorithm(sample.get(), 2, 0);
    ASSERT_NE(nullptr, agglomerative_result);

    delete agglomerative_result;
}