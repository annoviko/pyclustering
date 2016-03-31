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

#include "city_distance_matrix.hpp"
#include "ant_colony_params.hpp"

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

	auto get_result() -> std::shared_ptr<AntColonyResult> { return result; }

private:

	using AntAPI = ant_colony::AntColonyAlgorithmParamsInitializer::paramsName;
	using cities_t = std::vector<int>;

    typedef std::tuple_element<static_cast<int>(AntAPI::COUNT_ANTS_IN_ITERATION), ant_colony::AntColonyAlgorithmParamsInitializer::params_t>::type  param_t;

private:
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

		auto get_city_num() const -> int { return value.first; }

		auto get_probability() const -> double { return value.second; }

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
		Pheramone(unsigned int cityCount, double initialPheramone)
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
	
	std::vector<AntColony::CityProbability> calc_probability(const ant_t& ant, const Pheramone& pheramone);
	
	int realize_probability(const ant_t& ant, const std::vector<CityProbability>& prob);

	double calc_path_length(const cities_t& cities);

	std::vector<std::vector<double>> calc_delta_pheramone(const std::vector<ant_t>& ants);

	void update_pheramones(Pheramone& pheramone, const std::vector<ant_t>& ants);

	void update_shortes_path(cities_t& shortes_path, const std::vector<ant_t>& ants);

	inline auto get_count_city(void)				const -> int      { return distance->m_matrix.size(); }

	inline auto get_count_ants_in_iteration(void)	const -> unsigned { return params->get<AntAPI::COUNT_ANTS_IN_ITERATION>().get(); }

	inline auto get_random_number(unsigned max)	    const -> int      { return (std::rand() % max); }

	inline auto get_initial_pheromone(void)			const -> double   { return params->get<AntAPI::INITIAL_PHERAMONE>().get(); }

	inline auto get_count_iterations(void)			const -> unsigned { return params->get<AntAPI::ITERATIONS>().get(); }

	inline auto get_param_ro(void)				    const -> double   { return params->get<AntAPI::RO>().get(); }

	inline auto get_param_Q(void)				    const -> double   { return params->get<AntAPI::Q>().get(); }

public:

    std::shared_ptr<AntColonyResult> result;

	std::shared_ptr<city_distance::CityDistanceMatrix> distance;

	std::shared_ptr<AntColonyAlgorithmParams> params;

};


}//namespace ant_colony
