#ifndef _LEGION_NETWORK_H_
#define _LEGION_NETWORK_H_

#include "network.h"
#include "interface_ccore.h"

#include <vector>

typedef struct legion_dynamic {
	double time;
	double value;
} legion_dynamic;

typedef struct legion_parameters {
	double eps		= 0.02;
	double alpha	= 0.005;
	double gamma	= 6.0;
	double betta	= 0.1;
	double lamda	= 0.1;
	double teta		= 0.9;
	double teta_x	= -1.5;
	double teta_p	= 1.5;
	double teta_xz	= 0.1;
	double teta_zx	= 0.1;
	double T		= 2.0;
	double mu		= 0.01;
	double Wz		= 1.5;
	double Wt		= 8.0;
	double fi		= 3.0;
	double ro		= 0.02;
	double I		= 0.2;
} legion_parameters;

typedef struct legion_oscillator {
	double excitatory;
	double inhibitory;
	double potential;
	double stimulus;
	double coupling_term;
	double buffer_coupling_term;
	double noise;
} legion_oscillator;

class legion_network : public network {
protected:
	std::vector<legion_oscillator> * oscillators;
	legion_parameters params;

	std::vector< std::vector<unsigned int> * > * sync_ensembles;    /* pointer to sync ensembles    */

public:
	legion_network(const unsigned int num_osc, const std::vector<double> * stimulus, const legion_parameters * params, const conn_type connection_type);

	virtual ~legion_network(void);

    /***********************************************************************************************
	 *
	 * @brief   Performs static simulation of LEGION.
	 *
	 * @param   (in) steps             - number steps of simulations during simulation.
	 * @param   (in) time              - time of simulation.
	 * @param   (in) solver            - type of solver for simulation.
	 * @param   (in) collect_dynamic   - if true - returns whole dynamic of oscillatory network, 
	 *                                   otherwise returns only last values of dynamics.
	 *
	 * @return  Returns dynamic of oscillatory network. If argument 'collect_dynamic' = true, than it 
	 *          returns dynamic for the whole simulation time, otherwise returns only last values 
	 *          (last step of simulation) of dynamic. The last value is always value of global
	 *			inhibitory.
	 *
	 ***********************************************************************************************/
	std::vector< std::vector<legion_dynamic> * > * simulate_static(const unsigned int steps, const double time, const solve_type solver, const bool collect_dynamic);
};

#endif