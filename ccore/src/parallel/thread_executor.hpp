#pragma once


#include <atomic>
#include <condition_variable>
#include <thread>

#include "task.hpp"



class thread_executor {
public:
    using observer  = std::function<void(task::ptr)>;

    using ptr = std::shared_ptr<thread_executor>;

private:
    task::ptr               m_task          = nullptr;
    std::atomic<bool>       m_idle          = true;
    std::atomic<bool>       m_stop          = false;

    observer                m_callback      = nullptr;

    std::condition_variable m_event_arrive;
    std::mutex              m_block;
    std::thread             m_executor      = std::thread(&thread_executor::run, this);

public:
    thread_executor(void) = default;

    thread_executor(const observer & p_callback);

    thread_executor(const thread_executor & p_other) = delete;

    thread_executor(thread_executor && p_other);

    ~thread_executor(void);

public:
    bool execute(const task::ptr p_task);

    bool is_idle(void) const;

private:
    void run(void);

    void stop(void);
};