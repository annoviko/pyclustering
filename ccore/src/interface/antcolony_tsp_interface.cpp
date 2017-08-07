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

#include "interface/antcolony_tsp_interface.h"

#include "tsp/ant_colony.hpp"


pyclustering_package * antcolony_tsp_process_get_result(std::shared_ptr<city_distance::distance_matrix>& dist, const ant::ant_colony_tsp_params * algorithm_params) {
    using ant_api = ant::ant_colony_TSP_params_initializer;
    auto algo_params = ant::ant_colony_TSP_params::make_param
        ( ant_api::Q_t{ algorithm_params->q },
          ant_api::Ro_t{ algorithm_params->ro },
          ant_api::Alpha_t{ algorithm_params->alpha },
          ant_api::Beta_t{ algorithm_params->beta },
          ant_api::Gamma_t{ algorithm_params->gamma },
          ant_api::InitialPheramone_t{ algorithm_params->initial_pheramone },
          ant_api::Iterations_t{ algorithm_params->iterations },
          ant_api::CountAntsInIteration_t{ algorithm_params->count_ants_in_iteration }  );

    ant::ant_colony ant_algo{ dist, algo_params };
    auto algo_res = ant_algo.process();

    pyclustering_package * package = new pyclustering_package(pyclustering_type_data::PYCLUSTERING_TYPE_LIST);
    package->size = 2;   /* path length */
    package->data = new pyclustering_package * [package->size];

    std::vector<double> path_length_storage = { algo_res->path_length };
    ((pyclustering_package **) package->data)[0] = create_package(&path_length_storage);
    ((pyclustering_package **) package->data)[1] = create_package(&algo_res->shortest_path);

    return package;
}


pyclustering_package * antcolony_tsp_process_by_matrix(const pyclustering_package * objects_coord, const void * ant_colony_parameters) {
    dataset matrix;
    objects_coord->extract(matrix);

    auto dist = city_distance::distance_matrix::make_city_distance_matrix(matrix);
    return antcolony_tsp_process_get_result(dist, static_cast<const ant::ant_colony_tsp_params *>(ant_colony_parameters) );
}


pyclustering_package * antcolony_tsp_process(const pyclustering_package * objects_coord, const void * ant_colony_parameters) {
    const ant::ant_colony_tsp_params * algorithm_params = (const ant::ant_colony_tsp_params *) ant_colony_parameters;

#if 1
    dataset coordinates;
    objects_coord->extract(coordinates);

    std::vector<city_distance::object_coordinate> cities;
    for (auto & coordinate : coordinates) {
        cities.push_back(coordinate);
    }
#else
    std::vector<city_distance::object_coordinate> cities;
    objects_coord->extract(cities);
#endif

    auto dist = city_distance::distance_matrix::make_city_distance_matrix(cities);
    return antcolony_tsp_process_get_result(dist, algorithm_params);
}