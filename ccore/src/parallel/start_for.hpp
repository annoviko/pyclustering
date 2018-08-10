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


#include <future>
#include <thread>
#include <vector>

#include "spinlock.hpp"


namespace ccore {

namespace parallel {


class start_for {
public:
    static const std::size_t UNAVAILABLE_THREAD;

private:
    static const std::size_t AMOUNT_HARDWARE_THREADS;
    static const std::size_t AMOUNT_THREADS;

private:
    static std::vector<std::future<void>> FUTURE_STORAGE;
    static std::vector<spinlock> FUTURE_LOCKS;

public:
    start_for(void) = default;

    start_for(const start_for & p_other) = default;

    start_for(start_for && p_other) = default;

    ~start_for(void) = default;

public:
    template <typename TypeAction>
    static std::size_t try_execute(const TypeAction & p_action) {
        std::size_t free_index = UNAVAILABLE_THREAD;
        for (std::size_t i = 0; i < AMOUNT_THREADS; i++) {
            if (FUTURE_LOCKS[i].try_lock()) {
                auto future_result = std::async(std::launch::async, p_action);
                FUTURE_STORAGE[free_index] = std::move(future_result);

                break;
            }
        }

        return free_index;
    }

    static std::size_t get_size(void);

    static void wait(const std::size_t p_index);
};


}

}