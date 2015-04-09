#ifndef _UTEST_DIFFERENTIAL_
#define _UTEST_DIFFERENTIAL_

#include "ccore/differential.h"

#include "gtest/gtest.h"

using namespace differential;

TEST(utest_differential, plus_states) {
	differ_state<double> state1 { 0, 1, 2, 3, 4 };
	differ_state<double> state2 { 0, 1, 2, 3, 4 };

	differ_state<double> expected_result { 0, 2, 4, 6, 8 };

	ASSERT_TRUE(expected_result != state1);
	ASSERT_TRUE(expected_result != state2);
	ASSERT_TRUE(state1 == state2);
	ASSERT_TRUE(expected_result == state1 + state2);
}

TEST(utest_differential, plus_various_states) {
	differ_state<double> state1 { 12, -6, 11, 12, 5 };
	differ_state<double> state2 { -5, 5.5, 100, 32, 1 };

	differ_state<double> expected_result { 12 - 5, 5.5 - 6, 11 + 100, 12 + 32, 5 + 1 };

	ASSERT_TRUE(expected_result == state1 + state2);
}

TEST(utest_differential, plus_value) {
	differ_state<double> state { 0, 1, 2, 3, 4 };

	differ_state<double> expected_result1 { 1, 2, 3, 4, 5 };
	ASSERT_TRUE(expected_result1 == state + 1);
	ASSERT_TRUE(expected_result1 == 1 + state);

	differ_state<double> expected_result2 { 0.5, 1.5, 2.5, 3.5, 4.5 };
	ASSERT_TRUE(expected_result2 == state + 0.5);
	ASSERT_TRUE(expected_result2 == 0.5 + state);

	differ_state<double> expected_result3 { -1, 0, 1, 2, 3 };
	ASSERT_TRUE(expected_result3 == state + (-1));
	ASSERT_TRUE(expected_result3 == (-1) + state);
}

TEST(utest_differential, minus_states) {
	differ_state<double> state1 { 0, 1, 2, 3, 4 };
	differ_state<double> state2 { 0, 1, 2, 3, 4 };

	differ_state<double> expected_result { 0, 0, 0, 0, 0 };

	ASSERT_TRUE(expected_result == state1 - state2);
}

TEST(utest_differential, minus_various_states) {
	differ_state<double> state1 { 5, 10, 15, 20, 25, 30 };
	differ_state<double> state2 { 2, 12, 12, 22, 22, 32 };

	differ_state<double> expected_result { 3, -2, 3, -2, 3, -2 };

	ASSERT_TRUE(expected_result == state1 - state2);
}

TEST(utest_differential, minus_value) {
	differ_state<double> state { 0, 1, 2, 3, 4 };

	differ_state<double> expected_result1 { -1, 0, 1, 2, 3 };
	ASSERT_TRUE(expected_result1 == state - 1);

	differ_state<double> expected_result2 { 1, 0, -1, -2, -3 };
	ASSERT_TRUE(expected_result2 == 1 - state);
}

TEST(utest_differential, multiply_value) {
	differ_state<double> state1 { -2, -1, 0, 1, 2 };

	ASSERT_TRUE(state1 == state1 * 1);
	ASSERT_TRUE(state1 == 1 * state1);

	differ_state<double> expected_result1 { -4, -2, 0, 2, 4 };
	differ_state<double> expected_result2 { -6, -3, 0, 3, 6 };

	ASSERT_TRUE(expected_result1 == state1 * 2);
	ASSERT_TRUE(expected_result1 == 2 * state1);

	ASSERT_TRUE(expected_result2 == state1 * 3);
	ASSERT_TRUE(expected_result2 == 3 * state1);
}

TEST(utest_differential, divide_value) {
	differ_state<double> state1 { -2, -1, 0, 1, 2 };

	differ_state<double> expected_result1 { -2, -1, 0, 1, 2 };
	ASSERT_TRUE(expected_result1 == state1 / 1);

	differ_state<double> expected_result2 { -1, -0.5, 0, 0.5, 1 };
	ASSERT_TRUE(expected_result2 == state1 / 2);
}

TEST(utest_differential, assign_operations) {
	differ_state<double> state1 { -2, -1, 0, 1, 2 };
	differ_state<double> state2 = state1;

	ASSERT_TRUE(state1 == state2);
	ASSERT_TRUE(state2 == state1);

	state1 += 10;
	differ_state<double> expected_result1 { 8, 9, 10, 11, 12 };
	ASSERT_TRUE(expected_result1 == state1);

	state1 -= 5;
	differ_state<double> expected_result2 { 3, 4, 5, 6, 7 };
	ASSERT_TRUE(expected_result2 == state1);

	state1 *= 2;
	differ_state<double> expected_result3 { 6, 8, 10, 12, 14 };
	ASSERT_TRUE(expected_result3 == state1);

	state1 /= 0.5;
	differ_state<double> expected_result4 { 12, 16, 20, 24, 28 };
	ASSERT_TRUE(expected_result4 == state1);

	state1 = state2;
	ASSERT_TRUE(state1 == state2);
}


#endif