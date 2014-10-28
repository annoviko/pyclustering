#ifndef _UTEST_KDTREE_
#define _UTEST_KDTREE_

#include "ccore\kdtree.h"
#include "gtest\gtest.h"

class utest_kdtree : public ::testing::Test {
protected:
	typedef std::vector< std::vector<double> * >::iterator			iterator_point;
	typedef std::vector< std::vector<double> * >::const_iterator	const_iterator_point;

	virtual void SetUp() { 
		tree = new kdtree(); 
		points = new std::vector< std::vector<double> * >();
	}

	virtual void TearDown() { 
		delete tree;

		for (std::vector< std::vector<double> * >::iterator iter = points->begin(); iter != points->end(); iter++) { delete *iter; }
		delete points;
	}

	virtual void Initialization(double * pointer_points, unsigned int dimension, unsigned int number) {
		delete tree;

		kdtree * tree = new kdtree(GeneratePoints(pointer_points, dimension, number), NULL);
	}

	virtual std::vector< std::vector<double> * > * GeneratePoints(double * pointer_points, unsigned int dimension, unsigned int number) {
		unsigned int cursor = 0;
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

	virtual std::vector<double> * CreatePoint(double * pointer_point, unsigned int dimension) {
		std::vector<double> * single_point = new std::vector<double>(dimension, 0);
		for (unsigned int index_dimension = 0; index_dimension < dimension; index_dimension++) {
			(*single_point)[index_dimension] = pointer_point[index_dimension];
		}

		points->push_back(single_point);
		return single_point;
	}

protected:
	kdtree									* tree;
	std::vector< std::vector<double> * >	* points;
};


TEST_F(utest_kdtree, creation_without_payload) {
	double test_sample_point[7][2] = { {4, 3}, {3, 4}, {5, 8}, {3, 3}, {3, 9}, {6, 4}, {5, 9} };
	
	Initialization((double *) &test_sample_point, 2, 7);

	for (const_iterator_point point = points->begin(); point != points->end(); point++) {
		kdnode * node = tree->find_node(*point);

		ASSERT_TRUE(node != NULL);
		ASSERT_TRUE(node->get_payload() == NULL);
		ASSERT_TRUE(node->get_data() == *point);
	}
}

TEST_F(utest_kdtree, parent_node) {
	double test_sample_point[7][2] = { {4, 3}, {3, 4}, {5, 8}, {3, 3}, {3, 9}, {6, 4}, {5, 9} };

	Initialization((double *) &test_sample_point, 2, 7);

	kdnode * node = tree->find_node( (*points)[0] );
	ASSERT_TRUE(node->get_parent() == NULL);

	node = tree->find_node( (*points)[1] );
	ASSERT_TRUE(node->get_parent()->get_data() == (*points)[0]);

	node = tree->find_node( (*points)[2] );
	ASSERT_TRUE(node->get_parent()->get_data() == (*points)[0]);

	node = tree->find_node( (*points)[5] );
	ASSERT_TRUE(node->get_parent()->get_data() == (*points)[2]);

	node = tree->find_node( (*points)[3] );
	ASSERT_TRUE(node->get_parent()->get_data() == (*points)[1]);

	node = tree->find_node( (*points)[6] );
	ASSERT_TRUE(node->get_parent()->get_data() == (*points)[2]);

	node = tree->find_node( (*points)[4] );
	ASSERT_TRUE(node->get_parent()->get_data() == (*points)[1]);
}

TEST_F(utest_kdtree, insert_remove_node) {
	double test_sample_point[7][2] = { {4, 3}, {3, 4}, {5, 8}, {3, 3}, {3, 9}, {6, 4}, {5, 9} };
	char test_sample_payload[7] = { 'q', 'w', 'e', 'r', 't', 'y', 'u' };

	for (unsigned int index = 0; index < 7; index++) {
		std::vector<double> * point = CreatePoint((double *) &test_sample_point[index], 2);
		char * payload = (char *) &test_sample_payload[index];

		tree->insert(point, payload);

		kdnode * node = tree->find_node(point);
		ASSERT_TRUE(NULL != node);
		ASSERT_EQ(point, node->get_data());
		ASSERT_EQ(payload, node->get_payload());
	}


	for (unsigned int index = 0; index < 7; index++) {
		std::vector<double> * point = (*points)[index];
		tree->remove(point);

		kdnode * node = tree->find_node((*points)[index]);
		ASSERT_EQ(NULL, node);

		for (unsigned int next_index = index + 1; next_index < 7; next_index++) {
			node = tree->find_node( (*points)[next_index] );
			std::vector<double> * point = (*points)[next_index];

			ASSERT_EQ(point, node->get_data());
			ASSERT_EQ(&test_sample_payload[next_index], node->get_payload());
		}
	}
}

TEST_F(utest_kdtree, find_without_insertion) {
	double test_sample_point[7][2] = { {4, 3}, {3, 4}, {5, 8}, {3, 3}, {3, 9}, {6, 4}, {5, 9} };

	for (unsigned int index = 0; index < 7; index++) {
		std::vector<double> * point = CreatePoint((double *) &test_sample_point[index], 2);

		kdnode * node = tree->find_node(point);
		ASSERT_EQ(NULL, node);
	}
}

TEST_F(utest_kdtree, remove_long_branch) {
	double test_sample_point[5][2] = { {5, 5}, {6, 5}, {6, 6}, {7, 6}, {7, 7} };

	Initialization((double *) &test_sample_point, 2, 5);

	for (unsigned int index = 0; index < 5; index++) {
		std::vector<double> * point = (*points)[index];
		tree->remove(point);

		kdnode * node = tree->find_node((*points)[index]);
		ASSERT_EQ(NULL, node);
	}
}

#endif