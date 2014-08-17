#ifndef _SUPPORT_H_
#define _SUPPORT_H_

#include <string>
#include <fstream>
#include <sstream>

#include <vector>
#include <cmath>
#include <algorithm>

#include "interface_ccore.h"
#include "network.h"


typedef struct differential_result {
	double time;
	double value;
} differential_result;


inline double pi(void) { return (double) 3.14159265358979323846; }

/***********************************************************************************************
 *
 * @brief   Calculates square of Euclidean distance between points.
 *
 * @param   (in) point1     - point #1 that is represented by coordinates.
 *          (in) point2     - point #2 that is represented by coordinates.
 *
 * @return  Returns square of Euclidean distance between points.
 *
 ***********************************************************************************************/
inline double euclidean_distance_sqrt(const std::vector<double> * const point1, const std::vector<double> * const point2) {
	double distance = 0.0;
	/* assert(point1->size() != point1->size()); */
	for (unsigned int dimension = 0; dimension < point1->size(); dimension++) {
		double difference = (point1->data()[dimension] - point2->data()[dimension]);
		distance += difference * difference;
	}

	return distance;
}

/***********************************************************************************************
 *
 * @brief   Calculates Euclidean distance between points.
 *
 * @param   (in) point1     - point #1 that is represented by coordinates.
 *          (in) point2     - point #2 that is represented by coordinates.
 *
 * @return  Returns Euclidean distance between points.
 *
 ***********************************************************************************************/
inline double euclidean_distance(const std::vector<double> * const point1, const std::vector<double> * const point2) {
	double distance = 0.0;
	/* assert(point1->size() != point1->size()); */
	for (unsigned int dimension = 0; dimension < point1->size(); dimension++) {
		double difference = (point1->data()[dimension] - point2->data()[dimension]);
		distance += difference * difference;
	}

	return std::sqrt(distance);
}

/***********************************************************************************************
 *
 * @brief   Reads sample (input data) from the specified file.
 *
 * @param   (in) path_file  - path to the file with data.
 *
 * @return  Returns internal type of representation of input data.
 *
 ***********************************************************************************************/
std::vector<std::vector<double> > * read_sample(const char * const path_file);

/***********************************************************************************************
 *
 * @brief   Converts representation of data from CCORE standard to internal.
 *
 * @param   (in) sample     - input data (sample) for converting.
 *
 * @return  Returns internal type of representation of input data.
 *
 ***********************************************************************************************/
std::vector<std::vector<double> > * read_sample(const data_representation * const sample);

/***********************************************************************************************
 *
 * @brief   Converts representation of cluster to standard type of CCORE interface.
 *
 * @param   (in) clusters   - input clusters for converting.
 *
 * @return  Returns standard type of representation of clusters.
 *
 ***********************************************************************************************/
clustering_result * create_clustering_result(const std::vector<std::vector<unsigned int> *> * const clusters);

/***********************************************************************************************
 *
 * @brief   Returns average distance for establish links between specified number of neighbors.
 *
 * @param   (in) points         - input data.
 * @param   (in) num_neigh      - number of neighbors.
 *
 * @return  Returns average distance for establish links between 'num_neigh' in data set 'points'.
 *
 ***********************************************************************************************/
double average_neighbor_distance(const std::vector<std::vector<double> > * points, const unsigned int num_neigh);

/***********************************************************************************************
 *
 * @brief   Runge-Kutta 4 solver.
 *
 * @param   (in) function_pointer   - pointer to function.
 *          (in) initial_value      - initial values.
 *          (in) a                  - left point (start time).
 *          (in) b                  - right point (end time).
 *          (in) steps              - number of steps.
 *          (in) argv               - extra arguments are required by function_pointer.
 *
 * @return  Returns full result of integration (each step of integration).
 *
 ***********************************************************************************************/
std::vector<differential_result> * rk4(double (*function_pointer)(const double t, const double val, const std::vector<void *> & argv), double initial_value, const double a, const double b, const unsigned int steps, const std::vector<void *> & argv);

/***********************************************************************************************
 *
 * @brief   Runge-Kutta-Felhberg (RKF45) solver.
 *
 * @param   (in) function_pointer   - pointer to function.
 *          (in) initial_value      - initial values.
 *          (in) a                  - left point (start time).
 *          (in) b                  - right point (end time).
 *          (in) tolerance          - acceptable error for solving.
 *          (in) argv               - extra arguments are required by function_pointer.
 *
 * @return	Returns full result of integration (each step of integration).
 *
 ***********************************************************************************************/
std::vector<differential_result> * rkf45(double (*function_pointer)(const double t, const double val, const std::vector<void *> & argv), double initial_value, const double a, const double b, const double tolerance, const std::vector<void *> & argv);

#endif
