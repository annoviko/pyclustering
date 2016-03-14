#ifndef _UTEST_ADJACENCY_BIT_MATRIX_H_
#define _UTEST_ADJACENCY_BIT_MATRIX_H_

#include "ccore/adjacency_bit_matrix.h"

#include "gtest/gtest.h"

#include <cmath>
#include <utility>


TEST(utest_adjacency_bit_matrix, create_delete) {
    adjacency_bit_matrix * matrix = new adjacency_bit_matrix(10);
    ASSERT_EQ(10, matrix->size());

    for (size_t i = 0; i < matrix->size(); i++) {
        for (size_t j = i + 1; j < matrix->size(); j++) {
            ASSERT_EQ(false, matrix->has_connection(i, j));
        }
    }

    delete matrix;
}


TEST(utest_adjacency_bit_matrix, copy_matrix) {
    adjacency_bit_matrix matrix_first(20);
    adjacency_bit_matrix matrix_second(10);

    ASSERT_EQ(20, matrix_first.size());
    ASSERT_EQ(10, matrix_second.size());

    matrix_first.set_connection(1, 2);
    matrix_first.set_connection(2, 3);

    matrix_second.set_connection(2, 1);
    matrix_second.set_connection(4, 7);

    matrix_first = matrix_second;

    ASSERT_EQ(20, matrix_first.size());
    ASSERT_EQ(20, matrix_second.size());
    ASSERT_EQ(false, matrix_first.has_connection(1, 2));
    ASSERT_EQ(false, matrix_first.has_connection(2, 3));
    ASSERT_EQ(true, matrix_first.has_connection(2, 1));
    ASSERT_EQ(true, matrix_first.has_connection(4, 7));
}


TEST(utest_adjacency_bit_matrix, move_matrix) {
    adjacency_bit_matrix matrix_first(40);
    adjacency_bit_matrix matrix_second(40);

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
                ASSERT_EQ(false, matrix_second.has_connection(i, j));
            }
        }
    }
}


#endif
