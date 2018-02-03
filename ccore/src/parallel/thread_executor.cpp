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


#include "thread_executor.hpp"

#include <exception>


namespace ccore {

namespace parallel {


thread_executor::thread_executor(const task_getter & p_getter, const task_notifier & p_notifier) {
    m_stop        = false;

    m_getter      = p_getter;
    m_notifier    = p_notifier;
    m_executor    = std::thread(&thread_executor::run, this);
}


void thread_executor::run(void) {
    while(!m_stop) {
        task::ptr task = nullptr;
        m_getter(task);

        if (task) {
            task->set_status(task_status::PROCESSING);
            (*task)();
            task->set_status(task_status::READY);

            m_notifier(task);
        }
        else {
            m_stop = true;
        }
    }
}


void thread_executor::stop(void) {
    m_stop = true;

    if (m_executor.joinable()) {
        m_executor.join();
    }
}


}

}
