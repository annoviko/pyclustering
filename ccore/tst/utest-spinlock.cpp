/*!

@authors Andrei Novikov (pyclustering@yandex.ru)
@date 2014-2020
@copyright BSD-3-Clause

*/


#include <gtest/gtest.h>

#include <pyclustering/parallel/spinlock.hpp>
#include <pyclustering/parallel/thread_pool.hpp>

#include <algorithm>


using namespace pyclustering::parallel;


TEST(utest_spinlock, count_value) {
    const std::size_t amount_count = 100000;
    const std::size_t amount_tasks = 50;

    std::vector<std::thread> pool;

    std::size_t result = 0;
    spinlock locker;
    auto task = [&result, &locker, amount_count]() {
        for (std::size_t i = 0; i < amount_count; i++) {
            locker.lock();
            result++;
            locker.unlock();
        }
    };

    for (std::size_t i = 0; i < amount_tasks; i++) {
        pool.emplace_back(task);
    }

    for (std::size_t i = 0; i < amount_tasks; i++) {
        pool[i].join();
    }

    ASSERT_EQ(amount_count * amount_tasks, result);
}


TEST(utest_spinlock, count_value_thread_pool) {
    const std::size_t amount_threads = 20;
    const std::size_t amount_count = 1000;
    const std::size_t amount_tasks = 1000;

    thread_pool pool(amount_threads);

    std::size_t result = 0;
    spinlock locker;
    auto task = [&result, &locker, amount_count]() {
        for (std::size_t i = 0; i < amount_count; i++) {
            locker.lock();
            result++;
            locker.unlock();
        }
    };

    std::vector<task::ptr> tasks(amount_tasks);
    for (std::size_t i = 0; i < amount_tasks; i++) {
        tasks[i] = pool.add_task(task);
    }

    for (std::size_t i = 0; i < amount_tasks; i++) {
        tasks[i]->wait_ready();
    }

    ASSERT_EQ(amount_count * amount_tasks, result);
}
