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
    using container_data_t = typename TypeContainer::value_type;
    pyclustering_package * package = create_package(&container);

    ASSERT_EQ(container.size(), package->size);

    if (package->type != PYCLUSTERING_TYPE_LIST) {
        for (std::size_t index = 0; index < container.size(); index++) {
            ASSERT_EQ(container[index], package->at<container_data_t>(index));
        }
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


TEST(utest_pyclustering, package_list) {
    std::vector<std::vector<int>> container = { { 1, 2 }, { 1, 2, 3, 4 } };
    template_pyclustering_package(container);
}


TEST(utest_pyclustering, package_pointer_list) {
    std::vector<std::vector<int> *> container;
    container.push_back(new std::vector<int>({ 1, 2, 3, 4, 5}));
    template_pyclustering_package(container);
    delete container[0];
}


template <class TypeContainer>
static void template_two_dimension_pyclustering_package(const TypeContainer & container) {
    using sub_container_t   = typename TypeContainer::value_type;
    using container_data_t  = typename sub_container_t::value_type;

    pyclustering_package * package = create_package(&container);

    ASSERT_EQ(container.size(), package->size);

    for (std::size_t i = 0; i < container.size(); i++) {
        pyclustering_package * sub_package = package->at<pyclustering_package *>(i);
        ASSERT_EQ(container[i].size(), sub_package->size);

        for (std::size_t j = 0; j < container[i].size(); j++) {
            ASSERT_EQ(container[i][j], package->at<container_data_t>(i, j));
        }
    }

    delete package;
}


TEST(utest_pyclustering, package_two_dimension_integer) {
    std::vector<std::vector<int>> container = { { 1, 2, 3 }, { 4, 5 }, { 6, 7, 8, 9 } };
    template_two_dimension_pyclustering_package(container);
}


TEST(utest_pyclustering, package_two_dimension_double) {
    std::vector<std::vector<double>> container = { { 1.0, 2.5, 3.0 }, { 4.5, 5.5 }, { 6.1, 7.2, 8.3, 9.4 } };
    template_two_dimension_pyclustering_package(container);
}


TEST(utest_pyclustering, package_two_dimension_empty) {
    std::vector<std::vector<long>> container = { { }, { 4, 5 }, { }, { 6 } };
    template_two_dimension_pyclustering_package(container);
}


template <class Container>
static void template_pack_unpack(const Container & container) {
    pyclustering_package * package = create_package(&container);

    Container unpack_container;
    package->extract(unpack_container);

    ASSERT_EQ(container, unpack_container);

    delete package;
}


TEST(utest_pyclustering, package_unpack_int) {
    template_pack_unpack(std::vector<int>({ 1, 2, 3, 4 }));
}


TEST(utest_pyclustering, package_unpack_long) {
    template_pack_unpack(std::vector<long>({ 1, 2, 3, 4, 5, 6 }));
}


TEST(utest_pyclustering, package_unpack_empty) {
    template_pack_unpack(std::vector<float>({ }));
}


TEST(utest_pyclustering, package_unpack_two_dimension) {
    template_pack_unpack(std::vector<std::vector<double>>({ { 1.2, 2.4 }, { 3.6, 4.8, 5.0 }, { 6.0 } }));
}