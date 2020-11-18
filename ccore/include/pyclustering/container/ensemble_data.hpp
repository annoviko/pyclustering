/*!

@authors Andrei Novikov (pyclustering@yandex.ru)
@date 2014-2020
@copyright BSD-3-Clause

*/

#pragma once


#include <vector>


namespace pyclustering {

namespace container {


template <typename sync_ensemble_type>
using ensemble_data = std::vector<sync_ensemble_type>;


using basic_ensemble        = std::vector<std::size_t>;
using basic_ensemble_data   = std::vector<basic_ensemble>;


}

}
