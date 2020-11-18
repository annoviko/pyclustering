/*!

@authors Andrei Novikov (pyclustering@yandex.ru)
@date 2014-2020
@copyright BSD-3-Clause

*/

#pragma once


#include <pyclustering/differential/differ_state.hpp>
#include <pyclustering/differential/equation.hpp>
#include <pyclustering/differential/solve_type.hpp>

#include <functional>


namespace pyclustering {

namespace differential {


template <class state_type, class extra_type = void *>
void runge_kutta_4(const equation<state_type, extra_type> & func,
                   const differ_state<state_type> &         inputs,
                   const double                             time_start,
                   const double                             time_end,
                   const std::size_t                        steps,
                   const bool                               flag_collect,
                   const differ_extra<extra_type> &         argv,           /* additional arguments that are used in the equation */
                   differ_result<state_type> &              outputs) {

    const double step = (time_end - time_start) / (double) steps;

    if (flag_collect) {
        outputs.resize(steps);
    }
    else {
        outputs.resize(1);
    }

    differ_output<state_type> current_result;
    current_result.time = time_start;
    current_result.state = inputs;

    for (std::size_t i = 0; i < steps; i++) {
        differ_state<state_type> fp1, fp2, fp3, fp4;
        differ_state<state_type> k1, k2, k3, k4;

        func(current_result.time, current_result.state, argv, fp1);
        k1 = fp1 * step;

        func(current_result.time + step / 2.0, current_result.state + k1 / 2.0, argv, fp2);
        k2 = fp2 * step;

        func(current_result.time + step / 2.0, current_result.state + k2 / 2.0, argv, fp3);
        k3 = fp3 * step;

        func(current_result.time + step, current_result.state + k3, argv, fp4);
        k4 = fp4 * step;

        current_result.state += (k1 + 2.0 * k2 + 2.0 * k3 + k4) / 6.0;
        current_result.time += step;

        if (flag_collect) {
            outputs[i].time = current_result.time;
            outputs[i].state = current_result.state;
        }
    }

    if (!flag_collect) {
        outputs[0].time = current_result.time;
        outputs[0].state = current_result.state;
    }
}


}

}