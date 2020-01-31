/**
*
* @authors Andrei Novikov (pyclustering@yandex.ru)
* @date 2014-2020
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


#include <gtest/gtest.h>

#include <thread>

#include "utenv_check.hpp"

#include <pyclustering/cluster/elbow.hpp>


using namespace pyclustering::clst;


template <class type_initializer = kmeans_plus_plus>
void elbow_template(const dataset_ptr p_data,
                    const std::size_t p_amount_clusters,
                    const std::size_t p_kmin,
                    const std::size_t p_kmax)
{
  const static std::size_t repeat = 10;
  
  bool testing_result = false;
  elbow<type_initializer> instance(p_kmin, p_kmax);

  for (std::size_t i = 0; i < repeat; i++) {
    elbow_data result;
    instance.process(*p_data, result);

    ASSERT_GT(result.get_amount(), p_kmin);
    ASSERT_LT(result.get_amount(), p_kmax);
    ASSERT_EQ(result.get_wce().size(), p_kmax - p_kmin);
    ASSERT_GT(result.get_wce().front(), result.get_wce().back());

    std::size_t upper_limit = p_amount_clusters + 1;
    std::size_t lower_limit = p_amount_clusters > 1 ? p_amount_clusters - 1 : 1;
    
    if ((result.get_amount() > upper_limit) || (result.get_amount() < lower_limit)) {
      std::this_thread::sleep_for(std::chrono::duration<int, std::milli>(25));
      continue;
    }

    testing_result = true;
    break;
  }

  ASSERT_TRUE(testing_result);
}
