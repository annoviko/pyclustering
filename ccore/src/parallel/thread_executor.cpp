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


#include "thread_executor.hpp"

#include <exception>


namespace parallel {


thread_executor::thread_executor(const task_conveyor & p_conveyor) : thread_executor() {
    m_conveyor  = p_conveyor;
}


thread_executor::~thread_executor(void) {
    stop();
}


bool thread_executor::execute(const task::ptr p_task) {
    std::unique_lock<std::mutex> lock_event(m_block);

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
        while (m_task != nullptr) {
            (*m_task)();

            m_task->set_status(task_status::READY);

            m_conveyor(m_task, m_task);
        }

        m_idle.store(true);

        std::unique_lock<std::mutex> lock_event(m_block);
        m_event_arrive.wait(lock_event, [this]{ return (m_stop.load()) || (m_task != nullptr); });
    }
}


void thread_executor::stop(void) {
    m_stop.store(true);

    m_event_arrive.notify_one();
    m_executor.join();
}


}