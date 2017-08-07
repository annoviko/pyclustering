/**
*
* Copyright (C) 2014-2017    Kukushkin Aleksey (pyclustering@yandex.ru)
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

#include <memory>
#include <ctime>

#include "tsp/ant_colony_params.hpp"
#include "tsp/distance_matrix.hpp"

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
            , const std::shared_ptr<ant_colony_TSP_params>& initParams)
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

    using ant_api = ant::ant_colony_TSP_params_initializer;
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

    decltype(auto) get_count_city               ()              const { return distance->m_matrix.size(); }
    decltype(auto) get_count_ants_in_iteration  ()              const { return params->get<AntParamsName::COUNT_ANTS_IN_ITERATION>().get(); }
    decltype(auto) get_random_number            (unsigned max)  const { return (std::rand() % max); }
    decltype(auto) get_initial_pheromone        ()              const { return params->get<AntParamsName::INITIAL_PHERAMONE>().get(); }
    decltype(auto) get_count_iterations         ()              const { return params->get<AntParamsName::ITERATIONS>().get(); }
    decltype(auto) get_param_ro                 ()              const { return params->get<AntParamsName::RO>().get(); }
    decltype(auto) get_param_Q                  ()              const { return params->get<AntParamsName::Q>().get(); }
#else

    std::size_t get_count_city()                const { return distance->m_matrix.size(); }
    unsigned get_random_number(unsigned max)    const { return (std::rand() % max); }

    const ant_api::base_param_type<params_name_TSP::COUNT_ANTS_IN_ITERATION>
            get_count_ants_in_iteration()const { return params->get<params_name_TSP::COUNT_ANTS_IN_ITERATION>().get(); }

    const ant_api::base_param_type<params_name_TSP::INITIAL_PHERAMONE>
            get_initial_pheromone()     const { return params->get<params_name_TSP::INITIAL_PHERAMONE>().get(); }

    const ant_api::base_param_type<params_name_TSP::ITERATIONS>
            get_count_iterations()      const { return params->get<params_name_TSP::ITERATIONS>().get(); }

    const ant_api::base_param_type<params_name_TSP::RO>
            get_param_ro()              const { return params->get<params_name_TSP::RO>().get(); }

    const ant_api::base_param_type<params_name_TSP::Q>
            get_param_Q()                   const { return params->get<params_name_TSP::Q>().get(); }

    const ant_api::base_param_type<params_name_TSP::ALPHA>
            get_param_alpha()               const { return params->get<params_name_TSP::ALPHA>().get(); }
#endif

public:

    std::shared_ptr<ant_colony_result> result;
	std::shared_ptr<city_distance::distance_matrix> distance;
	std::shared_ptr<ant_colony_TSP_params> params;

};


}//namespace ant_colony
