/*!

@authors Andrei Novikov (pyclustering@yandex.ru)
@date 2014-2020
@copyright BSD-3-Clause

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