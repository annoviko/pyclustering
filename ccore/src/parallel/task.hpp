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


#include <condition_variable>
#include <functional>
#include <list>
#include <memory>
#include <mutex>


namespace ccore {

namespace parallel {


enum class task_status {
    NOT_READY,
    READY
};


class thread_executor;


class task {
public:
    friend thread_executor;

public:
    using proc      = std::function<void(void)>;
    using ptr       = std::shared_ptr<task>;
    using id        = std::size_t;

private:
    proc                              m_task          = proc();
    task_status                       m_status        = task_status::NOT_READY;

    mutable std::mutex                m_status_mutex;
    mutable std::condition_variable   m_status_ready_cond;

public:
    task(void) = default;

    explicit task(const proc & p_task);

    task(const task & p_other) = default;

    task(task && p_other) = default;

    ~task(void) = default;

private:
    void set_status(const task_status p_status);

public:
    void wait_ready(void) const;

public:
    void operator()();
};


}

}
