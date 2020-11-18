/*!

@authors Andrei Novikov (pyclustering@yandex.ru)
@date 2014-2020
@copyright BSD-3-Clause

*/


#include <pyclustering/utils/math.hpp>



namespace pyclustering {

namespace utils {

namespace math {


double heaviside(const double value) {
    if (value >= 0.0) { return 1.0; }
    return 0.0;
}


}

}

}