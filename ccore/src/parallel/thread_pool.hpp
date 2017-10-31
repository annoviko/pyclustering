#pragma once


#include <vector>
#include <deque>

#include "thread_executor.hpp"



class thread_pool {
private:
    using thread_container = std::vector<thread_executor::ptr>;

private:
    thread_container                m_pool  = { };

    std::deque<task::ptr>           m_queue = { };
    std::deque<task::ptr>           m_done  = { };

    std::mutex                      m_mutex;
    std::condition_variable         m_event;

    std::size_t                     m_free  = 0;

public:
    thread_pool(void) = default;

    thread_pool(const std::size_t p_size);

    thread_pool(const thread_pool & p_pool) = delete;

    thread_pool(thread_pool && p_pool) = delete;

    ~thread_pool(void) = default;

public:
    std::size_t add_task(task::proc & p_raw_task);

    std::size_t pop_complete_task(void);

private:
    void task_done(const task::ptr p_task);
};