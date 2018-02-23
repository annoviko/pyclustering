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


#include "thread_pool.hpp"

#include "task.hpp"


namespace ccore {

namespace parallel {


const std::size_t   thread_pool::DEFAULT_POOL_SIZE =
        (std::thread::hardware_concurrency() > 1) ? std::thread::hardware_concurrency() : 4;


thread_pool::thread_pool(void) {
    initialize(DEFAULT_POOL_SIZE);
}


thread_pool::thread_pool(const std::size_t p_size) {
    initialize(p_size);
}


thread_pool::~thread_pool(void) {
    {
        std::lock_guard<std::mutex> lock_common(m_common_mutex);
        m_stop = true;
    }

    m_queue_not_empty_cond.notify_all();

    for (auto executor : m_pool) {
        executor->stop();
    }
}


task::id thread_pool::add_task(task::proc & p_raw_task) {
    std::size_t task_id = task::INVALID_TASK_ID;

    {
        std::lock_guard<std::mutex> lock_common(m_common_mutex);

        task::ptr client_task(new task(p_raw_task));
        task_id = client_task->get_id();

        m_queue.push_back(client_task);
    }

    m_queue_not_empty_cond.notify_one();

    return task_id;
}


std::size_t thread_pool::size(void) const {
    return m_pool.size();
}


task::id thread_pool::pop_complete_task(void) {
    std::unique_lock<std::mutex> lock_common(m_common_mutex);

    if ( (m_free == m_pool.size()) && m_done.empty() && m_queue.empty() ) {
        return task::INVALID_TASK_ID;
    }
    else {
        while (m_done.empty()) {
            m_done_not_empty_cond.wait(lock_common, [this]{ return !m_done.empty(); });
        }

        std::size_t complete_task_id = m_done.front()->get_id();
        m_done.pop_front();

        return complete_task_id;
    }
}


void thread_pool::initialize(const std::size_t p_size) {
    m_pool  = { };
    m_queue = { };
    m_done  = { };
    m_free  = 0;
    m_stop  = false;

    thread_executor::task_getter getter = std::bind(&thread_pool::get_task, this, std::placeholders::_1);
    thread_executor::task_notifier notifier = std::bind(&thread_pool::done_task, this, std::placeholders::_1);

    for (std::size_t index = 0; index < p_size; index++) {
        m_pool.emplace_back(new thread_executor(getter, notifier));
        m_free++;
    }
}


void thread_pool::done_task(const task::ptr & p_task) {
    {
        std::unique_lock<std::mutex> lock_common(m_common_mutex);
        m_done.push_back(p_task);
        m_free++;
    }

    m_done_not_empty_cond.notify_one();
}


void thread_pool::get_task(task::ptr & p_task) {
    std::unique_lock<std::mutex> lock_common(m_common_mutex);

    p_task = nullptr;

    while(m_queue.empty() && !m_stop) {
        m_queue_not_empty_cond.wait(lock_common, [this]{ return !m_queue.empty() || m_stop; });
    }

    if (!m_queue.empty()) {
        p_task = m_queue.front();
        m_queue.pop_front();
        m_free--;
    }
}


}

}
