/**
*
* @authors Andrei Novikov (pyclustering@yandex.ru)
* @date 2014-2019
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


#include "gtest/gtest.h"

#include "interface/elbow_interface.h"
#include "interface/pyclustering_package.hpp"

#include "samples.hpp"

#include "utenv_utils.hpp"

#include <memory>


TEST(utest_interface_elbow, elbow_method) {
    std::shared_ptr<pyclustering_package> sample = pack(dataset({ { 1.0, 1.0 }, { 1.1, 1.0 }, { 1.2, 1.4 }, { 10.0, 10.3 }, { 10.1, 10.2 }, { 10.2, 10.4 } }));

    pyclustering_package * result = elbow_method_ikpp(sample.get(), 1, sample->size);
    ASSERT_EQ((std::size_t) ELBOW_PACKAGE_SIZE, result->size);

    delete result;

    result = elbow_method_irnd(sample.get(), 1, sample->size);
    ASSERT_EQ((std::size_t) ELBOW_PACKAGE_SIZE, result->size);

    delete result;
}


TEST(utest_interface_elbow, elbow_method_simple3_ikpp) {
    auto sample_ptr = simple_sample_factory::create_sample(SAMPLE_SIMPLE::SAMPLE_SIMPLE_03);
    std::shared_ptr<pyclustering_package> sample = pack(*sample_ptr);

    pyclustering_package * result = elbow_method_ikpp(sample.get(), 1, 10);
    ASSERT_EQ((std::size_t) ELBOW_PACKAGE_SIZE, result->size);

    delete result;
}


TEST(utest_interface_elbow, elbow_method_simple3_irnd) {
    auto sample_ptr = simple_sample_factory::create_sample(SAMPLE_SIMPLE::SAMPLE_SIMPLE_03);
    std::shared_ptr<pyclustering_package> sample = pack(*sample_ptr);

    pyclustering_package * result = elbow_method_irnd(sample.get(), 1, 10);
    ASSERT_EQ((std::size_t) ELBOW_PACKAGE_SIZE, result->size);

    delete result;
}