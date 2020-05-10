/*!

@authors Andrei Novikov (pyclustering@yandex.ru)
@date 2014-2020
@copyright GNU Public License

@cond GNU_PUBLIC_LICENSE
    pyclustering is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    pyclustering is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
@endcond

*/


#pragma once


#include <condition_variable>
#include <thread>

#include <pyclustering/parallel/task.hpp>


namespace pyclustering {

namespace parallel {


/*!

@class      thread_executor thread_executor.hpp pyclustering/parallel/thread_executor.hpp

@brief      Task executor for the thread pool.
@details    Task executor is responsible for executing task in separate thread and for notification the thread pool about task readiness.

@see thread_pool

*/
class thread_executor {
public:
    /*!
    
    @brief  Defines function to get next task for execution from the thread pool.
    @details The signature of the getter function should have following signature void(task::ptr &)`.
    
    */
    using task_getter   = std::function<void(task::ptr &)>;

    /*!

    @brief  Defines shared pointer of the thread executor.

    */
    using ptr           = std::shared_ptr<thread_executor>;

private:
    bool                    m_stop            = true;
    task_getter             m_getter          = nullptr;
    std::thread             m_executor;

public:
    /*!

    @brief  Default constructor of the thread executor.

    */
    thread_executor() = default;

    /*!

    @brief  Constructor of the thread executor with the task getting function.

    @param[in] p_getter: function with signatire `void(task::ptr &)` that is used to get next task to execute.

    */
    explicit thread_executor(const task_getter & p_getter);

    /*!

    @brief  Default copy constructor of the thread executor.

    */
    thread_executor(const thread_executor & p_other) = delete;

    /*!

    @brief  Default move constructor of the thread executor.

    */
    thread_executor(thread_executor && p_other) = delete;

    /*!

    @brief  Default destructor of the thread executor.

    */
    ~thread_executor() = default;

public:
    /*!

    @brief  Terminates thread executor: stops current task and join thread of the executor.

    */
    void stop();

private:
    /*!

    @brief  Run thread executor.

    */
    void run();
};


}

}
