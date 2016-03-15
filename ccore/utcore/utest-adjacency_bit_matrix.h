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

    ASSERT_EQ(10, matrix_first.size());
    ASSERT_EQ(10, matrix_second.size());
    ASSERT_EQ(false, matrix_first.has_connection(1, 2));
    ASSERT_EQ(false, matrix_first.has_connection(2, 3));
    ASSERT_EQ(true, matrix_first.has_connection(2, 1));
    ASSERT_EQ(true, matrix_first.has_connection(4, 7));
}


TEST(utest_adjacency_bit_matrix, move_matrix) {
    adjacency_bit_matrix matrix_first(40);
    adjacency_bit_matrix matrix_second(40);

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


TEST(utest_adjacency_bit_matrix, set_get_connection) {
    adjacency_bit_matrix matrix(100);

    for (size_t i = 0; i < matrix.size(); i++) {
        for (size_t j = i + 1; j < matrix.size(); j++) {
            ASSERT_EQ(false, matrix.has_connection(i, j));

            matrix.set_connection(i, j);

            ASSERT_EQ(true, matrix.has_connection(i, j));
            ASSERT_EQ(false, matrix.has_connection(j, i));

            matrix.set_connection(j, i);

            ASSERT_EQ(true, matrix.has_connection(j, i));
        }
    }
}


TEST(utest_adjacency_bit_matrix, erase_get_connection) {
    adjacency_bit_matrix matrix(20);

    for (size_t i = 0; i < matrix.size(); i++) {
        for (size_t j = i + 1; j < matrix.size(); j++) {
            matrix.set_connection(i, j);
            matrix.set_connection(j, i);
        }
    }

    for (size_t i = 0; i < matrix.size(); i++) {
        for (size_t j = i + 1; j < matrix.size(); j++) {
            ASSERT_EQ(true, matrix.has_connection(i, j));
            ASSERT_EQ(true, matrix.has_connection(j, i));

            matrix.erase_connection(i, j);

            ASSERT_EQ(false, matrix.has_connection(i, j));
            ASSERT_EQ(true, matrix.has_connection(j, i));

            matrix.erase_connection(j, i);

            ASSERT_EQ(false, matrix.has_connection(i, j));
            ASSERT_EQ(false, matrix.has_connection(j, i));
        }
    }
}


TEST(utest_adjacency_bit_matrix, get_neighbors_sizes) {
    adjacency_bit_matrix matrix(20);

    std::vector<size_t> node_neighbors;

    for (size_t i = 0; i < matrix.size(); i++) {
        for (size_t j = i + 1; j < matrix.size(); j++) {
            matrix.set_connection(i, j);
            matrix.set_connection(j, i);

            matrix.get_neighbors(i, node_neighbors);
            ASSERT_EQ(j, node_neighbors.size());

            matrix.get_neighbors(j, node_neighbors);
            ASSERT_EQ(i + 1, node_neighbors.size());
        }
    }
}


TEST(utest_adjacency_bit_matrix, get_neighbors_indexes) {
    adjacency_bit_matrix matrix(20);

    std::vector<size_t> node_neighbors;

    for (size_t i = 0; i < matrix.size(); i++) {
        for (size_t j = i + 1; j < matrix.size(); j++) {
            matrix.set_connection(i, j);
            matrix.set_connection(j, i);
        }
    }

    for (size_t i = 0; i < matrix.size(); i++) {
        matrix.get_neighbors(i, node_neighbors);
        ASSERT_EQ(matrix.size() - 1, node_neighbors.size());

        std::vector<bool> index_neighbor_checker(matrix.size(), false);
        for (size_t j = 0; j < node_neighbors.size(); j++) {
            size_t neighbor_index = node_neighbors[j];
            index_neighbor_checker[neighbor_index] = true;
        }

        for (size_t j = 0; j < node_neighbors.size(); j++) {
            if (i != j) {
                ASSERT_EQ(true, index_neighbor_checker[j]);
            }
            else {
                ASSERT_EQ(false, index_neighbor_checker[i]);
            }
        }
    }
}


#endif
