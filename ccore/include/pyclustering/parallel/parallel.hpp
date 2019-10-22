/**
*
* @authors Andrei Novikov (pyclustering@yandex.ru)
* @date 2014-2019
* @copyright GNU Public License
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

#include <pyclustering/parallel/spinlock.hpp>


/* Available options: 
    1. PARALLEL_IMPLEMENTATION_ASYNC_POOL - own parallel implementation based on std::async pool
    2. PARALLEL_IMPLEMENTATION_NONE       - parallel implementation is not used
    3. PARALLEL_IMPLEMENTATION_PPL        - parallel PPL implementation (windows system only)
    4. PARALLEL_IMPLEMENTATION_OPENMP     - parallel OpenMP implementation */


#if defined(WIN32) || (_WIN32) || (_WIN64)
#define PARALLEL_IMPLEMENTATION_PPL
#else
#define PARALLEL_IMPLEMENTATION_ASYNC_POOL
#endif


#if defined(PARALLEL_IMPLEMENTATION_PPL)
#include <ppl.h>
#endif


namespace pyclustering {

namespace parallel {


/* Pool of threads is used to prevent overhead in case of nested loop */
static const std::size_t AMOUNT_HARDWARE_THREADS = std::thread::hardware_concurrency();
static const std::size_t AMOUNT_THREADS = (AMOUNT_HARDWARE_THREADS > 1) ? (AMOUNT_HARDWARE_THREADS - 1) : 0;
static std::vector<std::future<void>> FUTURE_STORAGE(AMOUNT_THREADS);
static std::vector<spinlock> FUTURE_LOCKS(AMOUNT_THREADS);


template <typename TypeIndex, typename TypeAction>
void parallel_for(const TypeIndex p_start, const TypeIndex p_end, const TypeAction & p_task) {
#if defined(PARALLEL_IMPLEMENTATION_ASYNC_POOL)
    const TypeIndex step = (p_end - p_start) / (AMOUNT_THREADS + 1);
    TypeIndex current_start = p_start;
    TypeIndex current_end = p_start + step;

    std::vector<std::size_t> captured_feature;

    for (std::size_t i = 0; i < AMOUNT_THREADS; ++i) {
        const auto async_task = [&p_task, current_start, current_end](){
            for (TypeIndex i = current_start; i < current_end; ++i) {
                p_task(i);
            }
        };

        std::size_t free_index = (std::size_t) -1;
        for (std::size_t i = 0; i < AMOUNT_THREADS; i++) {
            if (FUTURE_LOCKS[i].try_lock()) {
                free_index = i;
                break;
            }
        }

        if (free_index != (std::size_t) -1) {
            FUTURE_STORAGE[free_index] = std::async(std::launch::async, async_task);
            captured_feature.push_back(free_index);
        }
        else {
            async_task();
        }

        current_start = current_end;
        current_end += step;
    }

    for (TypeIndex i = current_start; i < p_end; ++i) {
        p_task(i);
    }

    for (auto index_feature : captured_feature) {
        FUTURE_STORAGE[index_feature].get();
        FUTURE_LOCKS[index_feature].unlock();
    }
#elif defined(PARALLEL_IMPLEMENTATION_PPL)
    concurrency::parallel_for(p_start, p_end, p_task);
#elif defined(PARALLEL_IMPLEMENTATION_OPENMP)
    #pragma omp parallel for
    for (TypeIndex i = p_start; i < p_end, i++) {
        p_task(i);
    }
#else
    for (std::size_t i = p_start; i < p_end; i++) {
        p_task(i);
    }
#endif
}


template <typename TypeIter, typename TypeAction>
void parallel_for_each(const TypeIter p_begin, const TypeIter p_end, const TypeAction & p_task) {
#if defined(PARALLEL_IMPLEMENTATION_ASYNC_POOL)
    const std::size_t step = std::distance(p_begin, p_end) / (AMOUNT_THREADS + 1);

    auto current_start = p_begin;
    auto current_end = p_begin + step;

    std::vector<std::size_t> captured_feature;

    for (std::size_t i = 0; i < AMOUNT_THREADS; ++i) {
        auto async_task = [&p_task, current_start, current_end](){
            for (auto iter = current_start; iter != current_end; ++iter) {
                p_task(*iter);
            }
        };

        std::size_t free_index = (std::size_t) -1;
        for (std::size_t i = 0; i < AMOUNT_THREADS; i++) {
            if (FUTURE_LOCKS[i].try_lock()) {
                free_index = i;
                break;
            }
        }

        if (free_index != (std::size_t) -1) {
            FUTURE_STORAGE[free_index] = std::async(std::launch::async, async_task);
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
        FUTURE_STORAGE[index_feature].get();
        FUTURE_LOCKS[index_feature].unlock();
    }
#elif defined(PARALLEL_IMPLEMENTATION_PPL)
    concurrency::parallel_for_each(p_begin, p_end, p_task);
#else
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