/*!

@authors Andrei Novikov (pyclustering@yandex.ru)
@date 2014-2020
@copyright BSD-3-Clause

*/


#pragma once


#include <functional>


namespace pyclustering {

namespace differential {


enum class solve_type {
    FORWARD_EULER,
    RUNGE_KUTTA_4,
    RUNGE_KUTTA_FEHLBERG_45,
};


}

}