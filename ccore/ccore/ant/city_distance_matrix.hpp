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
*      ant_colony::CityCoord Piter  {4.0, 3.0};
*      ant_colony::CityCoord Moscow {14.0, 22.0};
*      ant_colony::CityCoord Zero   {0.0, 0.0};
* @endcode
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

    CityCoord(const std::vector<double> & init_coord)
    {
        for (auto e : init_coord)
        {
            location_point.push_back(e);
        }
    }

    CityCoord(std::vector<double> && init_coord)
    {
        for (auto e : init_coord)
        {
            location_point.push_back(std::move(e));
        }
    }

    double get_distance (const CityCoord & to_city) const;

    inline size_t get_dimention() const { return location_point.size(); }


private:
    std::vector<double> location_point;


};


typedef std::vector<std::vector<double>>    array_coordinate;

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
    static auto make_city_distance_matrix(const array_coordinate & init_distance) -> std::shared_ptr<CityDistanceMatrix> {
        return std::shared_ptr<CityDistanceMatrix>(new CityDistanceMatrix(init_distance));
    }	

	// fabric functions for initiating by matrix with move semantic
    static auto make_city_distance_matrix(const array_coordinate && init_distance) -> std::shared_ptr<CityDistanceMatrix> {
		return std::shared_ptr<CityDistanceMatrix>(new CityDistanceMatrix(std::move(init_distance)));
	}

	// fabric functions for initiating by list with city's coordinates
    static auto make_city_distance_matrix(const std::vector<CityCoord> & cities) -> std::shared_ptr<CityDistanceMatrix> {
        return std::shared_ptr<CityDistanceMatrix>(new CityDistanceMatrix(cities));
    }

	// return reference out of class is a bad idea!!! (TODO: shared_ptr)
	std::vector<std::vector<double>> & get_matrix() { return m_matrix; }


private:
	// constructor for initiating by matrix
    CityDistanceMatrix(const array_coordinate & init_distance) {
		m_matrix = init_distance;
    }

	// constructor for initiating by matrix with move semantic
    CityDistanceMatrix(array_coordinate && init_distance) {
		m_matrix = std::move(init_distance);
    }

	// constructor for initiating by list with city's coordinates
	CityDistanceMatrix(const std::vector<CityCoord> & cities);

public:
    array_coordinate    m_matrix;
};




}//namespace city_distance
