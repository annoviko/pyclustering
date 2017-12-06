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
#include <condition_variable>
#include <thread>

#include "task.hpp"


namespace parallel {


class thread_executor {
public:
    using task_conveyor = std::function<void(task::ptr, task::ptr &)>;

    using ptr           = std::shared_ptr<thread_executor>;

private:
    task::ptr               m_task          = nullptr;
    std::atomic<bool>       m_idle          { true };
    std::atomic<bool>       m_stop          { false };

    task_conveyor           m_conveyor      = nullptr;

    std::condition_variable m_event_arrive;
    std::mutex              m_block;
    std::thread             m_executor      = std::thread(&thread_executor::run, this);

public:
    thread_executor(void) = default;

    explicit thread_executor(const task_conveyor & p_conveyor);

    thread_executor(const thread_executor & p_other) = delete;

    thread_executor(thread_executor && p_other) = delete;

    ~thread_executor(void);

public:
    bool execute(const task::ptr p_task);

    bool is_idle(void) const;

private:
    void run(void);

    void stop(void);
};


}