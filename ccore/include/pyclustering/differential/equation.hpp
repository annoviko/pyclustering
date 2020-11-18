/*!

@authors Andrei Novikov (pyclustering@yandex.ru)
@date 2014-2020
@copyright BSD-3-Clause

*/


#pragma once


#include <functional>

#include <pyclustering/differential/differ_state.hpp>
#include <pyclustering/differential/solve_type.hpp>


namespace pyclustering {

namespace differential {


template <class state_type, class extra_type = void *>
using equation = std::function<void (double, const differ_state<state_type> &, const differ_extra<extra_type> &, differ_state<state_type> &) >;


}

}