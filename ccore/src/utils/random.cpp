/*!

@authors Andrei Novikov (pyclustering@yandex.ru)
@date 2014-2020
@copyright BSD-3-Clause

*/

#include <pyclustering/utils/random.hpp>

#include <chrono>
#include <random>


namespace pyclustering {

namespace utils {

namespace random {


double generate_uniform_random(const double p_from, const double p_to) {
    unsigned seed = (unsigned) std::chrono::system_clock::now().time_since_epoch().count();
    std::default_random_engine generator(seed);

    std::uniform_real_distribution<double> distribution(p_from, p_to);
    return distribution(generator);
}


}

}

}