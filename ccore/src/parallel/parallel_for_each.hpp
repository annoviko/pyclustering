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


#include <cstddef>
#include <functional>
#include <future>
#include <vector>


#include "start_for.hpp"


/* Available options: PARALLEL_IMPLEMENTATION_ASYNC, 
                      PARALLEL_IMPLEMENTATION_NONE,  */

#define PARALLEL_IMPLEMENTATION_ASYNC_POOL
//#define PARALLEL_IMPLEMENTATION_NONE


namespace ccore {

namespace parallel {


template <typename TypeIter, typename TypeAction>
void parallel_for_each(const TypeIter p_begin, const TypeIter p_end, const TypeAction & p_task) {
#if defined(PARALLEL_IMPLEMENTATION_ASYNC_POOL)
    const std::size_t step = std::distance(p_begin, p_end) / (start_for::get_size() + 1);

    auto current_start = p_begin;
    auto current_end = p_begin + step;

    std::vector<std::size_t> captured_threads;

    for (std::size_t i = 0; i < start_for::get_size(); ++i) {
        auto async_task = [&p_task, current_start, current_end](){
            for (auto iter = current_start; iter != current_end; ++iter) {
                p_task(*iter);
            }
        };

        const std::size_t free_index = start_for::try_execute(async_task);
        if (free_index == start_for::UNAVAILABLE_THREAD) {
            async_task();
        }
        else {
            captured_threads.push_back(free_index);
        }

        current_start = current_end;
        current_end += step;
    }

    for (auto iter = current_start; iter != p_end; ++iter) {
        p_task(*iter);
    }

    for (auto index_thread : captured_threads) {
        start_for::wait(index_thread);
    }
#else
    /* This part of code is switched only to estimate parallel implementation with non-parallel.
       Never switch on for real product. */
    for (auto iter = p_begin; iter != p_end; ++iter) {
        p_task(*iter);
    }
#endif
}


template <typename TypeContainer, typename TypeAction>
void parallel_for_each(const TypeContainer & p_container, const TypeAction & p_task) {
    parallel_for_each(std::begin(p_container), std::end(p_container), p_task);
}


}

}