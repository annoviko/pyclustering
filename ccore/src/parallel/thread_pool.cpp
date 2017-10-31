#include "thread_pool.hpp"


thread_pool::thread_pool(const std::size_t p_size) : thread_pool() {
    thread_executor::observer observer = std::bind(&thread_pool::task_done, this, std::placeholders::_1);
    for (std::size_t index = 0; index < p_size; index++) {
        m_pool.emplace_back(new thread_executor(observer));
        m_free++;
    }
}


std::size_t thread_pool::add_task(task::proc & p_raw_task) {
    task::ptr task(new task(p_raw_task));

    for(auto & executor : m_pool) {
        if (executor->is_idle()) {
            executor->execute(task);
            m_free--;

            return task->get_id();
        }
    }

    m_queue.push_back(task);
}


std::size_t thread_pool::pop_complete_task(void) {
    if (m_free == m_pool.size()) {
        return task::INVALID_TASK_ID;
    }
    else {
        std::unique_lock<std::mutex> lock_event(m_mutex);
        while(m_done.empty()) {
            m_event.wait(lock_event, [this]{ return !m_done.empty(); });
        }

        std::size_t complete_task_id = m_done.front()->get_id();
        m_done.pop_front();

        return complete_task_id;
    }
}


void thread_pool::task_done(const task::ptr p_task) {
    std::lock_guard<std::mutex> lock(m_mutex);
    m_done.push_back(p_task);
    m_free++;

    m_event.notify_one();
}