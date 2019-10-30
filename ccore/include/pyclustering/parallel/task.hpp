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
#include <functional>
#include <list>
#include <memory>
#include <mutex>

#include <pyclustering/parallel/spinlock.hpp>


namespace pyclustering {

namespace parallel {


class thread_executor;


class task {
public:
    friend thread_executor;

public:
    using proc      = std::function<void()>;
    using ptr       = std::shared_ptr<task>;
    using id        = std::size_t;

private:
    proc                m_task          = proc();
    mutable spinlock    m_ready;

public:
    task() = default;

    explicit task(const proc & p_task);

    task(const task & p_other) = default;

    task(task && p_other) = default;

    ~task() = default;

private:
    void set_ready();

public:
    void wait_ready() const;

public:
    void operator()();
};


}

}
