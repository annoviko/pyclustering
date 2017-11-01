/**
*
* Copyright (C) 2014-2017    Andrei Novikov (pyclustering@yandex.ru)
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


namespace parallel {


thread_pool::thread_pool(const std::size_t p_size) : thread_pool() {
    thread_executor::task_conveyor observer = std::bind(&thread_pool::task_conveyor, this, std::placeholders::_1, std::placeholders::_2);
    for (std::size_t index = 0; index < p_size; index++) {
        m_pool.emplace_back(new thread_executor(observer));
        m_free.fetch_add(1);
    }
}


std::size_t thread_pool::add_task(task::proc & p_raw_task) {
    std::lock_guard<std::mutex> locker(m_general_mutex);

    task::ptr client_task(new task(p_raw_task));

    for(auto & executor : m_pool) {
        if (executor->is_idle()) {
            executor->execute(client_task);
            m_free.fetch_sub(1, std::memory_order_release);

            return client_task->get_id();
        }
    }

    m_queue.push_back(client_task);

    return client_task->get_id();
}


std::size_t thread_pool::size(void) const {
    return m_pool.size();
}


std::size_t thread_pool::pop_complete_task(void) {
    std::unique_lock<std::mutex> lock_event(m_general_mutex);

    if ( (m_free.load() == m_pool.size()) && m_done.empty() && m_queue.empty() ) {
        return task::INVALID_TASK_ID;
    }
    else {
        while(m_done.empty()) {
            m_event.wait(lock_event, [this]{ return !m_done.empty(); });
        }

        std::size_t complete_task_id = m_done.front()->get_id();
        m_done.pop_front();

        return complete_task_id;
    }
}


void thread_pool::task_conveyor(const task::ptr p_task, task::ptr & p_next_task) {
    std::lock_guard<std::mutex> locker(m_general_mutex);

    m_done.push_back(p_task);
    m_free.fetch_add(1);

    m_event.notify_one();


    p_next_task = nullptr;
    if (!m_queue.empty()) {
        p_next_task = m_queue.front();
        m_queue.pop_front();

        m_free.fetch_sub(1);
    }
}


}