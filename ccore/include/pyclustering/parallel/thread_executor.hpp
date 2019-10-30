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


#pragma once


#include <condition_variable>
#include <thread>

#include <pyclustering/parallel/task.hpp>


namespace pyclustering {

namespace parallel {


class thread_executor {
public:
    using task_getter   = std::function<void(task::ptr &)>;
    using task_notifier = std::function<void(const task::ptr &)>;

    using ptr           = std::shared_ptr<thread_executor>;

private:
    bool                    m_stop            = true;
    task_getter             m_getter          = nullptr;
    std::thread             m_executor;

public:
    thread_executor() = default;

    explicit thread_executor(const task_getter & p_getter);

    thread_executor(const thread_executor & p_other) = delete;

    thread_executor(thread_executor && p_other) = delete;

    ~thread_executor() = default;

public:
    void stop();

private:
    void run();
};


}

}
