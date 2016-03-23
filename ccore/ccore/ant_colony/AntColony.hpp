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
	std::vector<int> shortesPath;
	double pathLen;
};


/***********************************************************************************************
* template <typename T> class Ant_colony
*                          - main class for Ant Colony Optimization
*
*
***********************************************************************************************/
template<typename T>
class AntColony
{

public:
	AntColony(const std::shared_ptr<city_distance::CityDistanceMatrix<T>>& init_distance
			, const std::shared_ptr<AntColonyAlgorithmParams>& init_params)
		: result(new AntColonyResult)
		, distance(init_distance)
		, params(init_params)
	{}

	decltype(auto) process();

	decltype(auto) get_result() { return result; }

private:

	using AntAPI = ant_colony::AntColonyAlgorithmParamsInitializer::paramsName;

	struct ant_t
	{
		std::vector<int> visited;
		int cur_state;
	};

	void place_ants_randomly(std::vector<ant_t>& ants);
	
	std::vector<std::pair<int, double>> calc_probability(const ant_t& ant, const std::vector<std::vector<double>>& pheramone);
	
	int realize_probability(const ant_t& ant, const std::vector<std::pair<int, double>>& prob);

	double calc_path_length(const std::vector<int>& cities);

	std::vector<std::vector<double>> calc_delta_pheramone(const std::vector<ant_t>& vAnts);

	void update_pheramones(std::vector<std::vector<double>>&pheramone, const std::vector<ant_t>& v_ants);

	void update_shortes_path(std::vector<int>& shortes_path, const std::vector<ant_t>& vAnts);



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
	std::shared_ptr<city_distance::CityDistanceMatrix<T>> distance;
	std::shared_ptr<AntColonyAlgorithmParams> params;

};










template<typename T>
void AntColony<T>::place_ants_randomly(std::vector<ant_t>& ants)
{
	for (auto& ant : ants)
	{
		ant.cur_state = get_random_number(get_count_city());
		ant.visited.push_back(ant.cur_state);
	}
}


template<typename T>
std::vector<std::pair<int, double>> AntColony<T>::calc_probability(const ant_t& ant, const std::vector<std::vector<double>>& pheramone)
{
	std::vector<std::pair<int,double>> prob;
	double common_delim = 0;

	for (std::size_t i = 0; i < get_count_city(); ++i)
	{
		if (std::find(ant.visited.begin(), ant.visited.end(), i) == ant.visited.end())
		{
			double p = std::pow(pheramone[ant.cur_state][i], params->get<AntAPI::ALPHA>().get())
				*  (1 / distance->get_matrix()[ant.cur_state][i]);
			
			prob.emplace_back(i, p);
			common_delim += p;
		}
	}

	for (std::size_t i = 0; i < prob.size(); ++i)
	{
		prob[i].second /= common_delim;
	}

	return prob;
}


template<typename T>
int AntColony<T>::realize_probability(const ant_t& ant, const std::vector<std::pair<int,double>>& prob)
{
	double reailized = static_cast<double>(get_random_number(RAND_MAX)) / RAND_MAX;
	double commulated_prob = 0;

	for (std::size_t i = 0; i < prob.size(); ++i)
	{
		commulated_prob += prob[i].second;
		if (commulated_prob > reailized) return prob[i].first;
	}

	return prob[prob.size()-1].first;
}


template<typename T>
double AntColony<T>::calc_path_length(const std::vector<int>& cities)
{
	double pathLength = 0;

	for (size_t i = 0; i < cities.size(); ++i)
	{
		pathLength += distance->get_matrix()[cities[i]][cities[(i + 1) % cities.size()]];
	}

	return pathLength;
}


template<typename T>
std::vector<std::vector<double>> AntColony<T>::calc_delta_pheramone(const std::vector<ant_t>& vAnts)
{
	std::vector<std::vector<double>> deltaPh (get_count_city(), std::vector<double>(get_count_city(), 0));
	std::vector<double> lengthTour(vAnts.size(), 0.0);

	for (const auto& ant : vAnts)
	{
		double lengthTour = calc_path_length(ant.visited);

		for (size_t i = 0; i < ant.visited.size(); ++i)
		{
			deltaPh[ant.visited[i]][ant.visited[(i + 1) % ant.visited.size()]] += get_param_Q() / lengthTour;
			deltaPh[ant.visited[(i + 1) % ant.visited.size()]][ant.visited[i]] = deltaPh[ant.visited[i]][ant.visited[(i + 1) % ant.visited.size()]];
		}
	}

	return deltaPh;
}


template<typename T>
void AntColony<T>::update_pheramones(std::vector<std::vector<double>>&pheramone, const std::vector<ant_t>& v_ants)
{
	if (get_count_city() == 0) return;
	
	auto deltaPheramone = calc_delta_pheramone(v_ants);
	
	for (std::size_t city_from = 0; city_from < get_count_city() - 1; ++city_from)
	{
		for (std::size_t city_to = city_from + 1; city_to < get_count_city(); ++city_to)
		{
			pheramone[city_from][city_to]
				= get_param_ro() * pheramone[city_from][city_to] + deltaPheramone[city_from][city_to];
			pheramone[city_to][city_from] = pheramone[city_from][city_to];
		}
	}
}


template<typename T>
void AntColony<T>::update_shortes_path(std::vector<int>& shortes_path, const std::vector<ant_t>& vAnts)
{
	int antWithShortesPath = -1;
	double curShortesLength = -1;

	for (std::size_t ant_num = 0; ant_num < vAnts.size(); ++ant_num)
	{
		double pathLen = calc_path_length(vAnts[ant_num].visited);
		if (curShortesLength == -1 || curShortesLength > pathLen)
		{
			antWithShortesPath = ant_num;
			curShortesLength = pathLen;
		}
	}

	if (shortes_path.size() == 0)
	{
		shortes_path = vAnts[antWithShortesPath].visited;
	}
	else
	{
		double pathLenShortes = calc_path_length(shortes_path);
		if (pathLenShortes > curShortesLength)
		{
			shortes_path = vAnts[antWithShortesPath].visited;
		}
	}

}


template<typename T>
decltype(auto) AntColony<T>::process()
{
	std::srand(static_cast<unsigned>(std::time(0)));
	const unsigned city_count = get_count_city();
	std::vector<int> shortes_path;

	//initiate pheramones to value from params
	std::vector<std::vector<double>>
		pheramone(city_count, std::vector<double>(city_count, static_cast<double>(get_initial_pheromone())));

	for (unsigned iteration = 0; iteration < get_count_iterations(); ++iteration)
	{
		std::vector<ant_t> v_ants(get_count_ants_in_iteration());
		
		// randomly place ants in cities
		place_ants_randomly(v_ants);

		// Ants should go throw all cities
		for (unsigned step = 0; step < city_count; ++step)
		{
			for (auto & ant : v_ants)
			{
				std::vector<std::pair<int,double>> 
					prob = calc_probability(ant, pheramone);
				
				if (prob.size() == 0) continue;

				int next_city = realize_probability(ant, prob);
			
				// refresh an ant state
				ant.cur_state = next_city;
				ant.visited.push_back(ant.cur_state);
			}
		}

		// update pheramones
		update_pheramones(pheramone, v_ants);

		// find shortest path
		update_shortes_path(shortes_path, v_ants);
	}

	result->shortesPath = shortes_path;
	result->pathLen = calc_path_length(result->shortesPath);

	std::cout << "\n\n TEST RESULT \n";
	for (std::size_t i = 0; i < shortes_path.size(); ++i)
	{
		std::cout << "Visit : " << shortes_path[i] << ",   ";
	}
	std::cout << std::endl;
	std::cout << "Path length : " << (result->pathLen) << std::endl;

	return	result;
}





}//namespace ant_colony
