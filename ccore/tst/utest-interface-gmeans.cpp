/**
*
* @authors Andrei Novikov (pyclustering@yandex.ru)
* @date 2014-2020
* @copyright GNU Public License
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


#include <gtest/gtest.h>

#include <pyclustering/interface/gmeans_interface.h>
#include <pyclustering/interface/pyclustering_interface.h>
#include <pyclustering/interface/pyclustering_package.hpp>

#include <pyclustering/cluster/gmeans.hpp>

#include "samples.hpp"
#include "utenv_utils.hpp"

#include <memory>


using namespace pyclustering;
using namespace pyclustering::clst;
using namespace pyclustering::utils::metric;


TEST(utest_interface_gmeans, gmeans_api) {
    std::shared_ptr<pyclustering_package> sample = pack(dataset({ { 1 }, { 2 }, { 3 }, { 10 }, { 11 }, { 12 } }));

    pyclustering_package * gmeans_result = gmeans_algorithm(sample.get(), 2, 0.001, 5, -1, RANDOM_STATE_CURRENT_TIME);
    ASSERT_NE(nullptr, gmeans_result);

    ASSERT_EQ(gmeans_result->size, GMEANS_PACKAGE_SIZE);
    delete gmeans_result;
}


TEST(utest_interface_gmeans, hepta_kmax_08) {
    auto data = fcps_sample_factory::create_sample(FCPS_SAMPLE::HEPTA);
    auto sample = pack(*data);

    pyclustering_package * gmeans_result = gmeans_algorithm(sample.get(), 1, 0.001, 3, 8, 1);
    ASSERT_NE(nullptr, gmeans_result);

    std::size_t amount_clusters = ((pyclustering_package **)gmeans_result->data)[GMEANS_PACKAGE_INDEX_CLUSTERS]->size;
    ASSERT_EQ(7ul, amount_clusters);

    free_pyclustering_package(gmeans_result);
}
