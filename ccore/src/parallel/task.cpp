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


const task::id    task::INVALID_TASK_ID              = (task::id) -1;

task::id          task::STATIC_TASK_ID_GENERATOR     = 0;


task::task(const proc & p_task) :
    m_id(generate_task_id()),
    m_task(p_task),
    m_status(task_status::PENDING)
{ }


void task::set_status(const task_status p_status) {
    m_status = p_status;
}


task_status task::get_status(void) const {
    return m_status;
}


task::id task::get_id(void) const {
    return m_id;
}


task::id task::generate_task_id(void) {
    if (++STATIC_TASK_ID_GENERATOR != task::INVALID_TASK_ID) {
        return STATIC_TASK_ID_GENERATOR;
    }

    return ++STATIC_TASK_ID_GENERATOR;
}


void task::operator()() {
    m_task();
}


}

}
