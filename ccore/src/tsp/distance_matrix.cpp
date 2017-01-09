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

#include "tsp/distance_matrix.hpp"


namespace city_distance
{


/***********************************************************************************************
* object_coordinate;
*              - contains coordinates of a city
***********************************************************************************************/
double object_coordinate::get_distance(const object_coordinate& to_city) const
{
    if (get_dimention() != to_city.get_dimention()) return -1.0;

    double res = 0;
    for (std::size_t i = 0; i < get_dimention(); ++i)
    {
        res += (location_point[i] - to_city.location_point[i]) * (location_point[i] - to_city.location_point[i]);
    }

    return std::sqrt(res);
}


/***********************************************************************************************
* class distance_matrix
*                          - contains distance matrix between all cities
***********************************************************************************************/
distance_matrix::distance_matrix(const std::vector<object_coordinate>& cities)
{
    // Resize matrix to able contains all the cities
    m_matrix.resize(cities.size());
    for (std::size_t i = 0; i < cities.size(); ++i)
    {
        m_matrix[i].resize(cities.size());
    }

    // initialize distance matrix
    for (std::size_t city_from = 0; city_from < cities.size(); ++city_from)
    {
        for (std::size_t city_to = 0; city_to < cities.size(); ++city_to)
        {
            m_matrix[city_from][city_to] = cities[city_from].get_distance(cities[city_to]);
        }
    }
}


}//namespace city_distance
