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


#pragma once


#include <cstddef>
#include <functional>
#include <future>
#include <vector>

#include "start_for.hpp"


/* Available options: PARALLEL_IMPLEMENTATION_ASYNC, 
                      PARALLEL_IMPLEMENTATION_CCORE_THREAD_POOL, 
                      PARALLEL_IMPLEMENTATION_NONE, 
                      PARALLEL_IMPLEMENTATION_THREAD_POOL,
                      PARALLEL_IMPLEMENTATION_ASYNC_POOL */

#define PARALLEL_IMPLEMENTATION_ASYNC_POOL


namespace ccore {

namespace parallel {


template <typename TypeAction>
void parallel_for(std::size_t p_start, std::size_t p_end, const TypeAction & p_task) {
#if defined(PARALLEL_IMPLEMENTATION_ASYNC)
    static const std::size_t amount_hardware_threads = std::thread::hardware_concurrency();
    static const std::size_t amount_threads = (amount_hardware_threads > 1) ? (amount_hardware_threads - 1) : 0;

    std::vector<std::future<void>> future_storage(amount_threads);

    const std::size_t step = (p_end - p_start) / (amount_threads + 1);
    std::size_t current_start = p_start;
    std::size_t current_end = p_start + step;

    for (std::size_t i = 0; i < amount_threads; ++i) {
        std::future<void> future_result;
        auto async_task = [&p_task, current_start, current_end](){
            for (std::size_t i = current_start; i < current_end; ++i) {
                p_task(i);
            }
        };

        try {
            future_result = std::async(std::launch::async, async_task);
        }
        catch(std::system_error &) {
            //std::cout << "[DEBUG] (parallel_for) std::async throws exception." << std::endl;
            future_result = std::async(std::launch::async | std::launch::deferred, async_task);
        }

        future_storage[i] = std::move(future_result);

        current_start = current_end;
        current_end += step;
    }

    for (std::size_t i = current_start; i < p_end; ++i) {
        p_task(i);
    }

    for (auto & result : future_storage) {
        result.get();
    }
#elif defined(PARALLEL_IMPLEMENTATION_ASYNC_POOL)
    static const std::size_t amount_hardware_threads = std::thread::hardware_concurrency();
    static const std::size_t amount_threads = (amount_hardware_threads > 1) ? (amount_hardware_threads - 1) : 0;
    static std::vector<std::future<void>> future_storage(amount_threads);
    static std::vector<spinlock> future_locks(amount_threads);

    const std::size_t step = (p_end - p_start) / (amount_threads + 1);
    std::size_t current_start = p_start;
    std::size_t current_end = p_start + step;

    std::vector<std::size_t> captured_feature;

    for (std::size_t i = 0; i < amount_threads; ++i) {
        auto async_task = [&p_task, current_start, current_end](){
            for (std::size_t i = current_start; i < current_end; ++i) {
                p_task(i);
            }
        };

        std::size_t free_index = (std::size_t) -1;
        for (std::size_t i = 0; i < amount_threads; i++) {
            if (future_locks[i].try_lock()) {
                free_index = i;
                break;
            }
        }

        if (free_index != (std::size_t) -1) {
            auto future_result = std::async(std::launch::async, async_task);
            future_storage[free_index] = std::move(future_result);
            captured_feature.push_back(free_index);
        }
        else {
            async_task();
        }

        current_start = current_end;
        current_end += step;
    }

    for (std::size_t i = current_start; i < p_end; ++i) {
        p_task(i);
    }

    for (auto index_feature : captured_feature) {
        future_storage[index_feature].get();
        future_locks[index_feature].unlock();
    }
#elif defined(PARALLEL_IMPLEMENTATION_CCORE_THREAD_POOL)
    static const std::size_t amount_threads = start_for::get_instance().size();

    const std::size_t step = (p_end - p_start) / (amount_threads + 1);

    std::size_t current_start = p_start;
    std::size_t current_end = p_start + step;

    std::vector<task::ptr> task_storage;
    task_storage.reserve(amount_threads);

    for (std::size_t i = 0; i < amount_threads; ++i) {
        auto async_task = [&p_task, current_start, current_end](){
            for (std::size_t i = current_start; i < current_end; ++i) {
                p_task(i);
            }
        };

        task::ptr task_under_processing = start_for::get_instance().add_task_if_free(async_task);
        if (task_under_processing == nullptr) {
            /* There is no free threads to take care about this task, process it by this thread */
            async_task();
        }
        else {
            task_storage.push_back(std::move(task_under_processing));
        }

        current_start = current_end;
        current_end += step;
    }

    for (std::size_t i = current_start; i < p_end; ++i) {
        p_task(i);
    }

    for (auto & task_under_processing : task_storage) {
        task_under_processing->wait_ready();
    }
#elif defined(PARALLEL_IMPLEMENTATION_THREAD_POOL)
    static const std::size_t amount_hardware_threads = std::thread::hardware_concurrency();
    static const std::size_t amount_threads = (amount_hardware_threads > 1) ? (amount_hardware_threads - 1) : 1;

    static std::vector<std::thread> thread_pool(amount_threads);
    static std::vector<spinlock> thread_locks(amount_threads);

    const std::size_t step = (p_end - p_start) / (amount_threads + 1);

    std::size_t current_start = p_start;
    std::size_t current_end = p_start + step;

    std::vector<std::size_t> captured_threads;

    for (std::size_t i = 0; i < amount_threads; ++i) {
        std::size_t free_thread_index = (std::size_t) -1;
        for (std::size_t thread_index = 0; thread_index < amount_threads; ++thread_index) {
            if (thread_locks[thread_index].try_lock()) {
                free_thread_index = thread_index;
                break;
            }
        }

        auto async_task = [&p_task, current_start, current_end]() {
            for (std::size_t i = current_start; i < current_end; ++i) {
                p_task(i);
            }
        };

        if (free_thread_index != (std::size_t) -1) {
            captured_threads.push_back(free_thread_index);
            thread_pool[free_thread_index] = std::move(std::thread(async_task));
        }
        else {
            /* There is no free threads to take care about this task, process it by this thread */
            async_task();
        }

        current_start = current_end;
        current_end += step;
    }

    /* Perform processing by this thread also */
    for (std::size_t i = current_start; i < p_end; ++i) {
        p_task(i);
    }

    for (auto thread_index : captured_threads) {
        thread_pool[thread_index].join();
        thread_locks[thread_index].unlock();
    }
#else
    /* This part of code is switched only to estimate parallel implementation of any algorithm with non-parallel.
       Never switch on for real product. */
    for (std::size_t i = p_start; i < p_end; i++) {
        p_task(i);
    }
#endif
}


}

}