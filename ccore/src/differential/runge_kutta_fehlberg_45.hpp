/**
*
* Copyright (C) 2014-2016    Andrei Novikov (pyclustering@yandex.ru)
*
* GNU_PUBLIC_LICENSE
*   pyclustering is free software: you can redistribute it and/or modify
*   it under the terms of the GNU General Public License as published by
*   the Free Software Foundation, either version 3 of the License, or
*   (at your option) any later version.
*
*   pyclustering is distributed in the hope that it will be useful,
*   but WITHOUT ANY WARRANTY; without even the implied warranty of
*   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
*   GNU General Public License for more details.
*
*   You should have received a copy of the GNU General Public License
*   along with this program.  If not, see <http://www.gnu.org/licenses/>.
*
*/

#ifndef CCORE_DIFFERENTIAL_RUNGE_KUTTA_FEHLBERG_45_HPP_
#define CCORE_DIFFERENTIAL_RUNGE_KUTTA_FEHLBERG_45_HPP_


#include <cmath>

#include "differential/differ_factor.hpp"
#include "differential/differ_state.hpp"


namespace differential {

template <typename state_type, typename extra_type = void *>
void runge_kutta_fehlberg_45(void (*function_pointer)(const double t, const differ_state<state_type> & inputs, const differ_extra<extra_type> & argv, differ_state<state_type> & outputs),
                   const differ_state<state_type> &     inputs,
                   const double                         time_start,
                   const double                         time_end,
                   const double                         tolerance,
                   const bool                           flag_collect,
                   const differ_extra<extra_type> &     argv,
                   differ_result<state_type> &          outputs) {

    if (flag_collect) {
        outputs.clear();
    }
    else {
        outputs.resize(1);
    }

    differ_output<state_type> current_result;
    current_result.time = time_start;
    current_result.state = inputs;

    double h = (time_end - time_start) / 10.0;      /* default number of steps */
    const double hmin = h / 1000.0; /* default multiplier for maximum step size */
    const double hmax = 1000.0 * h; /* default multiplier for minimum step size */

    const double br = time_end - 0.00001 * (double) std::abs(time_end);
    const unsigned int iteration_limit = 300;

    unsigned int iteration_counter = 0;

    while (current_result.time < time_end) {
        const double current_time = current_result.time;
        const differ_state<state_type> current_value = current_result.state;

        if ( (current_time + h) > br ) {
            h = time_end - current_result.time;
        }

        differ_state<state_type> fp1, fp2, fp3, fp4, fp5, fp6;
        differ_state<state_type> k1, k2, k3, k4, k5, k6;
        differ_state<state_type> y2, y3, y4, y5, y6;

        function_pointer(current_time, current_value, argv, fp1);
        k1 = h * fp1;
        y2 = current_value + factor::B2 * k1;

        function_pointer(current_time + factor::A2 * h, y2, argv, fp2);
        k2 = h * fp2;
        y3 = current_value + factor::B3 * k1 + factor::C3 * k2;

        function_pointer(current_time + factor::A3 * h, y3, argv, fp3);
        k3 = h * fp3;
        y4 = current_value + factor::B4 * k1 + factor::C4 * k2 + factor::D4 * k3;

        function_pointer(current_time + factor::A4 * h, y4, argv, fp4);
        k4 = h * fp4;
        y5 = current_value + factor::B5 * k1 + factor::C5 * k2 + factor::D5 * k3 + factor::E5 * k4;

        function_pointer(current_time + factor::A5 * h, y5, argv, fp5);
        k5 = h * fp5;
        y6 = current_value + factor::B6 * k1 + factor::C6 * k2 + factor::D6 * k3 + factor::E6 * k4 + factor::F6 * k5;

        function_pointer(current_time + factor::A6 * h, y6, argv, fp6);
        k6 = h * fp6;

        /* Calculate error (difference between Runge-Kutta 4 and Runge-Kutta 5) and new value. */
        differ_state<state_type> errors = factor::R1 * k1 + factor::R3 * k3 + factor::R4 * k4 + factor::R5 * k5 + factor::R6 * k6;

        double err = 0.0;
        for (typename differ_state<state_type>::const_iterator iter = errors.cbegin(); iter != errors.cend(); iter++) {
            double current_error = std::abs(*iter);
            if (current_error > err) {
                err = current_error;
            }
        }

        /* Calculate new value. */
        differ_state<state_type> ynew = current_value + factor::N1 * k1 + factor::N3 * k3 + factor::N4 * k4 + factor::N5 * k5;

        if ( (err < tolerance) || (h < 2.0 * hmin) ) {
            current_result.state = ynew;

            if (current_time + h > br) {
                current_result.time = time_end;
            }
            else {
                current_result.time = current_time + h;
            }

            if (flag_collect) {
                outputs.push_back(current_result);
            }
            else {
                outputs[0] = current_result;
            }

            iteration_counter++;
        }

        double s = 0.0;
        if (err != 0.0) {
            s = 0.84 * std::pow( (tolerance * h / err), 0.25 );
        }

        if ( (s < 0.75) && (h > 2.0 * hmin) ) {
            h = h / 2.0;
        }

        if ( (s > 1.5) && (h * 2.0 < hmax) ) {
            h = 2.0 * h;
        }

        if (iteration_counter >= iteration_limit) {
            break;
        }
    }
}

}


#endif
