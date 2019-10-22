/**
*
* @authors Andrei Novikov (pyclustering@yandex.ru)
* @date 2014-2019
* @copyright GNU Public License
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