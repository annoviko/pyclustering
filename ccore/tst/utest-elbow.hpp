/*!

@authors Andrei Novikov (pyclustering@yandex.ru)
@date 2014-2020
@copyright BSD-3-Clause

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
