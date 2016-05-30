/**
*
* Copyright (C) 2014-2016    Andrei Novikov (pyclustering@yandex.ru)
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

#include <gtest/gtest.h>

#include "utest-adjacency_bit_matrix.hpp"
#include "utest_adjacency_connector.hpp"
#include "utest-adjacency_list.hpp"
#include "utest-adjacency_matrix.hpp"
#include "utest-adjacency_weight_list.hpp"
#include "utest-agglomerative.hpp"
#include "utest-ant_colony.hpp"
#include "utest-ant_clustering.hpp"
#include "utest-cure.hpp"
#include "utest-dbscan.hpp"
#include "utest-differential.hpp"
#include "utest-hsyncnet.hpp"
#include "utest-kdtree.hpp"
#include "utest-kmeans.hpp"
#include "utest-kmedians.hpp"
#include "utest-kmedoids.hpp"
#include "utest-legion.hpp"
#include "utest-pcnn.hpp"
#include "utest-rock.hpp"
#include "utest-som.hpp"
#include "utest-sync.hpp"
#include "utest-syncnet.hpp"
#include "utest-syncpr.hpp"
#include "utest-xmeans.hpp"


int main(int argc, char *argv[]) {
	::testing::InitGoogleTest(&argc, argv);
	return RUN_ALL_TESTS();
}
