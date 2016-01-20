#ifndef _UTEST_HSYNCNET_
#define _UTEST_HSYNCNET_

#include "ccore/hsyncnet.h"

#include "gtest/gtest.h"

static void template_cluster_allocation(const unsigned int number_clusters) {
	bool result_testing = false;

	for (unsigned int i = 0; i < 3; i++) {
		std::vector<std::vector<double> > sample;

		sample.push_back( { 0.1, 0.1 } );
		sample.push_back( { 1.2, 1.1 } );
		sample.push_back( { 5.0, 5.0 } );

		sample.push_back( { 10.2, 10.1 } );
		sample.push_back( { 11.3, 11.0 } );
		sample.push_back( { 15.1, 15.4 } );

		hsyncnet network(&sample, number_clusters, initial_type::EQUIPARTITION);

		hsyncnet_analyser analyser;
		network.process(0.998, solve_type::FAST, true, analyser);

		hsyncnet_cluster_data ensembles;
		analyser.allocate_clusters(0.1, ensembles);

		if (number_clusters != ensembles.size()) {
			continue;
		}

		result_testing = true;
	}

	ASSERT_TRUE(result_testing);
}

TEST(utest_hsyncnet, allocation_2_clusters) {
	template_cluster_allocation(2);
}

TEST(utest_hsyncnet, allocation_1_clusters) {
	template_cluster_allocation(1);
}

#endif
