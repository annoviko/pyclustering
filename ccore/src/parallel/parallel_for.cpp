#include "parallel_for.hpp"


namespace ccore {

namespace parallel {


void parallel_for(std::size_t p_start, std::size_t p_end, const std::function<void(const std::size_t)> & p_task) {
    std::size_t thread_pool_size = 1;
    if (ccore::parallel::thread_pool::DEFAULT_POOL_SIZE > 1) {
        thread_pool_size = ccore::parallel::thread_pool::DEFAULT_POOL_SIZE - 1;

        ccore::parallel::thread_pool pool(thread_pool_size);

        std::size_t step = (p_end - p_start) / ccore::parallel::thread_pool::DEFAULT_POOL_SIZE;
        std::size_t current_start = p_start;
        std::size_t current_end = p_start + step;

        for (std::size_t i = 0; i < pool.size(); i++) {
            ccore::parallel::task::proc group_task = [&p_task, current_start, current_end](){
                for (std::size_t i = current_start; i < current_end; i++) {
                    p_task(i);
                }
            };

            current_start = current_end;
            current_end += step;

            pool.add_task(group_task);
        }

        for (std::size_t i = current_start; i < p_end; i++) {
            p_task(i);
        }

        for (std::size_t i = 0; i < pool.size(); i++) {
            pool.pop_complete_task();
        }
    }
    else
    {
        for (std::size_t i = p_start; i < p_end; i++) {
            p_task(i);
        }
    }
}


}

}