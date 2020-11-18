/*!

@authors Andrei Novikov (pyclustering@yandex.ru)
@date 2014-2020
@copyright BSD-3-Clause

*/


#include <pyclustering/parallel/spinlock.hpp>

#include <thread>


namespace pyclustering {

namespace parallel {


bool spinlock::try_lock() {
    return !m_lock.test_and_set(std::memory_order_acquire);
}

void spinlock::lock() {
    for(std::size_t i = 0; !try_lock(); i++) {
        if (i % 100) {
            std::this_thread::yield();
        }
    }
}

void spinlock::unlock() {
    m_lock.clear(std::memory_order_release);
}


}

}