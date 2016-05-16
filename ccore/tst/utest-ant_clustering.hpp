#pragma once

#include "gtest/gtest.h"

#include "cluster/ant_clustering_mean.hpp"

#include "utils.hpp"


using namespace container;



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

    ant::clustering_data input{ sizeof(points) / sizeof(points[0]), 2 };
    for (std::size_t i = 0; i < sizeof(points) / sizeof(points[0]); ++i)
    {
        for (std::size_t j = 0; j < 2; ++j)
            input.data[i][j] = points[i][j];
    }

    ant::ant_clustering_mean ant_mean_clustering{ params_ant_clustering };
    auto res = ant_mean_clustering.process(input, 2);

    auto test_eq_clusters = [](ant_clustering_result& res, std::size_t num_data_1, std::size_t num_data_2, std::size_t count_clusters){
        for (std::size_t cluster = 0; cluster < count_clusters; ++cluster)
            ASSERT_EQ(res->clusters[num_data_1][cluster],res->clusters[num_data_2][cluster]);
    };

    test_eq_clusters(res, 0, 1, 2);
    test_eq_clusters(res, 2, 3, 2);
    test_eq_clusters(res, 0, 4, 2);
    test_eq_clusters(res, 0, 5, 2);
    test_eq_clusters(res, 2, 6, 2);
}

