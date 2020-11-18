/*!

@authors Andrei Novikov (pyclustering@yandex.ru)
@date 2014-2020
@copyright BSD-3-Clause

*/


#include <gtest/gtest.h>

#include <pyclustering/cluster/ordering_analyser.hpp>

#include "samples.hpp"
#include "utenv_check.hpp"


using namespace pyclustering::clst;


TEST(utest_ordering, cluster_allocation_identical_ordering) {
    ordering cluster_ordering = {5.0, 5.0, 5.0, 5.0, 5.0, 5.0};

    EXPECT_EQ(1U, ordering_analyser::extract_cluster_amount(cluster_ordering, 6.5));
    EXPECT_EQ(0U, ordering_analyser::extract_cluster_amount(cluster_ordering, 4.5));
}


TEST(utest_ordering, impossible_calculate_radius_identical_ordering) {
    ordering cluster_ordering = {5.0, 5.0, 5.0, 5.0, 5.0, 5.0, 5.0, 5.0, 5.0, 5.0};

    EXPECT_TRUE(ordering_analyser::calculate_connvectivity_radius(cluster_ordering, 2) < 0);
}


TEST(utest_ordering, impossible_calculate_radius_geterogeneous_ordering) {
    ordering cluster_ordering = {5.0, 5.0, 5.0, 5.0, 6.0, 8.0, 6.0, 5.0, 5.0, 5.0};

    EXPECT_TRUE(ordering_analyser().calculate_connvectivity_radius(cluster_ordering, 3) < 0);
}
