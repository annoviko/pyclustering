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


#pragma once


#include <atomic>
#include <deque>
#include <vector>

#include "thread_executor.hpp"


namespace parallel {


class thread_pool {
private:
    using thread_container = std::vector<thread_executor::ptr>;

private:
    thread_container                m_pool  = { };

    std::deque<task::ptr>           m_queue = { };

    std::deque<task::ptr>           m_done  = { };

    std::mutex                      m_general_mutex;

    std::condition_variable         m_event;

    std::atomic<std::size_t>        m_free    { 0 };

public:
    thread_pool(void) = default;

    explicit thread_pool(const std::size_t p_size);

    thread_pool(const thread_pool & p_pool) = delete;

    thread_pool(thread_pool && p_pool) = delete;

    ~thread_pool(void) = default;

public:
    std::size_t add_task(task::proc & p_raw_task);

    std::size_t pop_complete_task(void);

    std::size_t size(void) const;

private:
    void task_conveyor(const task::ptr p_task, task::ptr & p_next_task);
};


}