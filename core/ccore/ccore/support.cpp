#include "support.h"

namespace butcher_table {
    const double a2 = 1.0/4.0,		b2 = 1.0/4.0;
    const double a3 = 3.0/8.0,		b3 = 3.0/32.0,			c3 = 9.0/32.0; 
    const double a4 = 12.0/13.0,	b4 = 1932.0/2197.0,		c4 = -7200.0/2197.0,    d4 = 7296.0/2197.0; 
    const double a5 = 1.0,			b5 = 439.0/216.0,		c5 = -8.0,				d5 = 3680.0/513.0,		e5 = -845.0/4104.0; 
    const double a6 = 1.0/2.0,		b6 = -8.0/27.0,			c6 = 2.0,				d6 = -3544.0/2565.0,	e6 = 1859.0/4104.0,		f6 = -11.0/40.0;   
    const double n1 = 25.0/216.0,	n3 = 1408.0/2565.0,		n4 = 2197.0/4104.0,		n5 = -1.0/5.0;
    
    /* Coef. for error that are defined from equation (y[k + 1] - z[k + 1]). It reduces time for solving value of Runge-Kutta 5. */
    const double r1 = 1.0/360.0,	r3 = -128.0/4275.0,		r4 = -2197.0/75240.0,	r5 = 1.0/50.0,			r6 = 2.0/55.0;  
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
std::vector<std::vector<double> > * read_sample(const char * const path_file) {
	std::string filename(path_file);

	std::ifstream file_stream(filename.c_str(), std::fstream::in);
	if (!file_stream.is_open()) {
		return NULL;
	}

	std::string line;

	std::vector<std::vector<double> > * dataset = new std::vector<std::vector<double> >();

	while(std::getline(file_stream, line)) {
		std::istringstream parser(line);
		std::vector<double> point;

		double coordinate = 0.0;
		while(parser >> coordinate) {
			point.push_back(coordinate);
		}

		dataset->push_back(point);
	}

	file_stream.close();

	return dataset;
}

/***********************************************************************************************
 *
 * @brief   Converts representation of data from CCORE standard to internal.
 *
 * @param   (in) sample     - input data (sample) for converting.
 *
 * @return  Returns internal type of representation of input data.
 *
 ***********************************************************************************************/
std::vector<std::vector<double> > * read_sample(const data_representation * const sample) {
	std::vector<std::vector<double> > * dataset = new std::vector<std::vector<double> >();

	for (unsigned int index = 0; index < sample->size; index++) {
		std::vector<double> point;
		for (unsigned int dimension = 0; dimension < sample->dimension; dimension++) {
			point.push_back(sample->objects[index][dimension]);
		}

		dataset->push_back(point);
	}

	return dataset;
}

/***********************************************************************************************
 *
 * @brief   Converts representation of cluster to standard type of CCORE interface.
 *
 * @param   (in) clusters   - input clusters for converting.
 *
 * @return  Returns standard type of representation of clusters.
 *
 ***********************************************************************************************/
clustering_result * create_clustering_result(const std::vector<std::vector<unsigned int> *> * const clusters) {
	clustering_result * result = new clustering_result();

	if (clusters == NULL) {
		result->size = 0;
		result->clusters = NULL;
	}
	else {
		result->size = clusters->size();
		result->clusters = new cluster_representation[result->size];
	}

	for (unsigned int index_cluster = 0; index_cluster < result->size; index_cluster++) {
		result->clusters[index_cluster].size = (*clusters)[index_cluster]->size();
		if (result->clusters[index_cluster].size > 0) {
			result->clusters[index_cluster].objects = new unsigned int[result->clusters[index_cluster].size];

			for (unsigned int index_object = 0; index_object < result->clusters[index_cluster].size; index_object++) {
				result->clusters[index_cluster].objects[index_object] = (*(*clusters)[index_cluster])[index_object];
			}
		}
		else {
			result->clusters[index_cluster].objects = NULL;
		}
	}

	return result;
}

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
std::vector<differential_result> * rk4(double (*function_pointer)(const double t, const double val, const std::vector<void *> & argv), double initial_value, const double a, const double b, const unsigned int steps, const std::vector<void *> & argv) {
	const double step = (b - a) / (double) steps;

	differential_result current_result;
	current_result.time = 0.0;
	current_result.value = initial_value;

	std::vector<differential_result> * result = new std::vector<differential_result>();
	result->push_back(current_result);

	for (unsigned int i = 0; i < steps; i++) {
		double k1 = step * function_pointer(current_result.time, current_result.value, argv);
		double k2 = step * function_pointer(current_result.time + step / 2.0, current_result.value + k1 / 2.0, argv);
		double k3 = step * function_pointer(current_result.time + step / 2.0, current_result.value + k2 / 2.0, argv);
		double k4 = step * function_pointer(current_result.time + step, current_result.value + k3, argv);

		current_result.value += (k1 + 2.0 * k2 + 2.0 * k3 + k4) / 6.0;
		current_result.time += step;

		result->push_back(current_result);
	}

	return result;
}

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
std::vector<differential_result> * rkf45(double (*function_pointer)(const double t, const double val, const std::vector<void *> & argv), double initial_value, const double a, const double b, const double tolerance, const std::vector<void *> & argv) {
	differential_result current_result;
	current_result.time = a;
	current_result.value = initial_value;

	std::vector<differential_result> * result = new std::vector<differential_result>();
	result->push_back(current_result);

	double h = (b - a) / 10.0;
	const double hmin = h / 100.0;
	const double hmax = 100.0 * h;

	const double br = b - 0.00001 * (double) std::abs(b);

	const unsigned int iteration_limit = 250;

	while (current_result.time < b) {
		const double current_time = current_result.time;
		const double current_value = current_result.value;

		if ( (current_time + h) > br ) {
			h = b - current_result.time;
		}

		double k1 = h * function_pointer(current_time, current_value, argv);
		double y2 = current_value + butcher_table::b2 * k1;

		double k2 = h * function_pointer(current_time + butcher_table::a2 * h, y2, argv);
		double y3 = current_value + butcher_table::b3 * k1 + butcher_table::c3 * k2;

		double k3 = h * function_pointer(current_time + butcher_table::a3 * h, y3, argv);
        double y4 = current_value + butcher_table::b4 * k1 + butcher_table::c4 * k2 + butcher_table::d4 * k3;

		double k4 = h * function_pointer(current_time + butcher_table::a4 * h, y4, argv);
        double y5 = current_value + butcher_table::b5 * k1 + butcher_table::c5 * k2 + butcher_table::d5 * k3 + butcher_table::e5 * k4;

		double k5 = h * function_pointer(current_time + butcher_table::a5 * h, y5, argv);
        double y6 = current_value + butcher_table::b6 * k1 + butcher_table::c6 * k2 + butcher_table::d6 * k3 + butcher_table::e6 * k4 + butcher_table::f6 * k5;

		double k6 = h * function_pointer(current_time + butcher_table::a6 * h, y6, argv);

		/* Calculate error (difference between Runge-Kutta 4 and Runge-Kutta 5) and new value. */
		double err = std::abs(butcher_table::r1 * k1 + butcher_table::r3 * k3 + butcher_table::r4 * k4 + butcher_table::r5 * k5 + butcher_table::r6 * k6);

		/* Calculate new value. */
		double ynew = current_value + butcher_table::n1 * k1 + butcher_table::n3 * k3 + butcher_table::n4 * k4 + butcher_table::n5 * k5;

		if ( (err < tolerance) || (h < 2.0 * hmin) ) {
			current_result.value = ynew;

			if (current_time + h > br) {
				current_result.time = b;
			}
			else {
				current_result.time = current_time + h;
			}

			result->push_back(current_result);
		}

		double s = 0.0;
		if (err != 0.0) {
			s = 0.84 * std::pow( (tolerance * h / err), 0.25 );
		}

		if ( (s < 0.75) && (h > 2.0 * hmin) ) {
			h = h / 2.0;
		}

		if ( (s > 1.5) && (h * 2.0 < hmax) ) {
			h = 2.0 * h;
		}

		if (iteration_limit == result->size()) {
			break;
		}
	}

	return result;
}