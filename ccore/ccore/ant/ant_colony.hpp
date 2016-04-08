/*
 * ant_colony.h
 *
 *  Created on: Mar 21, 2016
 *      Author: alex
 */

#pragma once

#include <memory>
#include <ctime>

#include "distance_matrix.hpp"
#include "ant_colony_params.hpp"

namespace ant
{


typedef struct ant_colony_tsp_params {
    double                  q;
    double                  ro;
    double                  alpha;
    double                  beta;
    double                  gamma;
    double                  initial_pheramone;
    unsigned int            iterations;
    unsigned int            count_ants_in_iteration;
} ant_colony_tsp_params;


class ant_colony_result
{
public:
    ant_colony_result(void)
        : path_length{0}
    {}

	std::vector<int> shortest_path;
	double path_length;
};


/***********************************************************************************************
* class Ant_colony
*                          - main class for Ant Colony Optimization
*
*
***********************************************************************************************/
class ant_colony
{

public:
	ant_colony(const std::shared_ptr<city_distance::distance_matrix>& initDistance
			, const std::shared_ptr<ant_colony_params>& initParams)
		: result(new ant_colony_result)
		, distance(initDistance)
		, params(initParams)
	{}

	std::shared_ptr<ant_colony_result> process();

#ifdef __CPP_14_ENABLED__
	decltype(auto) get_result() { return result; }
#else
	std::shared_ptr<ant_colony_result> get_result() { return result; }
#endif

private:

	using AntParamsName = ant::ant_colony_params_initializer::paramsName;
	using AntAPI = ant::ant_colony_params_initializer;
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
	* class object_probability
	*			- An ant take probabilities when it have more than one possible next state(cities).
	*			- The ant take an array with probabilities that can be realized by function 'realize_probability'  
	********************************************************/
	class object_probability
	{
	public:
		object_probability(int city_num, double prob)
			:value(city_num, prob)
		{}

#ifdef __CPP_14_ENABLED__
		decltype(auto) get_city_num() const { return value.first; }
		decltype(auto) get_probability() const { return value.second; }
#else
		int get_city_num() const { return value.first; }
		double get_probability() const { return value.second; }
#endif
		void divide_by(double divider) { value.second /= divider; }

	private:
		std::pair<int, double> value;
	};


	/*********************************************************
	* class pheramone
	*			- contains an array with pheramone value for all ways between cities
	********************************************************/
	class pheramone
	{
	public:
		pheramone(std::size_t cityCount, double initialPheramone)
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
	
	std::vector<object_probability> calc_probability(const ant_t& ant, const pheramone& pheramone);
	
	int realize_probability(const ant_t& ant, const std::vector<object_probability>& prob);

	double calc_path_length(const cities_t& cities);

	std::vector<std::vector<double>> calc_delta_pheramone(const std::vector<ant_t>& ants);

	void update_pheramones(pheramone& pheramone, const std::vector<ant_t>& ants);

	void update_shortes_path(cities_t& shortes_path, const std::vector<ant_t>& ants);

#ifdef __CPP_14_ENABLED__
	
	decltype(auto) get_count_city				()				const { return distance->m_matrix.size(); }
	decltype(auto) get_count_ants_in_iteration	()				const { return params->get<AntParamsName::COUNT_ANTS_IN_ITERATION>().get(); }
	decltype(auto) get_random_number			(unsigned max)	const { return (std::rand() % max); }
	decltype(auto) get_initial_pheromone		()				const { return params->get<AntParamsName::INITIAL_PHERAMONE>().get(); }
	decltype(auto) get_count_iterations			()				const { return params->get<AntParamsName::ITERATIONS>().get(); }
	decltype(auto) get_param_ro					()				const { return params->get<AntParamsName::RO>().get(); }
	decltype(auto) get_param_Q					()				const { return params->get<AntParamsName::Q>().get(); }
#else
	
	template <AntParamsName param_name>
	using get_base_param_type = typename std::tuple_element<static_cast<int>(param_name), ant::ant_colony_params_initializer::params_t>::type::type;
	
	std::size_t get_count_city()				const { return distance->m_matrix.size(); }
	unsigned get_random_number(unsigned max)	const { return (std::rand() % max); }

	const AntAPI::get_base_param_type<AntParamsName::COUNT_ANTS_IN_ITERATION>
			get_count_ants_in_iteration()const { return params->get<AntParamsName::COUNT_ANTS_IN_ITERATION>().get(); }

	const AntAPI::get_base_param_type<AntParamsName::INITIAL_PHERAMONE>
			get_initial_pheromone()		const { return params->get<AntParamsName::INITIAL_PHERAMONE>().get(); }

	const AntAPI::get_base_param_type<AntParamsName::ITERATIONS>
			get_count_iterations()		const { return params->get<AntParamsName::ITERATIONS>().get(); }
	
	const AntAPI::get_base_param_type<AntParamsName::RO>
			get_param_ro()				const { return params->get<AntParamsName::RO>().get(); }
	
	const AntAPI::get_base_param_type<AntParamsName::Q>
			get_param_Q()				const { return params->get<AntParamsName::Q>().get(); }
#endif

public:

    std::shared_ptr<ant_colony_result> result;
	std::shared_ptr<city_distance::distance_matrix> distance;
	std::shared_ptr<ant_colony_params> params;

};


}//namespace ant_colony
