/**
*
* Copyright (C) 2014-2018    Andrei Novikov (pyclustering@yandex.ru)
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


#include "gtest/gtest.h"

#include "cluster/ordering_analyser.hpp"

#include "samples.hpp"
#include "utenv_check.hpp"


using namespace ccore::clst;


TEST(utest_ordering, cluster_allocation_identical_ordering) {
    ordering cluster_ordering = {5.0, 5.0, 5.0, 5.0, 5.0, 5.0};

    EXPECT_EQ(1U, ordering_analyser::extract_cluster_amount(cluster_ordering, 6.5));
    EXPECT_EQ(0U, ordering_analyser::extract_cluster_amount(cluster_ordering, 4.5));
}


TEST(utest_ordering, impossible_calculate_radius_identical_ordering) {
    ordering cluster_ordering = {5.0, 5.0, 5.0, 5.0, 5.0, 5.0, 5.0, 5.0, 5.0, 5.0};

    EXPECT_TRUE(ordering_analyser::calculate_connvectivity_radius(cluster_ordering, 2) < 0);
}


TEST(utest_ordering, impossible_calculate_radius_geterogeneous_ordering) {
    ordering cluster_ordering = {5.0, 5.0, 5.0, 5.0, 6.0, 8.0, 6.0, 5.0, 5.0, 5.0};

    EXPECT_TRUE(ordering_analyser().calculate_connvectivity_radius(cluster_ordering, 3) < 0);
}
