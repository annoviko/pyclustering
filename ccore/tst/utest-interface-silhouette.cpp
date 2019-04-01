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

#include "interface/silhouette_interface.h"
#include "interface/pyclustering_package.hpp"

#include "samples.hpp"

#include "utenv_utils.hpp"

#include <memory>


TEST(utest_interface_silhouette, silhouette_ksearch) {
    dataset_ptr data = simple_sample_factory::create_sample(SAMPLE_SIMPLE::SAMPLE_SIMPLE_01);
    std::shared_ptr<pyclustering_package> sample = pack(*data);

    pyclustering_package * result = silhouette_ksearch_algorithm(sample.get(), 2, 5, 0);

    ASSERT_EQ((std::size_t) SILHOUETTE_KSEARCH_PACKAGE_SIZE, result->size);

    delete result;
}
