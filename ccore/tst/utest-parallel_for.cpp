/*!

@authors Andrei Novikov (pyclustering@yandex.ru)
@date 2014-2020
@copyright BSD-3-Clause

*/


#include <gtest/gtest.h>

#include <pyclustering/parallel/parallel.hpp>

#include <numeric>


using namespace pyclustering::parallel;


static void template_parallel_square(const std::size_t p_length, const std::size_t p_step = 1, const std::size_t p_threads = -1) {
    std::vector<double> values(p_length);
    std::iota(values.begin(), values.end(), 0);

    std::vector<double> results(p_length);

    if (p_threads == (std::size_t) -1) {
        parallel_for(std::size_t(0), values.size(), p_step, [&values, &results](const std::size_t p_index) {
            results[p_index] = values[p_index] * values[p_index];
        });
    }
    else {
        parallel_for(std::size_t(0), values.size(), p_step, [&values, &results](const std::size_t p_index) {
            results[p_index] = values[p_index] * values[p_index];
        }, p_threads);
    }


    for (std::size_t i = 0; i < p_length; i += p_step) {
        ASSERT_EQ(values[i] * values[i], results[i]);
    }
}


TEST(utest_parallel_for, square_1_element) {
    template_parallel_square(1);
}


TEST(utest_parallel_for, square_3_element) {
    template_parallel_square(3);
}


TEST(utest_parallel_for, square_10_elements) {
    template_parallel_square(10);
}


TEST(utest_parallel_for, square_elements_step_increase) {
    for (std::size_t i = 0; i < 50; i++) {
        template_parallel_square(i);
    }
}


TEST(utest_parallel_for, square_10000_elements) {
    template_parallel_square(10000);
}


TEST(utest_parallel_for, square_10_elements_step_2) {
    template_parallel_square(10, 2);
}


TEST(utest_parallel_for, square_10_elements_step_2_thread_1) {
    template_parallel_square(10, 2, 1);
}


TEST(utest_parallel_for, square_10_elements_step_3) {
    template_parallel_square(10, 3);
}


TEST(utest_parallel_for, square_10_elements_step_3_thread_1) {
    template_parallel_square(10, 3, 1);
}


TEST(utest_parallel_for, square_20_elements_step_2) {
    template_parallel_square(20, 2);
}


TEST(utest_parallel_for, square_20_elements_step_2_thread_1) {
    template_parallel_square(20, 2, 1);
}


TEST(utest_parallel_for, square_20_elements_step_2_thread_increase) {
    for (std::size_t i = 1; i < 16; i++) {
        template_parallel_square(20, 2, i);
    }
}



TEST(utest_parallel_for, square_20_elements_step_3) {
    template_parallel_square(20, 3);
}


TEST(utest_parallel_for, square_20_elements_step_3_thread_1) {
    template_parallel_square(20, 3, 1);
}


TEST(utest_parallel_for, square_20_elements_step_4) {
    template_parallel_square(20, 4);
}


TEST(utest_parallel_for, square_20_elements_step_4_thread_1) {
    template_parallel_square(20, 4, 1);
}


TEST(utest_parallel_for, square_100_elements_step_2) {
    template_parallel_square(100, 2);
}


TEST(utest_parallel_for, square_100_elements_step_2_thread_1) {
    template_parallel_square(100, 2, 1);
}


TEST(utest_parallel_for, square_100_elements_step_3) {
    template_parallel_square(100, 3);
}


TEST(utest_parallel_for, square_100_elements_step_3_thread_1) {
    template_parallel_square(100, 3, 1);
}


TEST(utest_parallel_for, square_100_elements_step_3_thread_2) {
    template_parallel_square(100, 3, 2);
}


TEST(utest_parallel_for, square_100_elements_step_3_thread_increase) {
    for (std::size_t i = 1; i < 16; i++) {
        template_parallel_square(100, 3, i);
    }
}


TEST(utest_parallel_for, square_100_elements_step_5) {
    template_parallel_square(100, 5);
}


TEST(utest_parallel_for, square_100_elements_step_5_thread_2) {
    template_parallel_square(100, 5, 2);
}


TEST(utest_parallel_for, square_100_elements_step_10) {
    template_parallel_square(100, 10);
}


TEST(utest_parallel_for, square_1000_elements_step_13) {
    template_parallel_square(1000, 13);
}


TEST(utest_parallel_for, square_1000_elements_step_13_thread_1) {
    template_parallel_square(1000, 13, 1);
}


TEST(utest_parallel_for, square_100_elements_step_increase) {
    for (std::size_t i = 1; i < 100; i++) {     /* go over the limit as well */
        template_parallel_square(100, i);
    }
}


static void template_parallel_for_sum(const std::size_t p_length) {
    std::vector<double> values(p_length);
    std::iota(values.begin(), values.end(), 0);

    parallel_for(std::size_t(0), p_length, [&values](const std::size_t p_index) {
        values[p_index] = values[p_index] + values[p_index];
    });

    for (std::size_t i = 0; i < p_length; i++) {
        ASSERT_EQ(i + i, values[i]);
    }
}

TEST(utest_parallel_for, sum_1000000_elements) {
    template_parallel_for_sum(1000000);
}



static void template_parallel_foreach_square(const std::size_t p_length, const std::size_t p_thread = -1) {
    std::vector<double> values(p_length);
    std::iota(values.begin(), values.end(), 0);

    if (p_thread == (std::size_t) -1) {
        parallel_for_each(std::begin(values), std::end(values), [](double & value) {
            value = value * value;
        });
    }
    else {
        parallel_for_each(std::begin(values), std::end(values), [](double & value) {
            value = value * value;
        }, p_thread);
    }

    for (std::size_t i = 0; i < p_length; i++) {
        ASSERT_EQ(i * i, values[i]);
    }
}

TEST(utest_parallel_for_each, square_1_element) {
    template_parallel_foreach_square(1);
}


TEST(utest_parallel_for_each, square_1_element_thread_1) {
    template_parallel_foreach_square(1, 1);
}


TEST(utest_parallel_for_each, square_3_element) {
    template_parallel_foreach_square(3);
}


TEST(utest_parallel_for_each, square_3_element_thread_1) {
    template_parallel_foreach_square(3, 1);
}


TEST(utest_parallel_for_each, square_10_elements) {
    template_parallel_foreach_square(10);
}


TEST(utest_parallel_for_each, square_10_elements_thread_1) {
    template_parallel_foreach_square(10, 1);
}


TEST(utest_parallel_for_each, square_100_elements) {
    template_parallel_foreach_square(100);
}


TEST(utest_parallel_for_each, square_100_elements_thread_1) {
    template_parallel_foreach_square(100, 1);
}


TEST(utest_parallel_for_each, square_123_elements) {
    template_parallel_foreach_square(123);
}


TEST(utest_parallel_for_each, square_123_elements_thread_1) {
    template_parallel_foreach_square(123, 1);
}


TEST(utest_parallel_for_each, square_1000_elements) {
    template_parallel_foreach_square(1000);
}


static void template_parallel_foreach_sum(const std::size_t p_length, const std::size_t p_thread = -1) {
    std::vector<double> values(p_length);
    std::iota(values.begin(), values.end(), 0);

    if (p_thread == static_cast<std::size_t>(-1)) {
        parallel_for_each(std::begin(values), std::end(values), [](double & value) {
            value = value + value;
        });
    }
    else {
        parallel_for_each(std::begin(values), std::end(values), [](double & value) {
            value = value + value;
        }, p_thread);
    }

    for (std::size_t i = 0; i < p_length; i++) {
        ASSERT_EQ(i + i, values[i]);
    }
}


TEST(utest_parallel_for_each, increase_length_to_500) {
    for (std::size_t i = 1; i < 500; i++) {
        template_parallel_foreach_sum(i);
    }
}


TEST(utest_parallel_for_each, increase_length_to_500_thread_1) {
    for (std::size_t i = 1; i < 500; i++) {
        template_parallel_foreach_sum(i, 1);
    }
}


TEST(utest_parallel_for_each, sum_1000000_elements) {
    template_parallel_foreach_sum(1000000);
}
