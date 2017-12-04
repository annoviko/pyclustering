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


#include <functional>
#include <list>
#include <memory>


namespace parallel {


enum class task_status {
    PENDING,
    PROCESSING,
    READY
};



class task {
public:
    const static std::size_t    INVALID_TASK_ID;

public:
    using proc      = std::function<void(void)>;
    using ptr       = std::shared_ptr<task>;

private:
    static std::size_t          STATIC_TASK_ID_GENERATOR;

private:
    std::size_t                 m_id        = generate_task_id();
    proc                        m_task      = proc();
    task_status                 m_status    = task_status::PENDING;

public:
    task(void) = default;

    explicit task(const proc & p_task);

    task(const task & p_other) = default;

    task(task && p_other) = default;

    ~task(void) = default;

public:
    void set_status(const task_status p_status);

    task_status get_status(void) const;

    std::size_t get_id(void) const;

private:
    static std::size_t generate_task_id(void);

public:
    void operator()();
};


}