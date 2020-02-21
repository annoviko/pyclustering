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


#include <gtest/gtest.h>

#include <pyclustering/definitions.hpp>

#include <pyclustering/utils/metric.hpp>

#include "utenv_check.hpp"


using namespace pyclustering;
using namespace pyclustering::utils::metric;


TEST(utest_metric, metric_factory_euclidean) {
   distance_metric<point> metric = distance_metric_factory<point>::euclidean();
   ASSERT_EQ(1.0, metric({0.0, 0.0}, {1.0, 0.0}));
   ASSERT_EQ(3.0, metric({-1.0, -2.0}, {-1.0, -5.0}));
}

TEST(utest_metric, metric_factory_euclidean_square) {
   distance_metric<point> metric = distance_metric_factory<point>::euclidean_square();
   ASSERT_EQ(1.0, metric({0.0, 0.0}, {1.0, 0.0}));
   ASSERT_EQ(9.0, metric({-1.0, -2.0}, {-1.0, -5.0}));
}

TEST(utest_metric, metric_factory_manhattan) {
   distance_metric<point> metric = distance_metric_factory<point>::manhattan();
   ASSERT_EQ(1.0, metric({0.0, 0.0}, {1.0, 0.0}));
   ASSERT_EQ(3.0, metric({0.0, 0.0}, {1.0, 2.0}));
}

TEST(utest_metric, metric_factory_chebyshev) {
   distance_metric<point> metric = distance_metric_factory<point>::chebyshev();
   ASSERT_EQ(1.0, metric({0.0, 0.0}, {1.0, 0.0}));
   ASSERT_EQ(2.0, metric({0.0, 0.0}, {1.0, 2.0}));
}

TEST(utest_metric, metric_factory_minkowski) {
   distance_metric<point> metric = distance_metric_factory<point>::minkowski(2);
   ASSERT_EQ(1.0, metric({0.0, 0.0}, {1.0, 0.0}));
   ASSERT_EQ(3.0, metric({-1.0, -2.0}, {-1.0, -5.0}));
}

TEST(utest_metric, metric_factory_canberra) {
   distance_metric<point> metric = distance_metric_factory<point>::canberra();
   ASSERT_EQ(0.0, metric({0.0, 0.0}, {0.0, 0.0}));
   ASSERT_EQ(2.0, metric({0.0, 0.0}, {1.0, 1.0}));
   ASSERT_EQ(1.0, metric({0.75, 0.75}, {0.25, 0.25}));
}

TEST(utest_metric, metric_factory_cchi_square) {
   distance_metric<point> metric = distance_metric_factory<point>::chi_square();
   ASSERT_EQ(0.0, metric({0.0, 0.0}, {0.0, 0.0}));
   ASSERT_EQ(2.0, metric({0.0, 0.0}, {1.0, 1.0}));
   ASSERT_EQ(0.5, metric({0.75, 0.75}, {0.25, 0.25}));
}

TEST(utest_metric, metric_factory_gower) {
   distance_metric<point> metric = distance_metric_factory<point>::gower({0.0, 0.0});
   ASSERT_EQ(0.0, metric({0.0, 0.0}, {0.0, 0.0}));
   metric = distance_metric_factory<point>::gower({1.0, 1.0});
   ASSERT_EQ(1.0, metric({1.0, 1.0}, {2.0, 2.0}));
   metric = distance_metric_factory<point>::gower({0.5, 0.5});
   ASSERT_EQ(1.0, metric({0.75, 0.75}, {0.25, 0.25}));
}

TEST(utest_metric, metric_factory_user_defined) {
   distance_metric<point> metric = distance_metric_factory<point>::user_defined([](const point & p1, const point & p2) { return -5.0; } );
   ASSERT_EQ(-5.0, metric({0.0, 0.0}, {1.0, 0.0}));
   ASSERT_EQ(-5.0, metric({0.0, 0.0}, {0.0, 0.0}));
}


TEST(utest_metric, calculate_distance_matrix_01) {
    dataset points = { {0}, {2}, {4} };
    dataset distance_matrix;

    pyclustering::utils::metric::distance_matrix(points, distance_matrix);

    dataset distance_matrix_expected = { { 0.0, 2.0, 4.0 }, { 2.0, 0.0, 2.0 }, { 4.0, 2.0, 0.0 } };

    ASSERT_EQ(distance_matrix, distance_matrix_expected);
}