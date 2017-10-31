#include "thread_executor.hpp"


#include <iostream>


thread_executor::thread_executor(const observer & p_callback) : thread_executor() {
    m_callback = p_callback;
}


thread_executor::~thread_executor(void) {
    stop();
}


bool thread_executor::execute(const task::ptr p_task) {
    if ((m_task != nullptr) || !m_idle.load()) {
        return false;
    }

    m_task = p_task;
    m_idle.store(false);

    m_event_arrive.notify_one();

    return true;
}


bool thread_executor::is_idle(void) const {
    return m_idle.load();
}


void thread_executor::run(void) {
    while(!m_stop.load()) {
        std::cout << "New life cycle is started of the thread '" << std::this_thread::get_id() << "'." << std::endl;

        if (m_task != nullptr) {
            std::cout << "Start task processing '" << std::this_thread::get_id() << "'." << std::endl;

            (*m_task)();

            m_task->set_status(task_status::READY);

            if (m_callback) {
                m_callback(m_task);
            }

            m_task = nullptr;
            m_idle.store(true);
        }


        std::unique_lock<std::mutex> lock_event(m_block);
        m_event_arrive.wait(lock_event, [this]{ return (m_stop.load()) || (m_task != nullptr); });

        std::cout << "Event is received by '" << std::this_thread::get_id() << "'." << std::endl;
    }
}


void thread_executor::stop(void) {
    m_stop.store(true);

    m_event_arrive.notify_one();
    m_executor.join();
}