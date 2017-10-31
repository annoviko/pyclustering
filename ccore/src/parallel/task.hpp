#pragma once


#include <functional>
#include <list>
#include <memory>



enum class task_status {
    PENDING,
    PROCESSING,
    READY
};



class task {
public:
    const static std::size_t    INVALID_TASK_ID;

public:
    using proc      = std::function<void(void)>;
    using ptr       = std::shared_ptr<task>;

private:
    static std::size_t          STATIC_TASK_ID_GENERATOR;

private:
    std::size_t                 m_id        = generate_task_id();
    proc                        m_task      = proc();
    task_status                 m_status    = task_status::PENDING;

public:
    task(void) = default;

    task(const proc & p_task);

    task(const task & p_other) = default;

    task(task && p_other) = default;

    ~task(void) = default;

public:
    void set_status(const task_status p_status);

    task_status get_status(void) const;

    std::size_t get_id(void) const;

private:
    static std::size_t generate_task_id(void);

public:
    void operator()();
};