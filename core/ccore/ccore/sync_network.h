#ifndef _SYNC_NETWORK_H_
#define _SYNC_NETWORK_H_

#include "network.h"
#include "interface_ccore.h"

#include <vector>


typedef struct sync_oscillator {
	double phase;
	double frequency;
} sync_oscillator;


typedef struct sync_dynamic {
	double time;
	double phase;
} sync_dynamic;


class sync_network : public network {
protected:
	std::vector<sync_oscillator>	* oscillators;					/* oscillators						*/
	std::vector< std::vector<unsigned int> * > * sync_ensembles;	/* pointer to sync ensembles		*/

	double							weight;							/* multiplier for connections		*/
	unsigned int					cluster;						/* q parameter						*/	

public:
	sync_network(const unsigned int size, const double weight_factor, const double frequency_factor, const unsigned int qcluster, const conn_type connection_type, const initial_type initial_phases);
	
	virtual ~sync_network(void);

	double sync_order(void) const;

	double sync_local_order(void) const;

	std::vector< std::vector<unsigned int> * > * allocate_sync_ensembles(const double tolerance = 0.01);

	dynamic_result * simulate_static(const unsigned int steps, const double time, const solve_type solver, const bool collect_dynamic);

	dynamic_result * simulate_dynamic(const double order, const solve_type solver, const bool collect_dynamic, const double step = 0.1, const double step_int = 0.01, const double threshold_changes = 0.0000001);

	static double phase_normalization(const double teta);

protected:
	virtual double phase_kuramoto(const double t, const double teta, const std::vector<void *> & argv);

	virtual void calculate_phases(const solve_type solver, const double t, const double step, const double int_step);

private:
	static double adapter_phase_kuramoto(const double t, const double teta, const std::vector<void *> & argv);

	void free_sync_ensembles(void);

	void store_dynamic(std::vector< std::vector<sync_dynamic> * > * dynamic, const double time) const;

	dynamic_result * convert_dynamic_representation(std::vector< std::vector<sync_dynamic> * > * dynamic) const;
};

#endif