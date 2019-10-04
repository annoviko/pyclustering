/**
*
* @authors Andrei Novikov (pyclustering@yandex.ru)
* @date 2014-2019
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


#include "gtest/gtest.h"

#include <algorithm>

#include "utils/stats.hpp"


using namespace ccore::utils::stats;


TEST(utest_stats, pdf) {
    std::vector<double> data = {-0.80526491, -1.03631388, 1.38455957, 1.67106978, -0.00618697, -2.44026332, 1.12861732, -0.16200512, -1.41740669, -1.27725788};
    std::sort(std::begin(data), std::end(data));

    auto result = pdf(data);

    ASSERT_EQ(std::size(result), result.size());

    std::vector<double> expected = { 0.0203153, 0.14610067, 0.17646506, 0.23318766, 0.28846996, 0.39374123, 0.39893464, 0.21101479, 0.15298106, 0.09874884 };
    for (std::size_t i = 0; i < result.size(); i++) {
        ASSERT_NEAR(expected[i], result[i], 0.000001);
    }
}


TEST(utest_stats, mean) {
    std::vector<double> data = {-0.80526491, -1.03631388, 1.38455957, 1.67106978, -0.00618697, -2.44026332, 1.12861732, -0.16200512, -1.41740669, -1.27725788};
    const double result = mean(data);
    ASSERT_NEAR(-0.2960452, result, 0.0000001);
}


TEST(utest_stats, var) {
    std::vector<double> data = {-0.80526491, -1.03631388, 1.38455957, 1.67106978, -0.00618697, -2.44026332, 1.12861732, -0.16200512, -1.41740669, -1.27725788};
    const double result = var(data);
    ASSERT_NEAR(1.827869, result, 0.000001);
}


TEST(utest_stats, std) {
    std::vector<double> data = {-0.80526491, -1.03631388, 1.38455957, 1.67106978, -0.00618697, -2.44026332, 1.12861732, -0.16200512, -1.41740669, -1.27725788};
    const double result = ccore::utils::stats::std(data);
    ASSERT_NEAR(1.351987, result, 0.000001);
}