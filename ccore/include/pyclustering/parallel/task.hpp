/*!

@authors Andrei Novikov (pyclustering@yandex.ru)
@date 2014-2020
@copyright BSD-3-Clause

*/



#pragma once


#include <condition_variable>
#include <functional>
#include <list>
#include <memory>
#include <mutex>

#include <pyclustering/parallel/spinlock.hpp>


namespace pyclustering {

namespace parallel {


class thread_executor;


/*

@class      task task.hpp pyclustering/parallel/task.hpp

@brief      Defines a task for thread pool that should be executed.
@details    The executed task is marked as a ready-task.

@see thread_pool

*/
class task {
    friend thread_executor;

public:
    /*!

    @brief  Defines a task for the thread pool and should have the following signature `void()`.

    */
    using proc      = std::function<void()>;

    /*!

    @brief  Defines shared pointer to the task.

    */
    using ptr       = std::shared_ptr<task>;

    /*!

    @brief  Defines ID type of the task.

    */
    using id        = std::size_t;

private:
    proc                m_task          = proc();
    mutable spinlock    m_ready;

public:
    /*!

    @brief  Default task constructor.

    */
    task() = default;

    /*!

    @brief  Constructor of the task where actions are defined by an input function with `void()` signature.

    @param[in] p_task: function with `void()` signature that should executed.

    */
    explicit task(const proc & p_task);

    /*!

    @brief  Default copy constructor of the task.

    */
    task(const task & p_other) = default;

    /*!

    @brief  Default move constructor of the task.

    */
    task(task && p_other) = default;

    /*!

    @brief  Default desctructor of the task.

    */
    ~task() = default;

private:
    /*!

    @brief  Marks the current task as complited.

    */
    void set_ready();

public:
    /*!

    @brief  Blocks until the current task is complited.

    */
    void wait_ready() const;

public:
    /*!

    @brief  Runs execution of the current task.

    */
    void operator()();
};


}

}
