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


#include "task.hpp"


namespace ccore {

namespace parallel {


task::task(const proc & p_task) :
    m_task(p_task),
    m_status(task_status::NOT_READY)
{ }


void task::set_status(const task_status p_status) {
    std::unique_lock<std::mutex> lock_status(m_status_mutex);

    m_status = p_status;
    m_status_ready_cond.notify_one();
}


void task::wait_ready(void) const {
    std::unique_lock<std::mutex> lock_status(m_status_mutex);

    while(m_status != task_status::READY) {
        m_status_ready_cond.wait(lock_status);
    }
}


void task::operator()() {
    m_task();
}


}

}
