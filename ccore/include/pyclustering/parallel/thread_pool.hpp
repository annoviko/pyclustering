/*!

@authors Andrei Novikov (pyclustering@yandex.ru)
@date 2014-2020
@copyright BSD-3-Clause

*/


#pragma once


#include <deque>
#include <vector>

#include <pyclustering/parallel/thread_executor.hpp>


namespace pyclustering {

namespace parallel {


/*!

@class      thread_pool thread_pool.hpp pyclustering/parallel/thread_pool.hpp

@brief      Thread pool provides service to execute client tasks asynchronously in parallel way.

*/
class thread_pool {
public:
    /*!
    
    @brief  Defines shared pointer of the thread pool.
    
    */
    using ptr              = std::shared_ptr<thread_pool>;

private:
    using thread_container = std::vector<thread_executor::ptr>;

public:
    static const std::size_t        DEFAULT_AMOUNT_THREADS;     /**< Default amount of threads. */
    static const std::size_t        DEFAULT_POOL_SIZE;          /**< Default size of the thread pool. */

private:
    thread_container                m_pool  = { };

    std::deque<task::ptr>           m_queue = { };

    mutable std::mutex              m_common_mutex;

    std::condition_variable         m_queue_not_empty_cond;

    std::size_t                     m_free = 0;
    std::size_t                     m_reserve = 0;
    bool                            m_stop = false;

public:
    /*!

    @brief  Default constructor of the thread pool.

    */
    thread_pool();

    /*!

    @brief  Constructor of the thread pool where specific size of the pool is specified.

    @param[in] p_size: amount of threads in the pool that are going to be used for processing.

    */
    explicit thread_pool(const std::size_t p_size);

    /*!

    @brief  Default copy constructor of the thread pool.

    */
    thread_pool(const thread_pool & p_pool) = delete;

    /*!

    @brief  Default move constructor of the thread pool.

    */
    thread_pool(thread_pool && p_pool) = delete;

    /*!

    @brief  Default destructor of the thread pool.

    */
    ~thread_pool();

public:
    /*!

    @brief  Add new task for execution to the current thread pool.

    @param[in] p_raw_task: task with signature `void()` that should be executed.

    @return Shared pointer to the task that is going to be executed.

    */
    task::ptr add_task(const task::proc & p_raw_task);

    /*!

    @brief  Add new task for execution to the current thread pool if there is enough capacity to serve it without delay.

    @param[in] p_raw_task: task with signature `void()` that should be executed.

    @return Shared pointer to the task that is going to be executed if there is enough capacity, otherwise `nullptr`.

    */
    task::ptr add_task_if_free(const task::proc & p_raw_task);

    /*!

    @brief  Returns amount of tasks in the current thread pool.

    @return Amount of tasks in the current thread pool.

    */
    std::size_t size() const;

private:
    void initialize(const std::size_t p_size);

    void get_task(task::ptr & p_task);
};


}

}
