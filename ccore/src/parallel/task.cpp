/*!

@authors Andrei Novikov (pyclustering@yandex.ru)
@date 2014-2020
@copyright BSD-3-Clause

*/


#include <pyclustering/parallel/task.hpp>


namespace pyclustering {

namespace parallel {


task::task(const proc & p_task) :
    m_task(p_task)
{ 
    m_ready.lock();
}


void task::set_ready() {
    m_ready.unlock();
}


void task::wait_ready() const {
    m_ready.lock();
}


void task::operator()() {
    m_task();
}


}

}
