/**
*
* Copyright (C) 2014-2018    Andrei Novikov (pyclustering@yandex.ru)
*
* GNU_PUBLIC_LICENSE
*   pyclustering is free software: you can redistribute it and/or modify
*   it under the terms of the GNU General Public License as published by
*   the Free Software Foundation, either version 3 of the License, or
*   (at your option) any later version.
*
*   pyclustering is distributed in the hope that it will be useful,
*   but WITHOUT ANY WARRANTY; without even the implied warranty of
*   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
*   GNU General Public License for more details.
*
*   You should have received a copy of the GNU General Public License
*   along with this program.  If not, see <http://www.gnu.org/licenses/>.
*
*/


#include "gtest/gtest.h"

#include "parallel/thread_pool.hpp"

#include <algorithm>
#include <limits>
#include <numeric>
#include <map>
#include <vector>


using namespace ccore::parallel;


std::size_t AUTO_POOL_SIZE = std::numeric_limits<std::size_t>::max();


static void template_create_delete_test(const std::size_t p_size) {
    thread_pool * pool          = nullptr;
    std::size_t expected_size   = p_size;

    if (p_size == AUTO_POOL_SIZE) {
        pool = new thread_pool();
        expected_size = thread_pool::DEFAULT_POOL_SIZE;
    }
    else {
        pool = new thread_pool(p_size);
    }

    ASSERT_EQ(expected_size, pool->size());
    ASSERT_EQ(task::INVALID_TASK_ID, pool->pop_complete_task());

    delete pool;
}


TEST(utest_thread_pool, create_delete_size_1) {
    template_create_delete_test(1);
}

TEST(utest_thread_pool, create_delete_size_5) {
    template_create_delete_test(5);
}

TEST(utest_thread_pool, create_delete_size_20) {
    template_create_delete_test(20);
}

TEST(utest_thread_pool, auto_size_pool) {
    template_create_delete_test(AUTO_POOL_SIZE);
}


static void template_add_task_test(const std::size_t p_pool_size, const std::size_t p_task_amount) {
    std::unique_ptr<thread_pool> pool = nullptr;
    if (p_pool_size == AUTO_POOL_SIZE) {
        pool = std::unique_ptr<thread_pool>(new thread_pool());
    }
    else {
        pool = std::unique_ptr<thread_pool>(new thread_pool(p_pool_size));
    }

    std::vector<double> results(p_task_amount, 0.0);

    double expected_basic_result = 1.0;
    std::vector<double> expected_results(p_task_amount, 0.0);
    for (std::size_t i = 0; i < p_task_amount; i++) {
        expected_results[i] = expected_basic_result + i;
    }

    std::map<std::size_t, std::size_t> task_ids;
    for (std::size_t task_index = 0; task_index < p_task_amount; task_index++) {
        task::proc user_proc = [task_index, &results](){ 
                results[task_index] = task_index + 1.0;
            };
        
        std::size_t id = pool->add_task(user_proc);

        ASSERT_NE(task::INVALID_TASK_ID, id);
        ASSERT_TRUE(task_ids.find(id) == task_ids.end());

        task_ids[id] = task_index;
    }

    ASSERT_EQ(p_task_amount, task_ids.size());

    for (std::size_t i = 0; i < p_task_amount; i++) {
        task::id id = pool->pop_complete_task();

        ASSERT_NE(task::INVALID_TASK_ID, id);
        ASSERT_TRUE(task_ids.find(id) != task_ids.end());

        task::id task_index = task_ids[id];
        double obtained_result = results[task_index];
        double expected_result = expected_results[task_index];

        ASSERT_EQ(expected_result, obtained_result);
    }

    task::id id = pool->pop_complete_task();
    ASSERT_EQ(task::INVALID_TASK_ID, id);
}


TEST(utest_thread_pool, pool_bigger_task_amount) {
    template_add_task_test(10, 5);
}

TEST(utest_thread_pool, pool_equal_task_amount) {
    template_add_task_test(5, 5);
}

TEST(utest_thread_pool, pool_less_task_amount) {
    template_add_task_test(5, 20);
}

TEST(utest_thread_pool, pool_1_thread_20_tasks) {
    template_add_task_test(1, 20);
}

TEST(utest_thread_pool, pool_1_thread_1_task) {
    template_add_task_test(1, 1);
}

TEST(utest_thread_pool, pool_1_thread_2_tasks) {
    template_add_task_test(1, 2);
}

TEST(utest_thread_pool, pool_1_thread_3_tasks) {
    template_add_task_test(1, 3);
}

TEST(utest_thread_pool, pool_2_threads_1_tasks) {
    template_add_task_test(2, 4);
}

TEST(utest_thread_pool, pool_2_threads_2_tasks) {
    template_add_task_test(2, 4);
}

TEST(utest_thread_pool, pool_2_threads_3_tasks) {
    template_add_task_test(2, 4);
}

TEST(utest_thread_pool, pool_2_threads_4_tasks) {
    template_add_task_test(2, 4);
}

TEST(utest_thread_pool, pool_10_threads_1_tasks) {
    template_add_task_test(10, 1);
}

TEST(utest_thread_pool, pool_10_threads_100_tasks) {
    template_add_task_test(10, 100);
}

TEST(utest_thread_pool, pool_10_threads_200_tasks) {
    template_add_task_test(10, 200);
}

TEST(utest_thread_pool, pool_20_threads_200_tasks) {
    template_add_task_test(20, 100);
}

TEST(utest_thread_pool, pool_30_threads_300_tasks) {
    template_add_task_test(30, 300);
}

TEST(utest_thread_pool, pool_5_threads_5000_tasks) {
    template_add_task_test(5, 5000);
}

TEST(utest_thread_pool, continious_pool_5_threads_50_tasks) {
    for (std::size_t i = 0; i < 100; i++) {
        template_add_task_test(5, 50);
    }
}

TEST(utest_thread_pool, pool_auto_size_1_tasks) {
    template_add_task_test(AUTO_POOL_SIZE, 20);
}

TEST(utest_thread_pool, pool_auto_size_10_tasks) {
    template_add_task_test(AUTO_POOL_SIZE, 10);
}

TEST(utest_thread_pool, pool_auto_size_20_tasks) {
    template_add_task_test(AUTO_POOL_SIZE, 20);
}

TEST(utest_thread_pool, pool_auto_size_50_tasks) {
    template_add_task_test(AUTO_POOL_SIZE, 20);
}

TEST(utest_thread_pool, pool_auto_size_100_tasks) {
    template_add_task_test(AUTO_POOL_SIZE, 20);
}
