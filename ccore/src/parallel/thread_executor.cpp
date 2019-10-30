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


#include <pyclustering/parallel/thread_executor.hpp>

#include <exception>


namespace pyclustering {

namespace parallel {


thread_executor::thread_executor(const task_getter & p_getter) :
    m_stop(false),
    m_getter(p_getter),
    m_executor(&thread_executor::run, this)
{ }


void thread_executor::run() {
    while(!m_stop) {
        task::ptr task = nullptr;
        m_getter(task);

        if (task) {
            (*task)();
            task->set_ready();
        }
        else {
            m_stop = true;
        }
    }
}


void thread_executor::stop() {
    m_stop = true;

    if (m_executor.joinable()) {
        m_executor.join();
    }
}


}

}
