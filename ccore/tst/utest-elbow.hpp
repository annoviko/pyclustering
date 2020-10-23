/*!

@authors Andrei Novikov (pyclustering@yandex.ru)
@date 2014-2020
@copyright GNU Public License

@cond GNU_PUBLIC_LICENSE
    pyclustering is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    pyclustering is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
@endcond

*/


#pragma once


#include <gtest/gtest.h>

#include <thread>

#include "utenv_check.hpp"

#include <pyclustering/cluster/elbow.hpp>


using namespace pyclustering::clst;


template <class type_initializer = kmeans_plus_plus>
void elbow_template(const dataset_ptr p_data,
                    const std::size_t p_amount_clusters,
                    const std::size_t p_kmin,
                    const std::size_t p_kmax,
                    const std::size_t p_step = 1)
{
    elbow<type_initializer> instance(p_kmin, p_kmax, p_step, 1000);

    elbow_data result;
    instance.process(*p_data, result);

    ASSERT_GT(result.get_amount(), p_kmin);
    ASSERT_LT(result.get_amount(), p_kmax);
    ASSERT_EQ(result.get_wce().size(), (p_kmax - p_kmin) / p_step + 1);
    ASSERT_GT(result.get_wce().front(), result.get_wce().back());

    if (p_amount_clusters != static_cast<std::size_t>(-1)) {
        ASSERT_EQ(result.get_amount(), p_amount_clusters);
    }
}
