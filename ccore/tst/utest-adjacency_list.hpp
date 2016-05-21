/**
*
* Copyright (C) 2014-2016    Andrei Novikov (pyclustering@yandex.ru)
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

#ifndef _UTEST_ADJACENCY_LIST_H_
#define _UTEST_ADJACENCY_LIST_H_


#include "gtest/gtest.h"

#include "container/adjacency_list.hpp"

#include "utest-adjacency.hpp"

#include <cmath>
#include <utility>


using namespace container;


TEST(utest_adjacency_list, create_delete) {
    adjacency_list * matrix = new adjacency_list(10);
    ASSERT_EQ(10, matrix->size());

    for (size_t i = 0; i < matrix->size(); i++) {
        for (size_t j = i + 1; j < matrix->size(); j++) {
            ASSERT_EQ(false, matrix->has_connection(i, j));
        }
    }

    delete matrix;
}


TEST(utest_adjacency_list, null_size) {
    adjacency_list matrix(0);
    ASSERT_EQ(0, matrix.size());
}


TEST(utest_adjacency_list, create_clear) {
    adjacency_list matrix(10);
    ASSERT_EQ(10, matrix.size());

    matrix.clear();
    ASSERT_EQ(0, matrix.size());
}


TEST(utest_adjacency_list, copy_matrix) {
    adjacency_list matrix_first(20);
    adjacency_list matrix_second(10);

    ASSERT_EQ(20, matrix_first.size());
    ASSERT_EQ(10, matrix_second.size());

    matrix_first.set_connection(1, 2);
    matrix_first.set_connection(2, 3);

    matrix_second.set_connection(2, 1);
    matrix_second.set_connection(4, 7);

    matrix_first = matrix_second;

    ASSERT_EQ(10, matrix_first.size());
    ASSERT_EQ(10, matrix_second.size());
    ASSERT_EQ(false, matrix_first.has_connection(1, 2));
    ASSERT_EQ(false, matrix_first.has_connection(2, 3));
    ASSERT_EQ(true, matrix_first.has_connection(2, 1));
    ASSERT_EQ(true, matrix_first.has_connection(4, 7));
}


TEST(utest_adjacency_list, move_matrix) {
    adjacency_list matrix_first(40);
    adjacency_list matrix_second(40);

    ASSERT_TRUE(matrix_first.size() == matrix_second.size());
    ASSERT_EQ(40, matrix_first.size());
    ASSERT_EQ(40, matrix_second.size());

    for (size_t i = 0; i < matrix_first.size(); i++) {
        for (size_t j = i + 1; j < matrix_first.size(); j++) {
            if ((i % 2) == 0) {
                matrix_first.set_connection(i, j);
                ASSERT_EQ(true, matrix_first.has_connection(i, j));
                ASSERT_EQ(false, matrix_second.has_connection(i, j));
            }
            else {
                matrix_second.set_connection(i, j);
                ASSERT_EQ(false, matrix_first.has_connection(i, j));
                ASSERT_EQ(true, matrix_second.has_connection(i, j));
            }
        }
    }

    matrix_first = std::move(matrix_second);

    ASSERT_EQ(40, matrix_first.size());
    ASSERT_EQ(0, matrix_second.size());

    for (size_t i = 0; i < matrix_first.size(); i++) {
        for (size_t j = i + 1; j < matrix_first.size(); j++) {
            if ((i % 2) != 0) {
                ASSERT_EQ(true, matrix_first.has_connection(i, j));
            }
        }
    }
}


TEST(utest_adjacency_list, has_no_connection) {
	adjacency_list matrix(30);
	template_has_no_connection(matrix);
}


TEST(utest_adjacency_list, has_all_connection) {
	adjacency_list matrix(25);
	template_has_all_connection(matrix);
}


TEST(utest_adjacency_list, set_get_connection) {
    adjacency_list matrix(100);
	template_set_connection(matrix);
}


TEST(utest_adjacency_list, erase_get_connection) {
    adjacency_list matrix(20);
	template_erase_connection(matrix);
}


TEST(utest_adjacency_list, get_neighbors_sizes) {
    adjacency_list matrix(20);
	template_get_neighbors_sizes(matrix);
}


TEST(utest_adjacency_list, get_neighbors_indexes) {
    adjacency_list matrix(20);
	template_get_neighbors_indexes(matrix);
}


TEST(utest_adjacency_list, no_get_neighbors) {
	adjacency_list matrix(30);
	template_no_get_neighbors(matrix);
}


TEST(utest_adjacency_list, all_get_neighbors) {
	adjacency_list matrix(11);
	template_all_get_neighbors(matrix);
}


TEST(utest_adjacency_list, get_neighbors_after_erase) {
	adjacency_list matrix(17);
	template_get_neighbors_after_erase(matrix);
}


#endif
