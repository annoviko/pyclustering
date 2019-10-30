/**
*
* @authors Andrei Novikov (pyclustering@yandex.ru)
* @date 2014-2019
* @copyright GNU Public License
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


#include <pyclustering/parallel/thread_pool.hpp>

#include <pyclustering/parallel/task.hpp>


namespace pyclustering {

namespace parallel {


const std::size_t   thread_pool::DEFAULT_AMOUNT_THREADS = 4;

const std::size_t   thread_pool::DEFAULT_POOL_SIZE =
        (std::thread::hardware_concurrency() > 1) ? std::thread::hardware_concurrency() : DEFAULT_AMOUNT_THREADS;


thread_pool::thread_pool() {
    initialize(DEFAULT_POOL_SIZE);
}


thread_pool::thread_pool(const std::size_t p_size) {
    initialize(p_size);
}


thread_pool::~thread_pool() {
    {
        std::lock_guard<std::mutex> lock_common(m_common_mutex);
        m_stop = true;
    }

    m_queue_not_empty_cond.notify_all();

    for (auto executor : m_pool) {
        executor->stop();
    }
}


task::ptr thread_pool::add_task(const task::proc & p_raw_task) {
    task::ptr client_task = std::make_shared<task>(p_raw_task);

    {
        std::lock_guard<std::mutex> lock_common(m_common_mutex);

        m_queue.push_back(client_task);
    }

    m_queue_not_empty_cond.notify_one();

    return client_task;
}


task::ptr thread_pool::add_task_if_free(const task::proc & p_raw_task) {
    task::ptr client_task = nullptr;

    {
        std::lock_guard<std::mutex> lock_common(m_common_mutex);

        if (m_reserve > 0) {
            client_task = std::make_shared<task>(p_raw_task);

            m_queue.push_back(client_task);

            m_queue_not_empty_cond.notify_one();

            m_reserve--;
        }
    }

    return client_task;
}


std::size_t thread_pool::size() const {
    return m_pool.size();
}


void thread_pool::initialize(const std::size_t p_size) {
    m_pool    = { };
    m_queue   = { };
    m_stop    = false;

    thread_executor::task_getter getter = std::bind(&thread_pool::get_task, this, std::placeholders::_1);

    for (std::size_t index = 0; index < p_size; index++) {
        m_pool.emplace_back(std::make_shared<thread_executor>(getter));
    }

    m_reserve = m_free = p_size;
}


void thread_pool::get_task(task::ptr & p_task) {
    std::unique_lock<std::mutex> lock_common(m_common_mutex);

    p_task = nullptr;

    m_reserve++;
    m_free++;

    while(m_queue.empty() && !m_stop) {
        m_queue_not_empty_cond.wait(lock_common, [this]{ return !m_queue.empty() || m_stop; });
    }

    if (!m_queue.empty()) {
        p_task = m_queue.front();
        m_queue.pop_front();

        if (m_reserve == m_free) {
            m_reserve--;
        }

        m_free--;
    }
}


}

}
