#ifndef _PCNN_H_
#define _PCNN_H_

#include "network.h"

#include <vector>

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

	double OUTPUT_TRUE;
	double OUTPUT_FALSE;

	bool FAST_LINKING;

	pcnn_parameters() {
	    VF = 1.0;
	    VL = 1.0;
	    VT = 10.0;

	    AF = 0.1;
	    AL = 0.1;
	    AT = 0.5;

	    W = 1.0;
	    M = 1.0;

	    B = 0.1;

	    OUTPUT_TRUE = 1;
	    OUTPUT_FALSE = 0;

	    FAST_LINKING = False;
	}
};

class pcnn : public network {
protected:
	std::vector<double> * stimulus;
	std::vector<pcnn_oscillator> * oscillators;
	std::vector<std::vector<double> * > * dynamic;
	pcnn_parameters params;

public:

private:
};

#endif
