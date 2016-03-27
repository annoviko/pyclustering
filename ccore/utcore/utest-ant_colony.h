#pragma once

#include "gtest/gtest.h"

#include "ccore/ant_colony/AntColony.hpp"


TEST(utest_ant_colony, city_distance) {
	city_distance::CityCoord One{ 23.46, 97.512 };
	city_distance::CityCoord Two{ -5671.2, -12.459 };
	city_distance::CityCoord Three{ 871.612, -987.293 };

	ASSERT_DOUBLE_EQ(5695.721739730708, One.get_distance(Two));
	//ASSERT_NEAR(5695.721739730708, One.get_distance(Two), 0.0000001);
	ASSERT_DOUBLE_EQ(1377.01260093326, One.get_distance(Three));
	ASSERT_DOUBLE_EQ(6615.035162030509, Two.get_distance(Three));
}


TEST(utest_ant_colony, find_smallest_path) {

	/*
	* Cities placement for the case:
	*    1 - 2 - 3
	*	 |   |   |
	*    4 - 5 - 6
	*/
	
	city_distance::CityCoord One{ 0.0, 1.0 };
	city_distance::CityCoord Two{ 1.0, 1.0 };
	city_distance::CityCoord Three{ 2.0, 1.0 };
	city_distance::CityCoord Thour{ 0.0, 0.0 };
	city_distance::CityCoord Five{ 1.0, 0.0 };
	city_distance::CityCoord Six{ 2.0, 0.0 };

	auto dist = city_distance::CityDistanceMatrix::make_city_distance_matrix
		({ One, Two, Three, Thour, Five, Six });

	using AntAPI = ant_colony::AntColonyAlgorithmParamsInitializer;
	auto sp_algo_params_2 = ant_colony::AntColonyAlgorithmParams::make_param
		(AntAPI::Q_t{ 1.5 }
			, AntAPI::Ro_t{ 0.7 }
			, AntAPI::Alpha_t{ 1.0 }
			, AntAPI::Beta_t{ 1.0 }
			, AntAPI::Gamma_t{ 2.0 }
			, AntAPI::InitialPheramone_t{ 0.1 }
			, AntAPI::Iterations_t{ 50 }
			, AntAPI::CountAntsInIteration_t{ 10 }
	);

	ant_colony::AntColony ant_algo{ dist, sp_algo_params_2 };
	auto res = ant_algo.process();

	ASSERT_DOUBLE_EQ(6.0, res->pathLen);
}