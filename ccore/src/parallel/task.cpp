#include "task.hpp"


const std::size_t    task::INVALID_TASK_ID              = (std::size_t) -1;

std::size_t          task::STATIC_TASK_ID_GENERATOR     = 0;


task::task(const proc & p_task) :
    m_id(generate_task_id()),
    m_task(p_task),
    m_status(task_status::PENDING)
{ }


void task::set_status(const task_status p_status) {
    m_status = p_status;
}


task_status task::get_status(void) const {
    return m_status;
}


std::size_t task::get_id(void) const {
    return m_id;
}


std::size_t task::generate_task_id(void) {
    if (++STATIC_TASK_ID_GENERATOR == task::INVALID_TASK_ID) {
        return STATIC_TASK_ID_GENERATOR;
    }

    return ++STATIC_TASK_ID_GENERATOR;
}


void task::operator()() {
    m_task();
}
