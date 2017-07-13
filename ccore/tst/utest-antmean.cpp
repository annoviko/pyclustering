/**
*
* Copyright (C) 2014-2017    Aleksey Kukushkin (pyclustering@yandex.ru)
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

#include "cluster/antmean.hpp"
#include "cluster/cluster_data.hpp"
#include "cluster/cluster_algorithm.hpp"

#include "utils.hpp"


void test_equal_clusters(cluster_analysis::cluster_data &res, std::vector<std::size_t> idx)
{
    bool found = false;

    for (const auto & clusters_to_test : (*(res.clusters())))
    {

        if(clusters_to_test.size() != idx.size()) continue;

        for (auto e_idx : idx)
        {
            auto pos = std::find(clusters_to_test.begin(), clusters_to_test.end(), e_idx);
            if (pos == clusters_to_test.end()) continue;
        }
        found = true;
    }

    ASSERT_TRUE(found);
};



TEST(utest_ant_clustering, simple_4_point_clustering)
{
    using AntCAPI = ant::ant_colony_clustering_params_initializer;

    auto params_ant_clustering = ant::ant_clustering_params::make_param(
        AntCAPI::RO_t(0.9)
        , AntCAPI::Pheramone_init_t(0.1)
        , AntCAPI::Iterations_t(50)
        , AntCAPI::Count_ants_t(20)
        );

    double points[][2] = {
        { 0,0 },{ 1,1 },{ 10,10 },{ 11,11 },{ -2, -2 },{ 0.55, -1.26 },{ 13.25, 12.12 }
    };
    std::size_t count_clusters = 2;

    std::size_t count_points = sizeof(points) / sizeof(points[0]);
    std::size_t dimention = sizeof(points[0]) / sizeof(points[0][0]);

    dataset input_points(count_points);

    for (std::size_t i = 0; i < input_points.size(); ++i)
    {
        for (std::size_t j = 0; j < dimention; ++j)
            input_points[i].push_back(points[i][j]);
    }

    cluster_analysis::cluster_data result;

    ant::ant_clustering_mean ant_mean_clustering{ params_ant_clustering, count_clusters };
    ant_mean_clustering.process(input_points, result);

    test_equal_clusters(result, {0, 1, 4, 5});
    test_equal_clusters(result, {2, 3, 6});
}

