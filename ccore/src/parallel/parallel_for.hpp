#pragma once


#include <cstddef>
#include <functional>
#include <future>
#include <vector>


#include <iostream>


/* Available options: PARALLEL_IMPLEMENTATION_CCORE, PARALLEL_IMPLEMENTATION_NONE */
#define PARALLEL_IMPLEMENTATION_CCORE



namespace ccore {

namespace parallel {


template <typename TypeAction>
void parallel_for(std::size_t p_start, std::size_t p_end, const TypeAction & p_task) {
#if defined(PARALLEL_IMPLEMENTATION_CCORE)
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
            std::cout << "[DEBUG] (parallel_for) std::async throws exception." << std::endl;
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
#else
    /* This part of code is switched only to estimate parallel implementation of any algorithm with non-parallel.
       Never switch on for real product. */
    for (std::size_t i = p_start; i < p_end; i++) {
        p_task(i);
    }
#endif
}


template <typename TypeIter, typename TypeAction>
void parallel_for_each(const TypeIter p_begin, const TypeIter p_end, const TypeAction & p_task) {
#if defined(PARALLEL_IMPLEMENTATION_CCORE)
    static const std::size_t amount_hardware_threads = std::thread::hardware_concurrency();
    static const std::size_t amount_threads = (amount_hardware_threads > 1) ? (amount_hardware_threads - 1) : 1;

    std::vector<std::future<void>> future_storage(amount_threads);

    const std::size_t step = std::distance(p_begin, p_end) / (amount_threads + 1);

    auto current_start = p_begin;
    auto current_end = p_begin + step;

    for (std::size_t i = 0; i < amount_threads; ++i) {
        std::future<void> future_result;
        auto async_task = [&p_task, current_start, current_end](){
            for (auto iter = current_start; iter != current_end; ++iter) {
                p_task(*iter);
            }
        };

        try {
            future_result = std::async(std::launch::async, async_task);
        }
        catch(std::system_error &) {
            std::cout << "[DEBUG] (parallel_for_each) std::async throws exception." << std::endl;
            future_result = std::async(std::launch::async | std::launch::deferred, async_task);
        }

        future_storage[i] = std::move(future_result);

        current_start = current_end;
        current_end += step;
    }

    for (auto iter = current_start; iter != p_end; ++iter) {
        p_task(*iter);
    }

    for (auto & result : future_storage) {
        result.get();
    }
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