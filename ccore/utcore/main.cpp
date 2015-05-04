#include <gtest/gtest.h>

#include "utest-differential.h"
#include "utest-kdtree.h"
#include "utest-network.h"
#include "utest-pcnn.h"
#include "utest-sync.h"
#include "utest-syncnet.h"

int main(int argc, char *argv[]) {
	::testing::InitGoogleTest(&argc, argv);
	return RUN_ALL_TESTS();
}