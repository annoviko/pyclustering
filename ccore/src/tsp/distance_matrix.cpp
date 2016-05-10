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
