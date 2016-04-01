#include "city_distance_matrix.hpp"


namespace city_distance
{


/***********************************************************************************************
* CityCoord;
*              - contains coordinates of a city
***********************************************************************************************/
double CityCoord::get_distance(const CityCoord& to_city) const
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
* class CityDistanceMatrix
*                          - contains distance matrix between all cities
***********************************************************************************************/
CityDistanceMatrix::CityDistanceMatrix(const std::vector<CityCoord>& cities)
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