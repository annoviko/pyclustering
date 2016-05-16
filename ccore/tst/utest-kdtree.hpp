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

#ifndef _UTEST_KDTREE_
#define _UTEST_KDTREE_


#include "gtest/gtest.h"

#include "container/kdtree.hpp"

#include <algorithm>


class utest_kdtree : public ::testing::Test {
protected:
	typedef std::vector< std::vector<double> * >::iterator			iterator_point;
	typedef std::vector< std::vector<double> * >::const_iterator	const_iterator_point;

	virtual void SetUp() { 
		tree = new kdtree(); 
	}

	virtual void TearDown() { 
		delete tree;
	}

	virtual void InitTestObject(std::vector< std::vector<double> * > * points) {
		delete tree;
		tree = new kdtree(points, NULL);
	}

	static std::vector< std::vector<double> * > * GeneratePoints(double * pointer_points, unsigned int dimension, unsigned int number) {
		unsigned int cursor = 0;
		std::vector< std::vector<double> * > * points = new std::vector< std::vector<double> * >();
		for (unsigned int index_point = 0; index_point < number; index_point++) {
			std::vector<double> * single_point = new std::vector<double>(dimension, 0);

			for (unsigned int index_dimension = 0; index_dimension < dimension; index_dimension++) {
				(*single_point)[index_dimension] = pointer_points[cursor];
				cursor++;
			}

			points->push_back(single_point);
		}

		return points;
	}

	static std::vector<double> * CreatePoint(double * pointer_point, unsigned int dimension) {
		std::vector<double> * single_point = new std::vector<double>(dimension, 0);
		for (unsigned int index_dimension = 0; index_dimension < dimension; index_dimension++) {
			(*single_point)[index_dimension] = pointer_point[index_dimension];
		}

		return single_point;
	}

	static void DestroyPoints(std::vector< std::vector<double> * > * points) {
		for (std::vector< std::vector<double> * >::iterator iter = points->begin(); iter != points->end(); iter++) { delete *iter; }
		delete points;
	}

protected:
	kdtree * tree;
};


TEST_F(utest_kdtree, creation_without_payload) {
	double test_sample_point[7][2] = { {4, 3}, {3, 4}, {5, 8}, {3, 3}, {3, 9}, {6, 4}, {5, 9} };
	std::vector< std::vector<double> * > * test_sample_point_vector = GeneratePoints((double *) &test_sample_point, 2, 7);

	InitTestObject(test_sample_point_vector);

	for (const_iterator_point point = test_sample_point_vector->begin(); point != test_sample_point_vector->end(); point++) {
		kdnode * node = tree->find_node(*point);

		ASSERT_TRUE(node != NULL);
		ASSERT_EQ(NULL, node->get_payload());
		ASSERT_EQ(*point, node->get_data());
	}

	DestroyPoints(test_sample_point_vector);
}

TEST_F(utest_kdtree, parent_node) {
	double test_sample_point[7][2] = { {4, 3}, {3, 4}, {5, 8}, {3, 3}, {3, 9}, {6, 4}, {5, 9} };
	std::vector< std::vector<double> * > * test_sample_point_vector = GeneratePoints((double *) &test_sample_point, 2, 7);

	InitTestObject(test_sample_point_vector);

	kdnode * node = tree->find_node( (*test_sample_point_vector)[0] );
	ASSERT_EQ(NULL, node->get_parent());

	node = tree->find_node( (*test_sample_point_vector)[1] );
	ASSERT_EQ((*test_sample_point_vector)[0], node->get_parent()->get_data());

	node = tree->find_node( (*test_sample_point_vector)[2] );
	ASSERT_EQ((*test_sample_point_vector)[0], node->get_parent()->get_data());

	node = tree->find_node( (*test_sample_point_vector)[5] );
	ASSERT_EQ((*test_sample_point_vector)[2], node->get_parent()->get_data());

	node = tree->find_node( (*test_sample_point_vector)[3] );
	ASSERT_EQ((*test_sample_point_vector)[1], node->get_parent()->get_data());

	node = tree->find_node( (*test_sample_point_vector)[6] );
	ASSERT_EQ((*test_sample_point_vector)[2], node->get_parent()->get_data());

	node = tree->find_node( (*test_sample_point_vector)[4] );
	ASSERT_EQ((*test_sample_point_vector)[1], node->get_parent()->get_data());

	DestroyPoints(test_sample_point_vector);
}

TEST_F(utest_kdtree, insert_remove_node) {
	double test_sample_point[7][2] = { {4, 3}, {3, 4}, {5, 8}, {3, 3}, {3, 9}, {6, 4}, {5, 9} };
	char test_sample_payload[7] = { 'q', 'w', 'e', 'r', 't', 'y', 'u' };

	std::vector< std::vector<double> * > * test_sample_point_vector = GeneratePoints((double *) &test_sample_point, 2, 7);

	for (unsigned int index = 0; index < 7; index++) {
		std::vector<double> * point = (*test_sample_point_vector)[index];
		char * payload = (char *) &test_sample_payload[index];

		tree->insert(point, payload);

		kdnode * node = tree->find_node(point);
		ASSERT_TRUE(NULL != node);
		ASSERT_EQ(point, node->get_data());
		ASSERT_EQ(payload, node->get_payload());
	}


	for (unsigned int index = 0; index < 7; index++) {
		std::vector<double> * point = (*test_sample_point_vector)[index];
		tree->remove(point);

		kdnode * node = tree->find_node((*test_sample_point_vector)[index]);
		ASSERT_EQ(NULL, node);

		for (unsigned int next_index = index + 1; next_index < 7; next_index++) {
			node = tree->find_node( (*test_sample_point_vector)[next_index] );
			std::vector<double> * point = (*test_sample_point_vector)[next_index];

			ASSERT_EQ(point, node->get_data());
			ASSERT_EQ(&test_sample_payload[next_index], node->get_payload());
		}
	}

	DestroyPoints(test_sample_point_vector);
}

TEST_F(utest_kdtree, find_without_insertion) {
	double test_sample_point[7][2] = { {4, 3}, {3, 4}, {5, 8}, {3, 3}, {3, 9}, {6, 4}, {5, 9} };
	std::vector< std::vector<double> * > * test_sample_point_vector = GeneratePoints((double *) &test_sample_point, 2, 7);

	for (unsigned int index = 0; index < 7; index++) {
		std::vector<double> * point = (*test_sample_point_vector)[index];

		kdnode * node = tree->find_node(point);
		ASSERT_EQ(NULL, node);
	}

	DestroyPoints(test_sample_point_vector);
}

TEST_F(utest_kdtree, remove_long_branch) {
	double test_sample_point[5][2] = { {5, 5}, {6, 5}, {6, 6}, {7, 6}, {7, 7} };
	std::vector< std::vector<double> * > * test_sample_point_vector = GeneratePoints((double *) &test_sample_point, 2, 5);

	InitTestObject(test_sample_point_vector);

	for (unsigned int index = 0; index < 5; index++) {
		std::vector<double> * point = (*test_sample_point_vector)[index];
		tree->remove(point);

		kdnode * node = tree->find_node((*test_sample_point_vector)[index]);
		ASSERT_EQ(NULL, node);
	}

	DestroyPoints(test_sample_point_vector);
}

TEST_F(utest_kdtree, insert_remove_permutation_vector) {
	double test_sample_point[8][2] = { {5, 5}, {4, 5}, {4, 4}, {3, 4}, {3, 3}, {6, 6}, {8, 8} };
	std::vector<std::vector<double> * > * test_sample_point_vector = GeneratePoints((double *) &test_sample_point, 2, 7);
	std::vector<std::vector<double> * > * permutated_point_vector = new std::vector<std::vector<double> * >(test_sample_point_vector->begin(), test_sample_point_vector->end());

	do {
		/* nodes are inserted in the same way in each cycle */
		for (iterator_point point = test_sample_point_vector->begin(); point != test_sample_point_vector->end(); point++) {
			tree->insert(*point, NULL);
		}

		/* nodes are removed in deffirent order in each cycle */
		for (unsigned int index_point = 0; index_point < permutated_point_vector->size(); index_point++) {
			tree->remove( (*permutated_point_vector)[index_point] );

			unsigned int expected_length = permutated_point_vector->size() - index_point - 1;
			ASSERT_EQ(expected_length, tree->traverse(tree->get_root()));
		}

		ASSERT_EQ(0, tree->traverse(tree->get_root()));
	} while ( std::next_permutation(permutated_point_vector->begin(), permutated_point_vector->end()) );

	DestroyPoints(test_sample_point_vector);
	delete permutated_point_vector;
}

#endif
