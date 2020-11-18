/*!

@authors Andrei Novikov (pyclustering@yandex.ru)
@date 2014-2020
@copyright BSD-3-Clause

*/


#include <pyclustering/parallel/thread_executor.hpp>

#include <exception>


namespace pyclustering {

namespace parallel {


thread_executor::thread_executor(const task_getter & p_getter) :
    m_stop(false),
    m_getter(p_getter),
    m_executor(&thread_executor::run, this)
{ }


void thread_executor::run() {
    while(!m_stop) {
        task::ptr task = nullptr;
        m_getter(task);

        if (task) {
            (*task)();
            task->set_ready();
        }
        else {
            m_stop = true;
        }
    }
}


void thread_executor::stop() {
    m_stop = true;

    if (m_executor.joinable()) {
        m_executor.join();
    }
}


}

}
