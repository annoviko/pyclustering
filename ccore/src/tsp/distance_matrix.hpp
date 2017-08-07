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

#include <cmath>
#include <memory>
#include <vector>
#include <initializer_list>


namespace city_distance
{

/***********************************************************************************************
*
* @brief   Contains coordinates of a city.
*
* Example for city coordinate creation by initializer list:
* @code
*      ant_colony::object_coordinate Piter  {4.0, 3.0};
*      ant_colony::object_coordinate Moscow {14.0, 22.0};
*      ant_colony::object_coordinate Zero   {0.0, 0.0};
* @endcode
*
***********************************************************************************************/
class object_coordinate
{
public:
    object_coordinate(std::initializer_list<double> init_coord)
    {
        for (auto e : init_coord)
        {
            location_point.push_back(e);
        }
    }

    object_coordinate(const std::vector<double> & init_coord)
    {
        for (auto e : init_coord)
        {
            location_point.push_back(e);
        }
    }

    object_coordinate(std::vector<double> && init_coord)
    {
        for (auto e : init_coord)
        {
            location_point.push_back(std::move(e));
        }
    }

    double get_distance (const object_coordinate & to_city) const;

    std::size_t get_dimention() const { return location_point.size(); }

private:
    std::vector<double> location_point;
};




/***********************************************************************************************
 * class distance_matrix
 *                          - contains distance matrix between all cities
 *
 * auto dist = city_distance::distance_matrix::make_city_distance_matrix
 *                    ({ Piter, Zero, Moscow });
 *
***********************************************************************************************/
class distance_matrix
{
public:
    using array_coordinate = std::vector<std::vector<double>>;

    // fabric functions for initiating by matrix
    static std::shared_ptr<distance_matrix>
    make_city_distance_matrix(const array_coordinate& init_distance)
    {
        return std::shared_ptr<distance_matrix>(new distance_matrix(init_distance));
    }

    // fabric functions for initiating by matrix with move semantic
    static std::shared_ptr<distance_matrix>
    make_city_distance_matrix(array_coordinate&& init_distance)
    {
        return std::shared_ptr<distance_matrix>(new distance_matrix(std::move(init_distance)));
    }

    // fabric functions for initiating by list with city's coordinates
    static std::shared_ptr<distance_matrix>
    make_city_distance_matrix(const std::vector<object_coordinate>& cities)
    {
        return std::shared_ptr<distance_matrix>(new distance_matrix(cities));
    }

    // return reference out of class is a bad idea!!! (TODO: shared_ptr)
    array_coordinate & get_matrix() { return m_matrix; }

private:
    // constructor for initiating by matrix
    distance_matrix(const array_coordinate & init_distance) {
        m_matrix = init_distance;
    }

    // constructor for initiating by matrix with move semantic
    distance_matrix(array_coordinate && init_distance) {
        m_matrix = std::move(init_distance);
    }

    // constructor for initiating by list with city's coordinates
    distance_matrix(const std::vector<object_coordinate> & cities);

public:
    array_coordinate    m_matrix;
};




}//namespace city_distance
