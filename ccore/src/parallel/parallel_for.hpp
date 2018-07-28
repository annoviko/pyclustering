#pragma once


#include <cstddef>
#include <functional>


namespace ccore {

namespace parallel {


void parallel_for(std::size_t p_start, std::size_t p_end, const std::function<void(const std::size_t)> & p_task);


}

}