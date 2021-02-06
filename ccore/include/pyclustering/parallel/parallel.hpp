/*!

@authors Andrei Novikov (pyclustering@yandex.ru)
@date 2014-2020
@copyright BSD-3-Clause

*/


#pragma once


#include <algorithm>
#include <cstddef>
#include <functional>
#include <future>
#include <vector>


#if defined(WIN32) || (_WIN32) || (_WIN64)
#define PARALLEL_IMPLEMENTATION_ASYNC_POOL  /* 'PARALLEL_IMPLEMENTATION_ASYNC_POOL' demostrates more efficiency than 'PARALLEL_IMPLEMENTATION_PPL' in scope of the pyclustering library. */
#else
#define PARALLEL_IMPLEMENTATION_ASYNC_POOL
#endif


#if defined(PARALLEL_IMPLEMENTATION_PPL)
#include <ppl.h>
#endif


namespace pyclustering {

namespace parallel {


/* Pool of threads is used to prevent overhead in case of nested loop */
const std::size_t AMOUNT_HARDWARE_THREADS = std::thread::hardware_concurrency();
const std::size_t AMOUNT_THREADS = (AMOUNT_HARDWARE_THREADS > 1) ? (AMOUNT_HARDWARE_THREADS - 1) : 0;


/*!

@brief Parallelizes for-loop using all available cores.
@details `parallel_for` uses PPL in case of Windows operating system and own implemention that is based
          on pure C++ functionality for concurency such as `std::future` and `std::async`.

Advanced uses might use one of the define to use specific implementation of the `parallel_for` loop:
1. PARALLEL_IMPLEMENTATION_ASYNC_POOL - own parallel implementation based on `std::async` pool.
2. PARALLEL_IMPLEMENTATION_NONE       - parallel implementation is not used.
3. PARALLEL_IMPLEMENTATION_PPL        - parallel PPL implementation (windows system only).
4. PARALLEL_IMPLEMENTATION_OPENMP     - parallel OpenMP implementation.

@param[in] p_start: initial value for the loop.
@param[in] p_end: final value of the loop - calculations are performed until the current counter value is less than the final value `i < p_end`.
@param[in] p_step: step that is used to iterate over the loop.
@param[in] p_task: body of the loop that defines actions that should be done on each iteration.
@param[in] p_threads: amount of threads that are going to be used for processing (by default the efficient amount of threads).

*/
template <typename TypeIndex, typename TypeAction>
void parallel_for(const TypeIndex p_start, const TypeIndex p_end, const TypeIndex p_step, const TypeAction & p_task, const std::size_t p_threads = AMOUNT_THREADS) {
#if defined(PARALLEL_IMPLEMENTATION_ASYNC_POOL)
    /*

    Microsoft `concurrency::parallel_for` implementation does not support negative step. The cite from the documentation about `concurrency::parallel_for`.
    The loop iteration must be forward. The parallel_for algorithm throws an exception of type std::invalid_argument if the _Step parameter is less than 1.

    Therefore let's support the same behavior.

    */

    if (p_end < p_start) {
        throw std::invalid_argument("Start index '" + std::to_string(p_start) + "' is greater than end '" + std::to_string(p_end) + "'.");
    }

    const TypeIndex interval_length = p_end - p_start;  /* Full interval to process */

    if (interval_length == 0) {
        return;     /* There are no work for threads. */
    }

    if ((interval_length > 0) && (interval_length <= p_step)) {
        p_task(p_start);    /* There is only one iteration in the loop. */
        return;
    }

    TypeIndex interval_thread_length = interval_length / p_step / static_cast<TypeIndex>(p_threads);    /* How many iterations should be performed by each thread */
    if (interval_thread_length < p_step)  {
        interval_thread_length = p_step;
    }
    else if (interval_thread_length % p_step != 0) {
        interval_thread_length = interval_thread_length - (interval_thread_length % p_step);
    }

    TypeIndex current_start = p_start;
    TypeIndex current_end = p_start + interval_thread_length;

    std::vector<std::future<void>> future_storage;
    future_storage.reserve(p_threads);

    /* 

    It is possible that there are not enough work for all threads, lets check that we are not out of range.

    */
    for (std::size_t i = 0; (i < static_cast<TypeIndex>(p_threads) - 1) && (current_end < p_end); ++i) {
        const auto async_task = [&p_task, current_start, current_end, p_step](){
            for (TypeIndex i = current_start; i < current_end; i += p_step) {
                p_task(i);
            }
        };
        /* There was an optimization for nested 'parallel_for' loops, but the maximum depth in the current library is 2.
           If the optimization is needed - get it from repository (versions that are <= 0.10.0.1). */
        future_storage.push_back(std::async(std::launch::async, async_task));

        current_start = current_end;
        current_end += interval_thread_length;
    }

    for (TypeIndex i = current_start; i < p_end; i += p_step) {
        p_task(i);
    }

    for (auto & feature : future_storage) {
        feature.get();
    }
#elif defined(PARALLEL_IMPLEMENTATION_PPL)
    (void) p_threads;
    concurrency::parallel_for(p_start, p_end, p_step, p_task);
#elif defined(PARALLEL_IMPLEMENTATION_OPENMP)
    #pragma omp parallel for
    for (TypeIndex i = p_start; i < p_end, i += p_step) {
        p_task(i);
    }
#else
    for (std::size_t i = p_start; i < p_end; i += p_step) {
        p_task(i);
    }
#endif
}


/*!

@brief Parallelizes for-loop using all available cores.
@details `parallel_for` uses PPL in case of Windows operating system and own implemention that is based
on pure C++ functionality for concurency such as `std::future` and `std::async`.

Advanced uses might use one of the define to use specific implementation of the `parallel_for` loop:
1. PARALLEL_IMPLEMENTATION_ASYNC_POOL - own parallel implementation based on `std::async` pool.
2. PARALLEL_IMPLEMENTATION_NONE       - parallel implementation is not used.
3. PARALLEL_IMPLEMENTATION_PPL        - parallel PPL implementation (windows system only).
4. PARALLEL_IMPLEMENTATION_OPENMP     - parallel OpenMP implementation.

@param[in] p_start: initial value for the loop.
@param[in] p_end: final value of the loop - calculations are performed until current counter value is less than final value `i < p_end`.
@param[in] p_task: body of the loop that defines actions that should be done on each iteration.

*/
template <typename TypeIndex, typename TypeAction>
void parallel_for(const TypeIndex p_start, const TypeIndex p_end, const TypeAction & p_task) {
    parallel_for(p_start, p_end, std::size_t(1), p_task);
}


/*!

@brief Parallelizes for-each-loop using all available cores.
@details `parallel_each` uses PPL in case of Windows operating system and own implemention that is based
          on pure C++ functionality for concurency such as `std::future` and `std::async`.

Advanced uses might use one of the define to use specific implementation of the `parallel_for_each` loop:
1. PARALLEL_IMPLEMENTATION_ASYNC_POOL - own parallel implementation based on `std::async` pool.
2. PARALLEL_IMPLEMENTATION_NONE       - parallel implementation is not used.
3. PARALLEL_IMPLEMENTATION_PPL        - parallel PPL implementation (windows system only).
4. PARALLEL_IMPLEMENTATION_OPENMP     - parallel OpenMP implementation.

@param[in] p_begin: initial iterator from that the loop starts.
@param[in] p_end: end iterator that defines when the loop should stop `iter != p_end`.
@param[in] p_task: body of the loop that defines actions that should be done for each element.
@param[in] p_threads: amount of threads that are going to be used for processing (by default the efficient amount of threads).

*/
template <typename TypeIter, typename TypeAction>
void parallel_for_each(const TypeIter p_begin, const TypeIter p_end, const TypeAction & p_task, const std::size_t p_threads = AMOUNT_THREADS) {
#if defined(PARALLEL_IMPLEMENTATION_ASYNC_POOL)
    const std::size_t interval_length = std::distance(p_begin, p_end);

    if (interval_length == 0) {
        return;
    }

    if (interval_length == 1) {
        p_task(*p_begin);
        return;
    }

    const std::size_t step = std::max(interval_length / p_threads, std::size_t(1));

    std::size_t amount_threads = static_cast<std::size_t>(interval_length / step);
    if (amount_threads > p_threads) {
        amount_threads = p_threads;
    }
    else if (amount_threads > 0) {
        amount_threads--;   /* current thread is also considered. */
    }

    auto current_start = p_begin;
    auto current_end = p_begin + step;

    std::vector<std::future<void>> future_storage(amount_threads);

    for (std::size_t i = 0; i < amount_threads; ++i) {
        auto async_task = [&p_task, current_start, current_end](){
            for (auto iter = current_start; iter != current_end; ++iter) {
                p_task(*iter);
            }
        };

        future_storage[i] = std::async(std::launch::async, async_task);

        current_start = current_end;
        current_end += step;
    }

    for (auto iter = current_start; iter != p_end; ++iter) {
        p_task(*iter);
    }

    for (auto & feature : future_storage) {
        feature.get();
    }
#elif defined(PARALLEL_IMPLEMENTATION_PPL)
    (void) p_threads;
    concurrency::parallel_for_each(p_begin, p_end, p_task);
#else
    for (auto iter = p_begin; iter != p_end; ++iter) {
        p_task(*iter);
    }
#endif
}


/*!

@brief Parallelizes for-each-loop using all available cores.
@details `parallel_each` uses PPL in case of Windows operating system and own implemention that is based
          on pure C++ functionality for concurency such as `std::future` and `std::async`.

@param[in] p_container: iterable container that should be processed.
@param[in] p_task: body of the loop that defines actions that should be done for each element.

*/
template <typename TypeContainer, typename TypeAction>
void parallel_for_each(const TypeContainer & p_container, const TypeAction & p_task) {
    parallel_for_each(std::begin(p_container), std::end(p_container), p_task);
}


}

}