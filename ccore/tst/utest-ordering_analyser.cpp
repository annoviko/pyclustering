/**
*
* Copyright (C) 2014-2017    Andrei Novikov (pyclustering@yandex.ru)
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
#include "utest-cluster.hpp"


TEST(utest_ordering, cluster_allocation_identical_ordering) {
    ordering_ptr cluster_ordering = std::shared_ptr<ordering>(new ordering({5.0, 5.0, 5.0, 5.0, 5.0, 5.0}));
    ordering_analyser analyser(cluster_ordering);

    EXPECT_EQ(1, analyser.extract_cluster_amount(6.5));
    EXPECT_EQ(0, analyser.extract_cluster_amount(4.5));
}


TEST(utest_ordering, impossible_calculate_radius_identical_ordering) {
    ordering_ptr cluster_ordering = std::shared_ptr<ordering>(new ordering({5.0, 5.0, 5.0, 5.0, 5.0, 5.0, 5.0, 5.0, 5.0, 5.0}));
    ordering_analyser analyser(cluster_ordering);

    EXPECT_TRUE(analyser.calculate_connvectivity_radius(2) < 0);
}


TEST(utest_ordering, impossible_calculate_radius_geterogeneous_ordering) {
    ordering_ptr cluster_ordering = std::shared_ptr<ordering>(new ordering({5.0, 5.0, 5.0, 5.0, 6.0, 8.0, 6.0, 5.0, 5.0, 5.0}));
    ordering_analyser analyser(cluster_ordering);

    EXPECT_TRUE(analyser.calculate_connvectivity_radius(3) < 0);
}
