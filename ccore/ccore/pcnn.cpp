#include "pcnn.h"

pcnn::pcnn(const unsigned int size, std::vector<double> * oscillator_stimulus, const pcnn_parameters * parameters, const conn_type connection_type) :
	network(size, connection_type)
{
	stimulus = oscillator_stimulus;

	oscillators = new std::vector<pcnn_oscillator>(size);

	params = parameters;
}

pcnn::~pcnn() {
	if (oscillators != NULL) {
		delete oscillators;
	}
}

std::vector< std::vector<sync_dynamic> * > * pcnn::simulate_static(const unsigned int steps, const bool collect_dynamic) {
	dynamic = new std::vector< std::vector<double> >(steps);


}
