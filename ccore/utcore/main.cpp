#include <gtest/gtest.h>

#include "utest-kdtree.h"
#include "utest-pcnn.h"

int main(int argc, char *argv[]) {
	::testing::InitGoogleTest(&argc, argv);
	return RUN_ALL_TESTS();
}