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


#include "start_for.hpp"


namespace ccore {

namespace parallel {


const std::size_t start_for::AMOUNT_HARDWARE_THREADS = std::thread::hardware_concurrency();
const std::size_t start_for::AMOUNT_THREADS = (AMOUNT_HARDWARE_THREADS > 1) ? (AMOUNT_HARDWARE_THREADS - 1) : 0;

std::vector<std::future<void>> start_for::FUTURE_STORAGE(AMOUNT_THREADS);
std::vector<spinlock> start_for::FUTURE_LOCKS(AMOUNT_THREADS);

const std::size_t start_for::UNAVAILABLE_THREAD = std::numeric_limits<std::size_t>::max();


std::size_t start_for::get_size(void) {
    return AMOUNT_THREADS;
}


void start_for::wait(const std::size_t p_index) {
    FUTURE_STORAGE[p_index].get();
    FUTURE_LOCKS[p_index].unlock();
}


}

}