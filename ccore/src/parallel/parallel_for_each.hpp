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


/* Available options: 
    1. PARALLEL_IMPLEMENTATION_ASYNC_POOL - own parallel implementation based on std::async pool
    2. PARALLEL_IMPLEMENTATION_NONE       - parallel implementation is not used
    3. PARALLEL_IMPLEMENTATION_PPL        - parallel PPL implementation (windows system only)         */


#if defined(_WIN32)
#define PARALLEL_IMPLEMENTATION_PPL
#else
#define PARALLEL_IMPLEMENTATION_ASYNC_POOL
#endif


#if defined(PARALLEL_IMPLEMENTATION_PPL)
#include <ppl.h>
#endif


namespace ccore {

namespace parallel {


template <typename TypeIter, typename TypeAction>
void parallel_for_each(const TypeIter p_begin, const TypeIter p_end, const TypeAction & p_task) {
#if defined(PARALLEL_IMPLEMENTATION_ASYNC_POOL)
    static const std::size_t amount_hardware_threads = std::thread::hardware_concurrency();
    static const std::size_t amount_threads = (amount_hardware_threads > 1) ? (amount_hardware_threads - 1) : 0;
    static std::vector<std::future<void>> future_storage(amount_threads);
    static std::vector<spinlock> future_locks(amount_threads);

    const std::size_t step = std::distance(p_begin, p_end) / (amount_threads + 1);

    auto current_start = p_begin;
    auto current_end = p_begin + step;

    std::vector<std::size_t> captured_feature;

    for (std::size_t i = 0; i < amount_threads; ++i) {
        auto async_task = [&p_task, current_start, current_end](){
            for (auto iter = current_start; iter != current_end; ++iter) {
                p_task(*iter);
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

    for (auto iter = current_start; iter != p_end; ++iter) {
        p_task(*iter);
    }

    for (auto index_feature : captured_feature) {
        future_storage[index_feature].get();
        future_locks[index_feature].unlock();
    }
#elif defined(PARALLEL_IMPLEMENTATION_PPL)
    concurrency::parallel_for_each(p_begin, p_end, p_task);
#else
    /* This part of code is switched only to estimate parallel implementation with non-parallel.
       Never switch on for real product. */
    for (auto iter = p_begin; iter != p_end; ++iter) {
        p_task(*iter);
    }
#endif
}


template <typename TypeContainer, typename TypeAction>
void parallel_for_each(const TypeContainer & p_container, const TypeAction & p_task) {
    parallel_for_each(std::begin(p_container), std::end(p_container), p_task);
}


}

}