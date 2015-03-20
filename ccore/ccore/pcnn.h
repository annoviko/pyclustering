#ifndef _PCNN_H_
#define _PCNN_H_

#include "network.h"

#include <vector>

#define OUTPUT_ACTIVE_STATE			(double) 1.0
#define OUTPUT_INACTIVE_STATE		(double) 0.0

typedef struct pcnn_oscillator {
	double output;
	double feeding;
	double linking;
	double threshold;

	pcnn_oscillator() :
		output(0.0),
		feeding(0.0),
		linking(0.0),
		threshold(0.0) { }
} pcnn_oscillator;


typedef struct pcnn_parameters {
	double VF;
	double VL;
	double VT;

	double AF;
	double AL;
	double AT;

	double W;
	double M;

	double B;

	bool FAST_LINKING;

	pcnn_parameters(void) {
	    VF = 1.0;
	    VL = 1.0;
	    VT = 10.0;

	    AF = 0.1;
	    AL = 0.1;
	    AT = 0.5;

	    W = 1.0;
	    M = 1.0;

	    B = 0.1;

	    FAST_LINKING = false;
	}
} pcnn_parameters;


class pcnn;


class pcnn_dynamic {
	friend class pcnn;
private:
	std::vector<std::vector<double> > dynamic;

public:
	~pcnn_dynamic(void);

public:
	std::vector< std::vector<unsigned int> * > * allocate_sync_ensembles(void) const;

	std::vector< std::vector<unsigned int> * > * allocate_spike_ensembles(void) const;

	std::vector<unsigned int> * allocate_time_signal(void) const;	

	const std::vector<std::vector<double> > * const get_dynamic(void) const { return &dynamic; }

private:
	pcnn_dynamic(void);

	pcnn_dynamic(const unsigned int number_oscillators, const unsigned int simulation_steps);
};


class pcnn : public network {
protected:
	std::vector<pcnn_oscillator> oscillators;

	pcnn_parameters params;

public:
	pcnn(void);

	pcnn(const unsigned int num_osc, const conn_type connection_type, const pcnn_parameters & parameters);

	virtual ~pcnn(void);

public:
	pcnn_dynamic * simulate_static(const unsigned int steps, const std::vector<double> & stimulus);

private:
	void calculate_states(const std::vector<double> & stimulus);

	void store_dynamic(pcnn_dynamic * const dynamic, const unsigned int step);

	void fast_linking(const std::vector<double> & feeding, std::vector<double> & linking, std::vector<double> & output);
};

#endif
