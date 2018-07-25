#include "parallel_for.hpp"


namespace ccore {

namespace parallel {


void parallel_for(std::size_t p_start, std::size_t p_end, const std::function<void(const std::size_t)> & p_task) {
  ccore::parallel::thread_pool pool;

  for (std::size_t i = p_start; i < p_end - 1; i++) {
    ccore::parallel::task::proc task = [&p_task, i](){ p_task(i); };
    pool.add_task(task);
  }

  p_task(p_end - 1);
  for (std::size_t i = 0; i < p_end; i++) {
    pool.pop_complete_task();
  }
}


}

}