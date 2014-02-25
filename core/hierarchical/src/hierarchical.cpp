#include <stddef.h>

#include <cmath>
#include <vector>
#include <list>
#include <algorithm>

#include <fstream>
#include <sstream>
#include <iostream>

#include <string>

using std::vector;
using std::list;

#if 1
	#define	FAST_SOLUTION
#endif

typedef vector<vector<double> >  	matrix;

inline double euclidean_distance_sqrt(const vector<double> * const point1, const vector<double> * const point2) {
	double distance = 0.0;
	/* assert(point1->size() != point1->size()); */
	for (unsigned int dimension = 0; dimension < point1->size(); dimension++) {
		double difference = (point1->data()[dimension] - point2->data()[dimension]);
		distance += difference * difference;
	}

	return distance;
}

inline double euclidean_distance(const vector<double> * const point1, const vector<double> * const point2) {
	double distance = 0.0;
	/* assert(point1->size() != point1->size()); */
	for (unsigned int dimension = 0; dimension < point1->size(); dimension++) {
		double difference = (point1->data()[dimension] - point2->data()[dimension]);
		distance += difference * difference;
	}

	return std::sqrt(distance);
}


class cluster {
private:
	matrix * 			dataset;	/* pointer to input data set */
	vector<int> * 		indexes; 	/* indexes of objects in input data set */
	vector<double> *  	center; 	/* center of the cluster */

public:
	cluster(const matrix * const data, const int index, const vector<double> * const point) {
		dataset = (matrix *) data;
		center = new vector<double>(*point);
		indexes = new vector<int>(1, index);
	}

	~cluster(void) {
		dataset = NULL;

		if (center != NULL) {
			delete center; center = NULL;
		}

		if (indexes != NULL) {
			delete indexes; indexes = NULL;
		}
	}

	void append(const cluster * cluster2) {
		indexes->insert(indexes->end(), cluster2->get_indexes()->begin(), cluster2->get_indexes()->end());

		/* update center */
		for (unsigned int dimension = 0; dimension < center->size(); dimension++) {
			(*center)[dimension] = 0.0;
			for (vector<int>::const_iterator iter = indexes->begin(); iter != indexes->end(); iter++) {
				(*center)[dimension] += (*dataset)[*iter][dimension];
			}

			(*center)[dimension] /= indexes->size();
		}
	}

	inline const vector<double> * const get_center(void) const {
		return center;
	}

	inline const vector<int> * const get_indexes(void) const {
		return indexes;
	}

	inline cluster & operator=(const cluster & object) {
		dataset = object.dataset;

		delete center; delete indexes;

		center = new vector<double>(object.center->size());
		indexes = new vector<int>(object.indexes->size());

		std::copy(object.center->begin(), object.center->end(), center->begin());
		std::copy(object.indexes->begin(), object.indexes->end(), indexes->begin());

		return *this;
	}
};

class hierarchical {
private:
	list<cluster *> *  	clusters;
	matrix *  			data;
	unsigned int 		number_clusters;

public:
	hierarchical(const matrix * const dataset, unsigned int cluster_number) {
		data = (matrix *) dataset;
		clusters = new list<cluster *>();

		number_clusters = cluster_number;

		for (unsigned int index = 0; index < dataset->size(); index++) {
			cluster * data_cluster = new cluster(dataset, index, &(dataset->data()[index]));
			clusters->push_back(data_cluster);
		}
	}

	~hierarchical() {
		data = NULL;

		if (clusters != NULL) {
			for (list<cluster *>::const_iterator iter = clusters->begin(); iter != clusters->end(); iter++) {
				delete (*iter);
			}

			delete clusters;
			clusters = NULL;
		}
	}

	const list<cluster *> * const process(void) {
		while(clusters->size() > number_clusters) {
			merge_nearest_clusters();
		}

		return clusters;
	}

private:
	void merge_nearest_clusters(void) {
		double minimum_distance = INFINITY;
		list<cluster *>::iterator candidate1, candidate2;

		for(list<cluster *>::iterator iter1 = clusters->begin(); iter1 != clusters->end(); iter1++) {
			list<cluster *>::iterator iter2 = iter1;
			for(++iter2; iter2 != clusters->end(); iter2++) {
#ifndef FAST_SOLUTION
				double distance = euclidean_distance((*iter1)->get_center(), (*iter2)->get_center());
#else
				double distance = euclidean_distance_sqrt((*iter1)->get_center(), (*iter2)->get_center());
#endif
				if (distance < minimum_distance) {
					candidate1 = iter1;
					candidate2 = iter2;
					minimum_distance = distance;
				}
			}
		}

		((cluster *) (*candidate1))->append(*candidate2);
		clusters->erase(candidate2);
	}
};


int main(int argc, char * argv[]) {
	std::string filename;
	unsigned int number_cluster = 0;

	for (unsigned int iter = 1; iter < (unsigned int) argc; iter++) {
		std::istringstream argument(argv[iter]);

		switch(iter) {
			case 1: argument >> filename; break;
			case 2: argument >> number_cluster; break;
			default: break;
		}
	}

	std::ifstream file_stream(filename.c_str(), std::fstream::in);
	if (!file_stream.is_open()) {
		std::cout << "Impossible to open file '" << filename.c_str() << "'" << std::endl;
		return 1;
	}

	std::string line;

	matrix * dataset = new matrix();

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

	hierarchical * solver = new hierarchical(dataset, number_cluster);
	const list<cluster *> * clusters = solver->process();

	for (list<cluster *>::const_iterator cluster_iterator = clusters->begin(); cluster_iterator != clusters->end(); cluster_iterator++) {
		std::cout << "[ ";
		for (vector<int>::const_iterator index_iterator = (*cluster_iterator)->get_indexes()->begin(); index_iterator != (*cluster_iterator)->get_indexes()->end(); index_iterator++) {
			std::cout << (*index_iterator) << " ";
		}
		std::cout << "]" << std::endl;
	}

	delete solver; solver = NULL;
	delete dataset; dataset = NULL;

	return 0;
}
