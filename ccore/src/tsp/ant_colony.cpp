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

#include "tsp/ant_colony.hpp"

#include <algorithm>



namespace ant
{


void ant_colony::place_ants_randomly(std::vector<ant_t>& ants)
{
    for (auto& ant : ants)
    {
        ant.curState = get_random_number(get_count_city());
        ant.visited.push_back(ant.curState);
    }
}


std::vector<ant_colony::object_probability> ant_colony::calc_probability(const ant_t& ant, const pheramone& pheramone)
{
    std::vector<object_probability> prob;
    double commonDivider = 0;

    for (std::size_t city_num = 0; city_num < get_count_city(); ++city_num)
    {
        if (std::find(ant.visited.begin(), ant.visited.end(), city_num) == ant.visited.end())
        {
            double p = std::pow(pheramone[ant.curState][city_num], get_param_alpha())
                *  (1 / distance->get_matrix()[ant.curState][city_num]);

            prob.emplace_back(city_num, p);
            commonDivider += p;
        }
    }

    for (auto& e : prob) e.divide_by(commonDivider);

    return prob;
}


int ant_colony::realize_probability(const ant_t& ant, const std::vector<object_probability>& prob)
{
    double reailized = static_cast<double>(get_random_number(RAND_MAX)) / RAND_MAX;
    double commulated_prob = 0;

    for (const auto& p : prob)
    {
        commulated_prob += p.get_probability();
        if (commulated_prob > reailized) return p.get_city_num();
    }

    return prob[prob.size() - 1].get_city_num();
}


double ant_colony::calc_path_length(const cities_t& cities)
{
    double pathLength = 0;

    for (size_t i = 0; i < cities.size(); ++i)
    {
        pathLength += distance->get_matrix()[cities[i]][cities[(i + 1) % cities.size()]];
    }

    return pathLength;
}


std::vector<std::vector<double>> ant_colony::calc_delta_pheramone(const std::vector<ant_t>& ants)
{
    std::vector<std::vector<double>> deltaPh(get_count_city(), std::vector<double>(get_count_city(), 0));
    std::vector<double> lengthTour(ants.size(), 0.0);

    for (const auto& ant : ants)
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


void ant_colony::update_pheramones(pheramone& pheramone, const std::vector<ant_t>& ants)
{
    if (get_count_city() == 0) return;

    auto deltaPheramone = calc_delta_pheramone(ants);

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


void ant_colony::update_shortes_path(cities_t& shortes_path, const std::vector<ant_t>& ants)
{
    int antWithShortesPath = -1;
    double curShortesLength = -1;

    for (std::size_t ant_num = 0; ant_num < ants.size(); ++ant_num)
    {
        double pathLen = calc_path_length(ants[ant_num].visited);
        if (curShortesLength == -1 || curShortesLength > pathLen)
        {
            antWithShortesPath = ant_num;
            curShortesLength = pathLen;
        }
    }

    if (shortes_path.size() == 0)
    {
        shortes_path = ants[antWithShortesPath].visited;
    }
    else
    {
        double pathLenShortes = calc_path_length(shortes_path);
        if (pathLenShortes > curShortesLength)
        {
            shortes_path = ants[antWithShortesPath].visited;
        }
    }

}


std::shared_ptr<ant_colony_result> ant_colony::process()
{
    // without this check program would be crashed
    if (get_count_ants_in_iteration() == 0)
    {
        return result;
    }

    // initialize random number generator
    std::srand(static_cast<unsigned>(std::time(0)));

    const unsigned cityCount = get_count_city();
    cities_t shortestPath;

    // initiate pheramones to value from params
    pheramone pheramone(cityCount, get_initial_pheromone());

    for (unsigned iteration = 0; iteration < get_count_iterations(); ++iteration)
    {
        std::vector<ant_t> v_ants(get_count_ants_in_iteration());

        // randomly place ants in cities
        place_ants_randomly(v_ants);

        // Ants should go throw all cities
        for (unsigned step = 0; step < cityCount; ++step)
        {
            for (auto & ant : v_ants)
            {
                auto prob = calc_probability(ant, pheramone);

                if (prob.size() == 0) continue;

                int next_city = realize_probability(ant, prob);

                // refresh an ant state
                ant.curState = next_city;
                ant.visited.push_back(ant.curState);
            }
        }

        // update pheramones
        update_pheramones(pheramone, v_ants);

        // find shortest path
        update_shortes_path(shortestPath, v_ants);
    }

    result->shortest_path = shortestPath;
    result->path_length = calc_path_length(result->shortest_path);

    return    result;
}


}//namespace ant_colony

