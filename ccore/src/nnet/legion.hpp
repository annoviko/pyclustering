/**
*
* Copyright (C) 2014-2016    Andrei Novikov (pyclustering@yandex.ru)
*
* GNU_PUBLIC_LICENSE
*   pyclustering is free software: you can redistribute it and/or modify
*   it under the terms of the GNU General Public License as published by
*   the Free Software Foundation, either version 3 of the License, or
*   (at your option) any later version.
*
*   pyclustering is distributed in the hope that it will be useful,
*   but WITHOUT ANY WARRANTY; without even the implied warranty of
*   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
*   GNU General Public License for more details.
*
*   You should have received a copy of the GNU General Public License
*   along with this program.  If not, see <http://www.gnu.org/licenses/>.
*
*/

#ifndef _LEGION_NETWORK_H_
#define _LEGION_NETWORK_H_


#include <vector>
#include <random>

#include "differential/runge_kutta_4.hpp"
#include "differential/runge_kutta_fehlberg_45.hpp"

#include "container/adjacency.hpp"
#include "container/adjacency_connector.hpp"
#include "container/dynamic_data.hpp"
#include "container/ensemble_data.hpp"

#include "nnet/network.hpp"


using namespace container;
using namespace differential;


typedef std::vector<unsigned int>		legion_ensemble;
typedef std::vector<double>				legion_stimulus;


typedef struct legion_network_state {
public:
	std::vector<double> m_output;
	double				m_inhibitor;
	double				m_time;

public:
	legion_network_state(void) : m_inhibitor(0.0), m_time(0.0) { }

	legion_network_state(const unsigned int size) : m_output(size, 0.0), m_inhibitor(0.0), m_time(0.0) { }

public:
	inline size_t size(void) const { return m_output.size(); }

	inline legion_network_state & operator=(const legion_network_state & other) {
		if (this != &other) {
			m_output.resize(other.size());
			std::copy(other.m_output.cbegin(), other.m_output.cend(), m_output.begin());

			m_inhibitor = other.m_inhibitor;
			m_time = other.m_time;
		}

		return *this;
	}
} legion_network_state;


class legion_dynamic : public dynamic_data<legion_network_state> {
public:
	legion_dynamic(void) { }

	~legion_dynamic(void) { }

public:
	void allocate_sync_ensembles(const double amplitude, ensemble_data<legion_ensemble> & sync_ensembles) const;

	void allocate_spike_ensembles(const double amplitude, ensemble_data<legion_ensemble> & spike_ensembles) const;
};


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

	bool ENABLE_POTENTIAL = true;
} legion_parameters;


typedef struct legion_oscillator {
	double m_excitatory;
	double m_inhibitory;
	double m_potential;
	double m_coupling_term;
	double m_buffer_coupling_term;
	double m_noise;

	legion_oscillator(void) : 
		m_excitatory(0.0),
		m_inhibitory(0.0),
		m_potential(0.0),
		m_coupling_term(0.0),
		m_buffer_coupling_term(0.0),
		m_noise(0.0) { }
} legion_oscillator;


class legion_network {
private:
	std::vector<legion_oscillator> m_oscillators;

	double m_global_inhibitor;

	legion_parameters m_params;

    std::shared_ptr<adjacency_collection> m_static_connections;

	std::vector<std::vector<double> > m_dynamic_connections;

	legion_stimulus * m_stimulus;		/* just keep it during simulation for convinience (pointer to external object, legion is not owner) */

	std::random_device                      m_device;

	std::default_random_engine              m_generator;

	std::uniform_real_distribution<double>	m_noise_distribution;


private:
    const static size_t MAXIMUM_MATRIX_REPRESENTATION_SIZE;


public:
    legion_network(void);

	legion_network(const size_t num_osc, 
        const connection_t connection_type,
        const legion_parameters & params);

    legion_network(const size_t num_osc,
        const connection_t connection_type,
        const size_t height,
        const size_t width,
        const legion_parameters & params);

	virtual ~legion_network(void);


public:
	void simulate(const unsigned int steps, const double time, const solve_type solver, const bool collect_dynamic, const legion_stimulus & stimulus, legion_dynamic & output_dynamic);

    inline size_t size(void) const { return m_oscillators.size(); }


private:
	void create_dynamic_connections(const legion_stimulus & stimulus);

	void calculate_states(const legion_stimulus & stimulus, const solve_type solver, const double t, const double step, const double int_step);

	void inhibitor_state(const double t, const differ_state<double> & inputs, const differ_extra<void *> & argv, differ_state<double> & outputs);

	static void adapter_inhibitor_state(const double t, const differ_state<double> & inputs, const differ_extra<void *> & argv, differ_state<double> & outputs);

	void neuron_states(const double t, const differ_state<double> & inputs, const differ_extra<void *> & argv, differ_state<double> & outputs);

	void neuron_simplify_states(const double t, const differ_state<double> & inputs, const differ_extra<void *> & argv, differ_state<double> & outputs);

	static void adapter_neuron_states(const double t, const differ_state<double> & inputs, const differ_extra<void *> & argv, differ_state<double> & outputs);

	static void adapter_neuron_simplify_states(const double t, const differ_state<double> & inputs, const differ_extra<void *> & argv, differ_state<double> & outputs);

	void store_dynamic(const double time, const bool collect_dynamic, legion_dynamic & dynamic);

    void initialize(const size_t num_osc,
        const connection_t connection_type,
        const size_t height,
        const size_t width,
        const legion_parameters & params);
};

#endif
