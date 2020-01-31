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

#include <pyclustering/interface/fcm_interface.h>
#include <pyclustering/interface/pyclustering_package.hpp>

#include "samples.hpp"
#include "utenv_utils.hpp"


using namespace pyclustering;


TEST(utest_interface_fcm, fcm_api) {
    dataset_ptr data = simple_sample_factory::create_sample(SAMPLE_SIMPLE::SAMPLE_SIMPLE_01);
    std::shared_ptr<pyclustering_package> sample = pack(*data);
    std::shared_ptr<pyclustering_package> centers = pack(dataset({ { 3.7, 5.5 },{ 6.7, 7.5 } }));

    pyclustering_package * fcm_result = fcm_algorithm(sample.get(), centers.get(), 2.0, 0.001, 200);
    ASSERT_NE(nullptr, fcm_result);
    ASSERT_EQ(fcm_package_indexer::FCM_PACKAGE_SIZE, fcm_result->size);

    delete fcm_result;
    fcm_result = nullptr;
}