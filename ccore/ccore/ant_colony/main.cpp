/*
 * test.cpp
 *
 *  Created on: Mar 21, 2016
 *      Author: alex
 */

#include <iostream>

#include "AntColony.hpp"

int main()
{
    city_distance::CityCoord<double> Piter {4.0, 3.0};
    city_distance::CityCoord<double> Moscow {14.0, 22.0};
    city_distance::CityCoord<double> Zero {0.0, 0.0};

    std::cout << Piter.get_dimention() << std::endl;
    std::cout << Piter.get_distance(Zero) << std::endl;

	auto dist = city_distance::CityDistanceMatrix<double>::make_city_distance_matrix
			({ Piter, Zero, Moscow });


    for (const auto& i : dist->get_matrix())
    {
        for (const auto j : i)
        {
            std::cout << j << "\t\t\t";
        }
        std::cout << std::endl;
    }


	using AntAPI = ant_colony::AntColonyAlgorithmParamsInitializer;
	auto sp_algo_params = ant_colony::AntColonyAlgorithmParams::make_param();

	auto sp_algo_params_2 = ant_colony::AntColonyAlgorithmParams::make_param
		(	AntAPI::Q_t{ 1.5 }
			, AntAPI::Ro_t{ 0.7 }
			, AntAPI::Alpha_t{ 1.0 }
			, AntAPI::Beta_t{ 1.0 }
			, AntAPI::Gamma_t{ 2.0 }
			, AntAPI::Iterations_t{ 100 }
		);

	std::cout << "Param_1 -> Q :" << sp_algo_params->get<AntAPI::paramsName::Q>().get() << std::endl;
	std::cout << "Param_2 -> Q :" << sp_algo_params_2->get<AntAPI::paramsName::Q>().get() << std::endl;

	std::cout << "Set Param 1 -> Q to 5.5" << std::endl;
	sp_algo_params->set<AntAPI::paramsName::Q>(5.5);

	std::cout << "Param_1 -> Q :" << sp_algo_params->get<AntAPI::paramsName::Q>().get() << std::endl;

	std::cout << std::endl << std::endl;

	std::cout << typeid(sp_algo_params).name() << std::endl;



	ant_colony::AntColony<double> ant_algo{ dist, sp_algo_params_2 };





	std::getchar();

    return 0;
}
