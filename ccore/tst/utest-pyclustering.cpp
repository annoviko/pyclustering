/**
*
* Copyright (C) 2014-2017    Andrei Novikov (pyclustering@yandex.ru)
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

#include "interface/pyclustering_package.hpp"

#include <vector>


template <class TypeContainer>
static void template_pyclustering_package(const TypeContainer & container) {
    pyclustering_package * package = create_package(&container);

    ASSERT_EQ(container.size(), package->size);
    for (std::size_t index = 0; index < container.size(); index++) {
        ASSERT_EQ(container[index], package->at<TypeContainer::value_type>(index));
    }

    delete package;
}


TEST(utest_pyclustering, package_integer) {
    std::vector<int> container = { 1, 2, 3, 4, 5 };
    template_pyclustering_package(container);
}


TEST(utest_pyclustering, package_double) {
    std::vector<double> container = { 1.0, 1.5, 2.0, 2.5, 3.0 };
    template_pyclustering_package(container);
}


TEST(utest_pyclustering, package_unsigned) {
    std::vector<unsigned int> container = { 1, 2, 3, 4, 5, 6, 7, 8, 9, 10 };
    template_pyclustering_package(container);
}


TEST(utest_pyclustering, package_float) {
    std::vector<float> container = { -1.0, -0.5, 0.0, 0.5, 1.0 };
    template_pyclustering_package(container);
}


TEST(utest_pyclustering, package_size_t) {
    std::vector<std::size_t> container = { 1, 2, 3, 4, 5, 6, 7 };
    template_pyclustering_package(container);
}


TEST(utest_pyclustering, package_empty) {
    std::vector<int> container = { };
    template_pyclustering_package(container);
}