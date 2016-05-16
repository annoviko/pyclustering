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

#include <ctime>

#include "cluster/ant_clustering_mean.hpp"


namespace ant {


std::shared_ptr<ant_clustering_result> ant_clustering_mean::process(const clustering_data& input, std::size_t count_clusters)
{
    assert(count_clusters > 0);
    assert(input.data.size() >= count_clusters);

    std::size_t dimension = input.data[0].size();

    std::vector<std::vector<bool>> best_clustering;

    // initialize random number generator
    std::srand(static_cast<unsigned>(std::time(0)));

    // init pheramone
    pheramone ph(input.data.size(), count_clusters, get_pheramone_init());
    // create agents
    std::vector<Ant> ants(get_count_ants(), Ant(input.data.size(), count_clusters));

    auto max_iterations = get_iterations();
    for (unsigned iteration = 0; iteration < max_iterations; ++iteration)
    {
        //realize probability
        clustering_by_pheramone(ph, input, ants);

        calculate_F(ants, input, count_clusters, dimension);
        update_pheramone(ph, ants, input.data.size(), count_clusters);

        update_best_clustering(ants, best_clustering);

        // clear agents to use it in a next iteration
        // if this is a not last turn
        if (iteration + 1 < max_iterations)
            for (auto& ant : ants) ant.clear();
    }

    auto result = std::shared_ptr<ant_clustering_result>(new ant_clustering_result());
    result->clusters = best_clustering;

    return  result;
}


void ant_clustering_mean::clustering_by_pheramone(const pheramone& ph, const clustering_data& input, std::vector<Ant>& ants)
{
    for (auto& ant : ants)
    {
        for (std::size_t data_num = 0; data_num < input.data.size(); ++data_num)
        {
            std::size_t cluster = realize_pheromone(ph, data_num);
            ant.clustering_data[data_num][cluster] = true;
        }
    }
}


std::size_t ant_clustering_mean::realize_pheromone(const pheramone& ph, std::size_t data_num)
{
    const std::size_t count_clusters = ph[data_num].size();
    double sum_ph{ 0 };

    for (const auto& elem : ph[data_num])
        sum_ph += elem;

    assert(sum_ph > 0.0001);

    double reailized = static_cast<double>(get_random_number(RAND_MAX)) / RAND_MAX;
    double commulated_prob = 0;

    for (std::size_t i = 0; i < count_clusters; ++i)
    {
        commulated_prob += ph[data_num][i] / sum_ph;
        if (commulated_prob > reailized) return i;
    }

    return     (count_clusters > 0) ? count_clusters - 1 : 0;
}


void ant_clustering_mean::calculate_F(std::vector<Ant>& ants, const clustering_data& input, std::size_t count_clusters, std::size_t dimension)
{
    for (auto& ant : ants)
    {
        // calc center for each cluster
        std::vector<std::vector<double>> cluster_centers(count_clusters, std::vector<double>(dimension, 0.0));

        calculate_cluster_centers(input, ant, cluster_centers, count_clusters, dimension);

        // calc F
        ant.F = 0.0;
        for (std::size_t i = 0; i < input.data.size(); ++i)
        {
            for (std::size_t cluster = 0; cluster < count_clusters; ++cluster)
            {
                if (true == ant.clustering_data[i][cluster])
                {
                    for (std::size_t dim = 0; dim < dimension; ++dim)
                        ant.F +=  (input.data[i][dim] - cluster_centers[cluster][dim])
                                * (input.data[i][dim] - cluster_centers[cluster][dim]);

                }
            }
        }
    }
}


void ant_clustering_mean::calculate_cluster_centers(const clustering_data& input
                                                    , Ant& ant
                                                    , std::vector<std::vector<double>>& cluster_centers
                                                    , std::size_t count_clusters
                                                    , std::size_t dimension)
{
    std::vector<unsigned> count_samples_in_cluster(count_clusters, 0);

    for (std::size_t i = 0; i < input.data.size(); ++i)
    {
        for (std::size_t cluster = 0; cluster < count_clusters; ++cluster)
        {
            if (true == ant.clustering_data[i][cluster])
            {
                for (std::size_t dim = 0; dim < dimension; ++dim)
                    cluster_centers[cluster][dim] += input.data[i][dim];

                ++count_samples_in_cluster[cluster];
            }
        }
    }

    for (std::size_t cluster = 0; cluster < count_clusters; ++cluster)
    {
        if (0 != count_samples_in_cluster[cluster])
        {
            for (std::size_t dim = 0; dim < dimension; ++dim)
                cluster_centers[cluster][dim] /= count_samples_in_cluster[cluster];
        }
    }
}


void ant_clustering_mean::update_pheramone(pheramone& ph, const std::vector<Ant>& ants, std::size_t size_of_data, std::size_t count_clusters)
{
    for (std::size_t i = 0; i < size_of_data; ++i)
    {
        for (std::size_t cluster = 0; cluster < count_clusters; ++cluster)
        {
            ph[i][cluster] = (1.0 - get_ro()) * ph[i][cluster];

            for (const auto& ant : ants)
            {
                if (true == ant.clustering_data[i][cluster])
                    ph[i][cluster] += 1.0 / ant.F;
            }
        }
    }
}


void ant_clustering_mean::update_best_clustering(const std::vector<Ant>& ants, std::vector<std::vector<bool>>& best_clustering)
{
    std::size_t best = 0;

    for (std::size_t ant_num = 1; ant_num < ants.size(); ++ant_num)
    {
        if (ants[ant_num].F < ants[best].F)
            best = ant_num;
    }

    best_clustering = ants[best].clustering_data;
}

}// namespace ant
