/**
*
* Copyright (C) 2014-2017    Andrei Novikov (pyclustering@yandex.ru)
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

#include "interface/antmean_interface.h"

#include "cluster/antmean.hpp"


pyclustering_package * antmean_algorithm(const pyclustering_package * const sample, const void * p_ant_clustering_params, unsigned int count_clusters)
{
    const ant::s_ant_clustering_params * algorithm_params = (const ant::s_ant_clustering_params *) p_ant_clustering_params;

    using AntCAPI = ant::ant_colony_clustering_params_initializer;

    auto params_ant_clustering = ant::ant_clustering_params::make_param(
      AntCAPI::RO_t(algorithm_params->ro),
      AntCAPI::Pheramone_init_t(algorithm_params->pheramone_init),
      AntCAPI::Iterations_t(algorithm_params->iterations),
      AntCAPI::Count_ants_t(algorithm_params->count_ants)
    );

    dataset input_points;
    sample->extract(input_points);

    cluster_analysis::cluster_data result;

    ant::ant_clustering_mean ant_mean_clustering{ params_ant_clustering, count_clusters };
    ant_mean_clustering.process(input_points, result);

    pyclustering_package * package = create_package(result.clusters().get());

    return package;
}