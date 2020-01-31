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


#include <gtest/gtest.h>

#include <algorithm>

#include <pyclustering/utils/stats.hpp>


using namespace pyclustering::utils::stats;


TEST(utest_stats, pdf) {
    std::vector<double> data = {-0.80526491, -1.03631388, 1.38455957, 1.67106978, -0.00618697, -2.44026332, 1.12861732, -0.16200512, -1.41740669, -1.27725788};
    std::sort(std::begin(data), std::end(data));

    auto result = pdf(data);

    ASSERT_EQ(data.size(), result.size());

    std::vector<double> expected = { 0.0203153, 0.14610067, 0.17646506, 0.23318766, 0.28846996, 0.39374123, 0.39893464, 0.21101479, 0.15298106, 0.09874884 };
    for (std::size_t i = 0; i < result.size(); ++i) {
        ASSERT_NEAR(expected[i], result[i], 0.000001);
    }
}


TEST(utest_stats, cdf) {
    std::vector<double> data = {-0.80526491, -1.03631388, 1.38455957, 1.67106978, -0.00618697, -2.44026332, 1.12861732, -0.16200512, -1.41740669, -1.27725788};
    std::sort(std::begin(data), std::end(data));

    auto result = cdf(data);

    ASSERT_EQ(data.size(), result.size());

    std::vector<double> expected = { 0.00733828, 0.07818203, 0.10075561, 0.15002787, 0.21033341, 0.43565091, 0.49753177, 0.87047035, 0.91690641, 0.95264605 };
    for (std::size_t i = 0; i < result.size(); ++i) {
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
    const double result = pyclustering::utils::stats::std(data);
    ASSERT_NEAR(1.351987, result, 0.000001);
}


TEST(utest_stats, anderson) {
    std::vector<double> data = { 1.20051687, -0.11498334, -0.06660842, 0.65981179, -0.8188606, -1.48766638, -0.76268192, 0.89156879, 0.5011937, 0.85737694 };
    const double result = anderson(data);
    ASSERT_NEAR(0.319009, result, 0.000001);
}


TEST(utest_stats, critical_values) {
    std::vector<double> expected = { 0.50086957, 0.57043478, 0.68434783, 0.79826087, 0.94956522 };
    std::vector<double> actual = critical_values(10);

    ASSERT_EQ(expected.size(), actual.size());

    for (std::size_t i = 0; i < expected.size(); ++i) {
        ASSERT_NEAR(expected[i], actual[i], 0.000001);
    }
}