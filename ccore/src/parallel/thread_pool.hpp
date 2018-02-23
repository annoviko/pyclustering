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


#pragma once


#include <atomic>
#include <deque>
#include <vector>

#include "thread_executor.hpp"


namespace ccore {

namespace parallel {


class thread_pool {
public:
    using ptr              = std::shared_ptr<thread_pool>;

private:
    using thread_container = std::vector<thread_executor::ptr>;

public:
    static const std::size_t        DEFAULT_POOL_SIZE;

private:
    thread_container                m_pool  = { };

    std::deque<task::ptr>           m_queue = { };

    std::deque<task::ptr>           m_done  = { };

    mutable std::mutex              m_common_mutex;

    std::condition_variable         m_queue_not_empty_cond;
    std::condition_variable         m_done_not_empty_cond;

    std::size_t                     m_free = 0;
    bool                            m_stop = false;

public:
    thread_pool(void);

    explicit thread_pool(const std::size_t p_size);

    thread_pool(const thread_pool & p_pool) = delete;

    thread_pool(thread_pool && p_pool) = delete;

    ~thread_pool(void);

public:
    task::id add_task(task::proc & p_raw_task);

    task::id pop_complete_task(void);

    std::size_t size(void) const;

private:
    void initialize(const std::size_t p_size);

    void done_task(const task::ptr & p_task);

    void get_task(task::ptr & p_task);
};


}

}
