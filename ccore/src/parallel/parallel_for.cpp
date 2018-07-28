#include "parallel_for.hpp"


#include <future>
#include <vector>


namespace ccore {

namespace parallel {


void parallel_for(const std::size_t p_start, const std::size_t p_end, const std::function<void(const std::size_t)> & p_task) {
    static const std::size_t amount_hardware_threads = std::thread::hardware_concurrency();
    static const std::size_t amount_threads = (amount_hardware_threads > 1) ? (amount_hardware_threads - 1) : 2;

    std::vector<std::future<void>> future_storage(amount_threads);

    const std::size_t step = (p_end - p_start) / (amount_threads + 1);
    std::size_t current_start = p_start;
    std::size_t current_end = p_start + step;

    for (std::size_t i = 0; i < amount_threads; ++i) {
        std::future<void> future_result = std::async(std::launch::async, [&p_task, current_start, current_end](){
            for (std::size_t i = current_start; i < current_end; ++i) {
                p_task(i);
            }
        });

        future_storage[i] = std::move(future_result);

        current_start = current_end;
        current_end += step;
    }

    for (std::size_t i = current_start; i < p_end; ++i) {
        p_task(i);
    }

    for (auto & result : future_storage) {
        result.get();
    }
}


}

}