#ifndef _SUPPORT_H_
#define _SUPPORT_H_

#include <string>
#include <fstream>
#include <sstream>

#include <vector>
#include <cmath>

#include "interface_ccore.h"
#include "network.h"


typedef struct differential_result {
	double time;
	double value;
} differential_result;



inline double euclidean_distance_sqrt(const std::vector<double> * const point1, const std::vector<double> * const point2) {
	double distance = 0.0;
	/* assert(point1->size() != point1->size()); */
	for (unsigned int dimension = 0; dimension < point1->size(); dimension++) {
		double difference = (point1->data()[dimension] - point2->data()[dimension]);
		distance += difference * difference;
	}

	return distance;
}

inline double euclidean_distance(const std::vector<double> * const point1, const std::vector<double> * const point2) {
	double distance = 0.0;
	/* assert(point1->size() != point1->size()); */
	for (unsigned int dimension = 0; dimension < point1->size(); dimension++) {
		double difference = (point1->data()[dimension] - point2->data()[dimension]);
		distance += difference * difference;
	}

	return std::sqrt(distance);
}

inline double pi(void) { return (double) 3.14159265358979323846; }

std::vector<std::vector<double> > * read_sample(const char * const path_file);

std::vector<std::vector<double> > * read_sample(const data_representation * const sample);

clustering_result * create_clustering_result(const std::vector<std::vector<unsigned int> *> * const clusters);

/***********************************************************************************************
 *
 * @brief   Runge-Kutta 4 solver.
 *
 * @param   (in) function_pointer	- pointer to function.
 *          (in) initial_value		- initial values.
 *          (in) a					- left point (start time).
 *			(in) b					- right point (end time).
 *			(in) steps				- number of steps.
 *			(in) argv				- extra arguments are required by function_pointer.
 *
 * @return	Returns full result of integration (each step of integration).
 *
 ***********************************************************************************************/
std::vector<differential_result> * rk4(double (*function_pointer)(const double t, const double val, const std::vector<void *> & argv), double initial_value, const double a, const double b, const unsigned int steps, const std::vector<void *> & argv);

/***********************************************************************************************
 *
 * @brief   Runge-Kutta-Felhberg (RKF45) solver.
 *
 * @param   (in) function_pointer	- pointer to function.
 *          (in) initial_value		- initial values.
 *          (in) a					- left point (start time).
 *			(in) b					- right point (end time).
 *			(in) tolerance			- acceptable error for solving.
 *			(in) argv				- extra arguments are required by function_pointer.
 *
 * @return	Returns full result of integration (each step of integration).
 *
 ***********************************************************************************************/
std::vector<differential_result> * rkf45(double (*function_pointer)(const double t, const double val, const std::vector<void *> & argv), double initial_value, const double a, const double b, const double tolerance, const std::vector<void *> & argv);

#endif