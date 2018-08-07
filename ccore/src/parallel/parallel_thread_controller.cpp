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


#include "parallel_thread_controller.hpp"


namespace ccore {

namespace parallel {


parallel_thread_controller::parallel_thread_controller(void) :
    thread_pool(thread_pool::DEFAULT_POOL_SIZE - 1)
{ }


parallel_thread_controller & parallel_thread_controller::get_instance(void) {
    static parallel_thread_controller controller;
    return controller;
}


}

}