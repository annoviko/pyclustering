/*
 * city_distance.hpp
 *
 *  Created on: Mar 21, 2016
 *      Author: alex
 */

#pragma once

#include <cmath>
#include <memory>
#include <vector>
#include <initializer_list>


namespace city_distance
{

/***********************************************************************************************
 * template<typename T> CityCoord;
 *              - contains coordinates of a city
 *
 * example for initialization by initializer list:
 *      ant_colony::CityCoord<double> Piter  {4.0, 3.0};
 *      ant_colony::CityCoord<double> Moscow {14.0, 22.0};
 *      ant_colony::CityCoord<double> Zero   {0.0, 0.0};
 *
 ***********************************************************************************************/
template<typename T>
class CityCoord
{
public:

    CityCoord(std::initializer_list<T> init_coord)
    {
        for (auto e : init_coord)
        {
            location_point.push_back(e);
        }
    }

    double get_distance (const CityCoord& to_city) const;

    decltype(auto) get_dimention() const { return location_point.size(); }


private:
    std::vector<T> location_point;


}; //end class CityCoord


template<typename T>
double CityCoord<T>::get_distance(const CityCoord<T>& to_city) const
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
 * template <typename T> class CityDistanceMatrix
 *                          - contains distance matrix between all cities
 *
 * auto dist = city_distance::CityDistanceMatrix<double>::make_city_distance_matrix
 *					({ Piter, Zero, Moscow });
 *
***********************************************************************************************/
template <typename T>
class CityDistanceMatrix
{
public:
	// fabric functions for initiating by matrix
	static decltype(auto) make_city_distance_matrix(const std::vector<std::vector<T>>& init_distance)
	{
		return std::shared_ptr<CityDistanceMatrix>(new CityDistanceMatrix(init_distance));
	}

	// fabric functions for initiating by matrix with move semantic
	static decltype(auto) make_city_distance_matrix(std::vector<std::vector<T>>&& init_distance)
	{
		return std::shared_ptr<CityDistanceMatrix>(new CityDistanceMatrix(std::move(init_distance)));
	}

	// fabric functions for initiating by list with city's coordinates
	static decltype(auto) make_city_distance_matrix(const std::vector<CityCoord<T>>& cities)
	{
		return std::shared_ptr<CityDistanceMatrix>(new CityDistanceMatrix(cities));
	}

private:
	// constructor for initiating by matrix
    CityDistanceMatrix(const std::vector<std::vector<T>>& init_distance)
    {
        distance = init_distance;
    }

	// constructor for initiating by matrix with move semantic
    CityDistanceMatrix(std::vector<std::vector<T>>&& init_distance)
    {
        distance = std::move(init_distance);
    }

	// constructor for initiating by list with city's coordinates
    CityDistanceMatrix(const std::vector<CityCoord<T>>& cities);


public:
    std::vector<std::vector<T>> distance;
}; //end CityDistanceMatrix



template <typename T>
CityDistanceMatrix<T>::CityDistanceMatrix(const std::vector<CityCoord<T>>& cities)
{
    // Resize matrix to able contains all the cities
    distance.resize(cities.size());
    for (std::size_t i = 0; i < cities.size(); ++i)
    {
        distance[i].resize(cities.size());
    }

    // initialize distance matrix
    for (std::size_t city_from = 0; city_from < cities.size(); ++city_from)
    {
        for (std::size_t city_to = 0; city_to < cities.size(); ++city_to)
        {
            distance[city_from][city_to] = cities[city_from].get_distance(cities[city_to]);
        }
    }
}



}//namespace city_distance
