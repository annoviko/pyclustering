/*
 * ant_colony.h
 *
 *  Created on: Mar 21, 2016
 *      Author: alex
 */

#pragma once

#include <memory>
#include <ctime>

#include <iostream>

#include "CityDistanceMatrix.hpp"
#include "AntColonyAlgorithmParams.hpp"

namespace ant_colony
{


class AntColonyResult
{
public:
	std::vector<int> shortestPath;
	double pathLen;
};


/***********************************************************************************************
* class Ant_colony
*                          - main class for Ant Colony Optimization
*
*
***********************************************************************************************/
class AntColony
{

public:
	AntColony(const std::shared_ptr<city_distance::CityDistanceMatrix>& initDistance
			, const std::shared_ptr<AntColonyAlgorithmParams>& initParams)
		: result(new AntColonyResult)
		, distance(initDistance)
		, params(initParams)
	{}

	std::shared_ptr<AntColonyResult> process();

	decltype(auto) get_result() { return result; }

private:

	using AntAPI = ant_colony::AntColonyAlgorithmParamsInitializer::paramsName;
	using cities_t = std::vector<int>;


	/*********************************************************
	* struct ant_t
	*			- contains visited cities and current state of an agent
	********************************************************/
	struct ant_t
	{
		cities_t visited;
		int curState;
	};


	/*********************************************************
	* class CityProbability
	*			- An ant take probabilities when it have more than one possible next state(cities).
	*			- The ant take an array with probabilities that can be realized by function 'realize_probability'  
	********************************************************/
	class CityProbability
	{
	public:
		CityProbability(int city_num, double prob)
			:value(city_num, prob)
		{}

		decltype(auto) get_city_num() const { return value.first; }
		decltype(auto) get_probability() const { return value.second; }

		void divide_by(double divider) { value.second /= divider; }

	private:
		std::pair<int, double> value;
	};


	/*********************************************************
	* class Pheramone
	*			- contains an array with pheramone value for all ways between cities
	********************************************************/
	class Pheramone
	{
	public:
		Pheramone(int cityCount, double initialPheramone)
			: value(cityCount, std::vector<double>(cityCount, initialPheramone))
		{}

		const std::vector<double>& operator[] (std::size_t idx) const { return value[idx]; }
		std::vector<double>& operator[] (std::size_t idx) { return value[idx]; }

	private:
		std::vector<std::vector<double>> value;
	};

	//
	// Private functions to calculate process result
	//
	void place_ants_randomly(std::vector<ant_t>& ants);
	
	std::vector<CityProbability> calc_probability(const ant_t& ant, const Pheramone& pheramone);
	
	int realize_probability(const ant_t& ant, const std::vector<CityProbability>& prob);

	double calc_path_length(const cities_t& cities);

	std::vector<std::vector<double>> calc_delta_pheramone(const std::vector<ant_t>& ants);

	void update_pheramones(Pheramone& pheramone, const std::vector<ant_t>& ants);

	void update_shortes_path(cities_t& shortes_path, const std::vector<ant_t>& ants);



	decltype(auto) get_count_city				()				const { return distance->matrix.size(); }
	decltype(auto) get_count_ants_in_iteration	()				const { return params->get<AntAPI::COUNT_ANTS_IN_ITERATION>().get(); }
	decltype(auto) get_random_number			(unsigned max)	const { return (std::rand() % max); }
	decltype(auto) get_initial_pheromone		()				const { return params->get<AntAPI::INITIAL_PHERAMONE>().get(); }
	decltype(auto) get_count_iterations			()				const { return params->get<AntAPI::ITERATIONS>().get(); }
	decltype(auto) get_param_ro					()				const { return params->get<AntAPI::RO>().get(); }
	decltype(auto) get_param_Q					()				const { return params->get<AntAPI::Q>().get(); }

	// decltype(auto) get_count_iterations();

public:

    std::shared_ptr<AntColonyResult> result;
	std::shared_ptr<city_distance::CityDistanceMatrix> distance;
	std::shared_ptr<AntColonyAlgorithmParams> params;

};


}//namespace ant_colony
