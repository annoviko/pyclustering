#ifndef CCORE_DIFFERENTIAL_RUNGE_KUTTA_4_HPP_
#define CCORE_DIFFERENTIAL_RUNGE_KUTTA_4_HPP_


#include "differential/differ_state.hpp"


namespace differential {

template <typename state_type, typename extra_type = void *>
void runge_kutta_4(void (*function_pointer)(const double t, const differ_state<state_type> & inputs, const differ_extra<extra_type> & argv, differ_state<state_type> & outputs),
                   const differ_state<state_type> &     inputs,
                   const double                         time_start,
                   const double                         time_end,
                   const unsigned int                   steps,
                   const bool                           flag_collect,
                   const differ_extra<extra_type> &     argv,
                   differ_result<state_type> &          outputs) {

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

    for (unsigned int i = 0; i < steps; i++) {
        differ_state<state_type> fp1, fp2, fp3, fp4;
        differ_state<state_type> k1, k2, k3, k4;

        function_pointer(current_result.time, current_result.state, argv, fp1);
        k1 = fp1 * step;

        function_pointer(current_result.time + step / 2.0, current_result.state + k1 / 2.0, argv, fp2);
        k2 = fp2 * step;

        function_pointer(current_result.time + step / 2.0, current_result.state + k2 / 2.0, argv, fp3);
        k3 = fp3 * step;

        function_pointer(current_result.time + step, current_result.state + k3, argv, fp4);
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


#endif
