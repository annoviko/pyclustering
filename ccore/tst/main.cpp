#include <gtest/gtest.h>

#include "utest-adjacency_bit_matrix.hpp"
#include "utest_adjacency_connector.hpp"
#include "utest-adjacency_list.hpp"
#include "utest-adjacency_matrix.hpp"
#include "utest-adjacency_weight_list.hpp"
#include "utest-agglomerative.hpp"
#include "utest-ant_colony.hpp"
#include "utest-differential.hpp"
#include "utest-hsyncnet.hpp"
#include "utest-kdtree.hpp"
#include "utest-kmedians.hpp"
#include "utest-legion.hpp"
#include "utest-pcnn.hpp"
#include "utest-som.hpp"
#include "utest-sync.hpp"
#include "utest-syncnet.hpp"
#include "utest-syncpr.hpp"
#include "utest-xmeans.hpp"


int main(int argc, char *argv[]) {
	::testing::InitGoogleTest(&argc, argv);
	return RUN_ALL_TESTS();
}
