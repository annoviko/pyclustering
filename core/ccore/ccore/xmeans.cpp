#if 0
#include "xmeans.h"

xmeans::xmeans(const std::vector<std::vector<double> > * const data, const std::vector<std::vector<double> > * const initial_centers, const unsigned int kmax, const double minimum_change) {
#ifdef FAST_SOLUTION
	tolerance = minimum_change * minimum_change;
#else
	tolerance = minimum_change;
#endif
	
	dataset = (std::vector<std::vector<double> > * const) data;

	centers = new std::vector<std::vector<double> >( (*initial_centers) );

	clusters = new std::vector<std::vector<unsigned int> * >();
	for (unsigned int index = 0; index < centers->size(); index++) {
		clusters->push_back(new std::vector<unsigned int>());
	}
}

xmeans::~xmeans(void) {
	if (centers != NULL) {
		delete centers;
		centers = NULL;
	}

	if (clusters != NULL) {
		for (std::vector<std::vector<unsigned int> * >::const_iterator iter = clusters->begin(); iter != clusters->end(); iter++) {
			delete (*iter);
		}

		delete clusters;
		clusters = NULL;
	}
}

void xmeans::process(void) {
	unsigned int current_number_clusters = clusters->size();

	while (current_number_clusters < maximum_clusters) {
		improve_parameters();
		improve_structure();

		if (current_number_clusters == clusters->size()) {
			break;
		}

		current_number_clusters = clusters->size();
	}
}

void xmeans::improve_parameters(const std::vector<std::vector<unsigned int> > * const available_indexes) {
	double current_change = std::numeric_limits<double>::max();

	while(current_change > tolerance) {
		update_clusters(available_indexes);
		current_change = update_centers();
	}
}


void xmeans::improve_structure() {
	const double difference = 0.001;
	std::vector<std::vector<double> > * allocated_centers = new std::vector<std::vector<double> >();

	for (unsigned int index = 0; index < clusters->size(); index++) {
		std::vector<std::vector<double> > parent_child_centers;
	}
}
#endif