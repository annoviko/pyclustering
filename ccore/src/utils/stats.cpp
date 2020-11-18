/*!

@authors Andrei Novikov (pyclustering@yandex.ru)
@date 2014-2020
@copyright BSD-3-Clause

*/


#include <pyclustering/utils/stats.hpp>


namespace pyclustering {

namespace utils {

namespace stats {


std::vector<double> critical_values(const std::size_t p_data_size) {
    std::vector<double> result = { 0.576, 0.656, 0.787, 0.918, 1.092 };
    const double size = static_cast<const double>(p_data_size);
    for (auto & value : result) {
        value /= (1.0 + 4.0 / size - 25.0 / size / size);
    }

    return result;
}


}

}

}