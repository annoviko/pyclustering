/*!

@authors Andrei Novikov (pyclustering@yandex.ru)
@date 2014-2020
@copyright GNU Public License

@cond GNU_PUBLIC_LICENSE
    pyclustering is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    pyclustering is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
@endcond

*/


#pragma once


#include <atomic>


namespace pyclustering {

namespace parallel {

/*!

@class      spinlock spinlock.hpp pyclustering/parallel/spinlock.hpp

@brief      Spinlock mechanism for synchronization.
@details    Spinlock is a lock which causes a thread trying to acquire it to simply wait in a loop while repeatedly 
             checking if the lock is available.

*/
class spinlock {
private:
    std::atomic_flag    m_lock = ATOMIC_FLAG_INIT;

public:
    /*!

    @brief Default spinlock constructor.

    */
    spinlock() = default;

    /*!

    @brief Default spinlock destructor.

    */
    ~spinlock() = default;

public:
    /*!

    @brief Tries to lock once and if it is impossible then the spinlock returns control.

    @return Returns `true` if the resource was successfully locked.

    */
    bool try_lock();

    /*!

    @brief Tries to lock until success.

    */
    void lock();

    /*!

    @brief Unlocks the resource.

    */
    void unlock();
};


}

}