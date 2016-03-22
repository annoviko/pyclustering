/*
 * ant_colony.cpp
 *
 *  Created on: Mar 21, 2016
 *      Author: alex
 */


#include "AntColony.hpp"


namespace ant_colony
{

	template<typename T>
	decltype(auto) AntColony<T>::process()
	{
		const unsigned city_count = get_count_city();
		
		////initiate pheramones to value from params
		//std::vector<std::vector<double>> 
		//	pheramone (std::vecotr<double>(city_count, get_initial_pheromone), city_count);

		//for (unsigned iteration = 0; iteration < get_count_iterations(); ++iteration)
		//{
		//	//randomly place ants in cities
		//	place_ants();

		//	for (unsigned step = 0; step < city_count; ++step)
		//	{
		//		for (auto & ant : v_ants)
		//		{

		//		}
		//	}
		//}


		
		return	result;
	}

}//namespace ant_colony

