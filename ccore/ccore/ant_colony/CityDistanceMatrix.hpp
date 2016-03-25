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
 * CityCoord;
 *              - contains coordinates of a city
 *
 * example for initialization by initializer list:
 *      ant_colony::CityCoord<double> Piter  {4.0, 3.0};
 *      ant_colony::CityCoord<double> Moscow {14.0, 22.0};
 *      ant_colony::CityCoord<double> Zero   {0.0, 0.0};
 *
 ***********************************************************************************************/
class CityCoord
{
public:

    CityCoord(std::initializer_list<double> init_coord)
    {
        for (auto e : init_coord)
        {
            location_point.push_back(e);
        }
    }

    double get_distance (const CityCoord& to_city) const;

    decltype(auto) get_dimention() const { return location_point.size(); }


private:
    std::vector<double> location_point;


}; //end class CityCoord


/***********************************************************************************************
 * class CityDistanceMatrix
 *                          - contains distance matrix between all cities
 *
 * auto dist = city_distance::CityDistanceMatrix::make_city_distance_matrix
 *					({ Piter, Zero, Moscow });
 *
***********************************************************************************************/
class CityDistanceMatrix
{
public:
	// fabric functions for initiating by matrix
	static decltype(auto) make_city_distance_matrix(const std::vector<std::vector<double>>& init_distance)
	{
		return std::shared_ptr<CityDistanceMatrix>(new CityDistanceMatrix(init_distance));
	}

	// fabric functions for initiating by matrix with move semantic
	static decltype(auto) make_city_distance_matrix(std::vector<std::vector<double>>&& init_distance)
	{
		return std::shared_ptr<CityDistanceMatrix>(new CityDistanceMatrix(std::move(init_distance)));
	}

	// fabric functions for initiating by list with city's coordinates
	static decltype(auto) make_city_distance_matrix(const std::vector<CityCoord>& cities)
	{
		return std::shared_ptr<CityDistanceMatrix>(new CityDistanceMatrix(cities));
	}


	// return reference out of class is a bad idea!!! (TODO: shared_ptr)
	std::vector<std::vector<double>>& get_matrix() { return matrix; }


private:
	// constructor for initiating by matrix
    CityDistanceMatrix(const std::vector<std::vector<double>>& init_distance)
    {
		matrix = init_distance;
    }

	// constructor for initiating by matrix with move semantic
    CityDistanceMatrix(std::vector<std::vector<double>>&& init_distance)
    {
		matrix = std::move(init_distance);
    }

	// constructor for initiating by list with city's coordinates
	CityDistanceMatrix(const std::vector<CityCoord>& cities);

public:
    std::vector<std::vector<double>> matrix;
}; //end CityDistanceMatrix




}//namespace city_distance
