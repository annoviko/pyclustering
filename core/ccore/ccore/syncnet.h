#ifndef _SYNCNET_H_
#define _SYNCNET_H_

#include <vector>

#include "sync_network.h"

class syncnet: public sync_network {
private:
	std::vector<std::vector<double> >	* oscillator_locations;
	double								connection_weight;

public:
	syncnet(std::vector<std::vector<double> > * input_data, const double connectivity_radius, const initial_type initial_phases);

	virtual ~syncnet(void);

	dynamic_result * process(const double order, const solve_type solver, const bool collect_dynamic);

	virtual double phase_kuramoto(const double t, const double teta, const std::vector<void *> & argv);

private:
	static double adapter_phase_kuramoto(const double t, const double teta, const std::vector<void *> & argv);

	void create_connections(const double connectivity_radius);
};

#endif