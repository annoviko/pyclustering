#include <gtest/gtest.h>

#include "utest-agglomerative.h"
#include "utest-differential.h"
#include "utest-hsyncnet.h"
#include "utest-kdtree.h"
#include "utest-kmedians.h"
#include "utest-legion.h"
#include "utest-network.h"
#include "utest-pcnn.h"
#include "utest-som.h"
#include "utest-sync.h"
#include "utest-syncnet.h"
#include "utest-syncpr.h"
#include "utest-xmeans.h"

int main(int argc, char *argv[]) {
	::testing::InitGoogleTest(&argc, argv);
	return RUN_ALL_TESTS();
}
