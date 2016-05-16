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

#ifndef _PCNN_H_
#define _PCNN_H_

#include <vector>

#include "container/adjacency.hpp"
#include "container/adjacency_connector.hpp"
#include "container/dynamic_data.hpp"
#include "container/ensemble_data.hpp"

#include "nnet/network.hpp"


using namespace container;


#define OUTPUT_ACTIVE_STATE			(double) 1.0
#define OUTPUT_INACTIVE_STATE		(double) 0.0

typedef struct pcnn_oscillator {
	double output;
	double feeding;
	double linking;
	double threshold;

	pcnn_oscillator(void) :
		output(0.0),
		feeding(0.0),
		linking(0.0),
		threshold(0.0) { }
} pcnn_oscillator;


typedef struct pcnn_parameters {
	double VF = 1.0;
	double VL = 1.0;
	double VT = 10.0;

	double AF = 0.1;
	double AL = 0.1;
	double AT = 0.5;

	double W = 1.0;
	double M = 1.0;

	double B = 0.1;

	bool FAST_LINKING = false;
} pcnn_parameters;


typedef std::vector<unsigned int>		pcnn_ensemble;
typedef std::vector<double>				pcnn_stimulus;
typedef std::vector<unsigned int>		pcnn_time_signal;

typedef struct pcnn_network_state {
public:
	std::vector<double> m_output;

	double				m_time;

public:
	inline size_t size(void) const { return m_output.size(); }

	inline pcnn_network_state & operator=(const pcnn_network_state & other) {
		if (this != &other) {
			m_output.resize(other.size());
			std::copy(other.m_output.cbegin(), other.m_output.cend(), m_output.begin());

			m_time = other.m_time;
		}

		return *this;
	}

} pcnn_network_state;


class pcnn_dynamic : public dynamic_data<pcnn_network_state> {
public:
	pcnn_dynamic(void);

	pcnn_dynamic(const unsigned int number_oscillators, const unsigned int simulation_steps);

	~pcnn_dynamic(void);

public:
	void allocate_sync_ensembles(ensemble_data<pcnn_ensemble> & sync_ensembles) const;

	void allocate_spike_ensembles(ensemble_data<pcnn_ensemble> & spike_ensembles) const;

	void allocate_time_signal(pcnn_time_signal & time_signal) const;

public:
    /***********************************************************************************************
    *
    * @brief   Returns dynamic state of oscillator of the pulse-coupled neural network at the
    *          specified iteration step.
    *
    * @param[in] iteration: number of iteration at which oscillator state is required.
    * @param[in] index_oscillator: index of oscillator whose state is required.
    *
    * @return dynamic state of the oscillator at the specified iteration.
    *
    ***********************************************************************************************/
    inline double dynamic_oscillator_at(const size_t iteration, const size_t index_oscillator) const { 
        return dynamic_at(iteration).m_output[index_oscillator]; 
    }
};


class pcnn {
protected:
	std::vector<pcnn_oscillator> m_oscillators;

	std::shared_ptr<adjacency_collection> m_connection;

	pcnn_parameters m_params;


private:
	const static size_t MAXIMUM_MATRIX_REPRESENTATION_SIZE;


public:
	pcnn(void);

	pcnn(const size_t p_size, const connection_t p_structure, const pcnn_parameters & p_parameters);

    pcnn(const size_t num_osc, 
         const connection_t connection_type,
         const size_t height,
         const size_t width,
         const pcnn_parameters & parameters);

	virtual ~pcnn(void);


public:
	void simulate(const unsigned int steps, const pcnn_stimulus & stimulus, pcnn_dynamic & output_dynamic);

	inline size_t size(void) const { return m_oscillators.size(); }


private:
	void initilize(const size_t p_size,
		const connection_t p_structure,
		const size_t p_height,
		const size_t p_width,
		const pcnn_parameters & p_parameters);

	void calculate_states(const pcnn_stimulus & stimulus);

	void store_dynamic(const unsigned int step, pcnn_dynamic & dynamic);

	void fast_linking(const std::vector<double> & feeding, std::vector<double> & linking, std::vector<double> & output);
};

#endif
