/**
*
* Copyright (C) 2014-2016    Aleksey Kukushkin (pyclustering@yandex.ru)
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

#include "gtest/gtest.h"

#include "tsp/ant_colony.hpp"
#include "tsp/distance_matrix.hpp"

#include "utils.hpp"


using namespace container;


const double EPS = 0.0000001; 

TEST(utest_ant_colony, city_distance_calculation) {
    city_distance::object_coordinate One{ 23.46, 97.512 };
    city_distance::object_coordinate Two{ -5671.2, -12.459 };
    city_distance::object_coordinate Three{ 871.612, -987.293 };

    //ASSERT_DOUBLE_EQ(5695.721739730708, One.get_distance(Two));
    ASSERT_NEAR(5695.721739730708, One.get_distance(Two), EPS);
    ASSERT_NEAR(1377.01260093326, One.get_distance(Three), EPS);
    ASSERT_NEAR(6615.035162030509, Two.get_distance(Three), EPS);
}

void template_smallest_distance_test(const std::shared_ptr<city_distance::distance_matrix> & coordinates, const double expected_result) {
    using AntAPI = ant::ant_colony_TSP_params_initializer;
    auto sp_algo_params_2 = ant::ant_colony_TSP_params::make_param
        (AntAPI::Q_t{ 1.5 },
                 AntAPI::Ro_t{ 0.7 }, 
                 AntAPI::Alpha_t{ 1.0 }, 
                 AntAPI::Beta_t{ 1.0 }, 
                 AntAPI::Gamma_t{ 2.0 }, 
                 AntAPI::InitialPheramone_t{ 0.1 }, 
                 AntAPI::Iterations_t{ 50 }, 
                 AntAPI::CountAntsInIteration_t{ 10 }
    );

    ant::ant_colony ant_algo{ coordinates, sp_algo_params_2 };
    auto res = ant_algo.process();

    ASSERT_DOUBLE_EQ(expected_result, res->path_length);
}


TEST(utest_ant_colony, one_city_only) {	
    city_distance::object_coordinate One{ 0.0, 0.0 };

    auto dist = city_distance::distance_matrix::make_city_distance_matrix({ One });

    template_smallest_distance_test(dist, 0.0);
}


TEST(utest_ant_colony, two_cities_negative_coordinate) {	
    city_distance::object_coordinate One{ -5.0,  0.0 };
    city_distance::object_coordinate Two{ -5.0, -4.0 };

    auto dist = city_distance::distance_matrix::make_city_distance_matrix({ One, Two });

    template_smallest_distance_test(dist, 8.0);
}


TEST(utest_ant_colony, three_cities_negative_positive_coordinate) {	
    city_distance::object_coordinate One{ -1.0, 1.0 };
    city_distance::object_coordinate Two{ -5.0, 1.0 };
    city_distance::object_coordinate Three{  3.0, 1.0 };

    auto dist = city_distance::distance_matrix::make_city_distance_matrix({ One, Two, Three });

    template_smallest_distance_test(dist, 16.0);
}


TEST(utest_ant_colony, cities_same_coordinates) {	
    city_distance::object_coordinate One{ 1.5, 2.5 };
    city_distance::object_coordinate Two{ 1.5, 2.5 };
    city_distance::object_coordinate Three{ 1.5, 2.5 };
    city_distance::object_coordinate Four{ 1.5, 2.5 };

    auto dist = city_distance::distance_matrix::make_city_distance_matrix({ One, Two, Three, Four });

    template_smallest_distance_test(dist, 0.0);
}


TEST(utest_ant_colony, smallest_path_two_cities) {
    /* Cities placement for the case: 1 - 2 */

    city_distance::object_coordinate One{ 0.0, 0.0 };
    city_distance::object_coordinate Two{ 15.0, 0.0 };

    auto dist = city_distance::distance_matrix::make_city_distance_matrix({ One, Two });

    template_smallest_distance_test(dist, 30.0);
}

TEST(utest_ant_colony, smallest_path_four_cities_by_graph) {
    /* Cities placement for the case
     *  symmetric matrix for 4 cities:
     *  (a,b) = 1
     *  (a,c) = 30
     *  (a,d) = 99
     *  (b,c) = 1
     *  (b,d) = 30
     *  (c,d) = 1
     * */
    enum class city_name_t
    {
        A, B, C, D
    };

    const std::size_t citiesCount = 4;

    // bad style for initialization !!!
    city_distance::distance_matrix::array_coordinate dist_matrix(citiesCount, std::vector<double>(citiesCount, 0));

#ifdef __CPP_14_ENABLED__
    auto write_symmetric = [&dist_matrix] (auto city1, auto city2, auto dist)
#else
    auto write_symmetric = [&dist_matrix] (city_name_t city1, city_name_t city2, double dist)
#endif
            {
                dist_matrix[static_cast<unsigned int>(city1)][static_cast<unsigned int>(city2)]
                      = dist_matrix[static_cast<unsigned int>(city2)][static_cast<unsigned int>(city1)]
                      = dist;
            };

    write_symmetric(city_name_t::A, city_name_t::B, 1.0);
    write_symmetric(city_name_t::A, city_name_t::C, 30.0);
    write_symmetric(city_name_t::A, city_name_t::D, 99.0);
    write_symmetric(city_name_t::B, city_name_t::C, 1.0);
    write_symmetric(city_name_t::B, city_name_t::D, 30.0);
    write_symmetric(city_name_t::C, city_name_t::D, 1.0);

    auto dist = city_distance::distance_matrix::make_city_distance_matrix(std::move(dist_matrix));

    template_smallest_distance_test(dist, 62.0);
}


TEST(utest_ant_colony, smallest_path_six_cities) {

    /*
    * Cities placement for the case:
    *    1 - 2 - 3
    *	 |   |   |
    *    4 - 5 - 6
    */

    city_distance::object_coordinate One{ 0.0, 1.0 };
    city_distance::object_coordinate Two{ 1.0, 1.0 };
    city_distance::object_coordinate Three{ 2.0, 1.0 };
    city_distance::object_coordinate Thour{ 0.0, 0.0 };
    city_distance::object_coordinate Five{ 1.0, 0.0 };
    city_distance::object_coordinate Six{ 2.0, 0.0 };

    auto dist = city_distance::distance_matrix::make_city_distance_matrix
        ({ One, Two, Three, Thour, Five, Six });

    template_smallest_distance_test(dist, 6.0);
}


TEST(utest_ant_colony, no_ants_for_processing) {
    city_distance::object_coordinate One{ -5.0,  0.0 };
    city_distance::object_coordinate Two{ -5.0, -4.0 };

    auto dist = city_distance::distance_matrix::make_city_distance_matrix({ One, Two });

    using AntAPI = ant::ant_colony_TSP_params_initializer;
    auto sp_algo_params_2 = ant::ant_colony_TSP_params::make_param
            (AntAPI::Q_t{ 1.5 },
                 AntAPI::Ro_t{ 0.7 },
                 AntAPI::Alpha_t{ 1.0 },
                 AntAPI::Beta_t{ 1.0 },
                 AntAPI::Gamma_t{ 2.0 },
                 AntAPI::InitialPheramone_t{ 0.1 },
                 AntAPI::Iterations_t{ 50 },
                 AntAPI::CountAntsInIteration_t{ 0 }
    );

    ant::ant_colony ant_algo{ dist, sp_algo_params_2 };
    auto res = ant_algo.process();

    ASSERT_DOUBLE_EQ(0.0, res->path_length);
}


TEST(utest_ant_colony, no_iterations_for_processing) {
    city_distance::object_coordinate One{ -5.0,  0.0 };
    city_distance::object_coordinate Two{ -5.0, -4.0 };

    auto dist = city_distance::distance_matrix::make_city_distance_matrix({ One, Two });

    using AntAPI = ant::ant_colony_TSP_params_initializer;
    auto sp_algo_params_2 = ant::ant_colony_TSP_params::make_param
            (AntAPI::Q_t{ 1.5 },
                 AntAPI::Ro_t{ 0.7 },
                 AntAPI::Alpha_t{ 1.0 },
                 AntAPI::Beta_t{ 1.0 },
                 AntAPI::Gamma_t{ 2.0 },
                 AntAPI::InitialPheramone_t{ 0.1 },
                 AntAPI::Iterations_t{ 0 },
                 AntAPI::CountAntsInIteration_t{ 10 }
    );

    ant::ant_colony ant_algo{ dist, sp_algo_params_2 };
    auto res = ant_algo.process();

    ASSERT_DOUBLE_EQ(0.0, res->path_length);
}
