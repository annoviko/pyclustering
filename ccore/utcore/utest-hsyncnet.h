#ifndef _UTEST_HSYNCNET_
#define _UTEST_HSYNCNET_

#include "ccore/hsyncnet.h"

#include "gtest/gtest.h"

static void template_cluster_allocation(const unsigned int number_clusters) {
	std::vector<std::vector<double> > sample;

	sample.push_back( { 0.1, 0.1 } );
	sample.push_back( { 1.2, 1.1 } );
	sample.push_back( { 5.0, 5.0 } );

	sample.push_back( { 10.2, 10.1 } );
	sample.push_back( { 11.3, 11.0 } );
	sample.push_back( { 15.1, 15.4 } );

	hsyncnet network(&sample, number_clusters, initial_type::EQUIPARTITION);

	hsyncnet_analyser analyser;
	network.process(0.995, solve_type::FAST, true, analyser);

	hsyncnet_cluster_data ensembles;
	analyser.allocate_clusters(0.1, ensembles);

	ASSERT_EQ(number_clusters, ensembles.size());
}

TEST(utest_hsyncnet, allocation_6_clusters) {
	template_cluster_allocation(6);
}

TEST(utest_hsyncnet, allocation_2_clusters) {
	template_cluster_allocation(2);
}

TEST(utest_hsyncnet, allocation_1_clusters) {
	template_cluster_allocation(1);
}

#endif