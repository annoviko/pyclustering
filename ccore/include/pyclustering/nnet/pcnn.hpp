/*!

@authors Andrei Novikov (pyclustering@yandex.ru)
@date 2014-2020
@copyright BSD-3-Clause

*/

#pragma once


#include <vector>

#include <pyclustering/container/adjacency.hpp>
#include <pyclustering/container/adjacency_connector.hpp>
#include <pyclustering/container/dynamic_data.hpp>
#include <pyclustering/container/ensemble_data.hpp>

#include <pyclustering/nnet/network.hpp>


using namespace pyclustering::container;


namespace pyclustering {

namespace nnet {


#define OUTPUT_ACTIVE_STATE       (double) 1.0
#define OUTPUT_INACTIVE_STATE     (double) 0.0

struct pcnn_oscillator {
    double output;
    double feeding;
    double linking;
    double threshold;

    pcnn_oscillator() :
        output(0.0),
        feeding(0.0),
        linking(0.0),
        threshold(0.0) { }
};


struct pcnn_parameters {
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
};


using pcnn_ensemble = std::vector<std::size_t>;
using pcnn_stimulus = std::vector<double>;
using pcnn_time_signal = std::vector<std::size_t>;


struct pcnn_network_state {
public:
    std::vector<double> m_output;
    double              m_time;

public: 
    std::size_t size() const;
};


class pcnn_dynamic : public dynamic_data<pcnn_network_state> {
public:
    pcnn_dynamic();

    ~pcnn_dynamic();

public:
    void allocate_sync_ensembles(ensemble_data<pcnn_ensemble> & sync_ensembles) const;

    void allocate_spike_ensembles(ensemble_data<pcnn_ensemble> & spike_ensembles) const;

    void allocate_time_signal(pcnn_time_signal & time_signal) const;

public:
    /**
     *
     * @brief   Returns dynamic state of oscillator of the pulse-coupled neural network at the
     *          specified iteration step.
     *
     * @param[in] iteration: number of iteration at which oscillator state is required.
     * @param[in] index_oscillator: index of oscillator whose state is required.
     *
     * @return dynamic state of the oscillator at the specified iteration.
     *
     */
    inline double dynamic_oscillator_at(const size_t iteration, const size_t index_oscillator) const { 
        return at(iteration).m_output[index_oscillator]; 
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
    pcnn();

    pcnn(const size_t p_size, const connection_t p_structure, const pcnn_parameters & p_parameters);

    pcnn(const size_t p_size,
         const connection_t p_structure,
         const size_t p_height,
         const size_t p_width,
         const pcnn_parameters & p_parameters);

    virtual ~pcnn() = default;


public:
    void simulate(const std::size_t steps, const pcnn_stimulus & stimulus, pcnn_dynamic & output_dynamic);

    inline size_t size() const { return m_oscillators.size(); }


private:
    void initilize(const size_t p_size,
      const connection_t p_structure,
      const size_t p_height,
      const size_t p_width,
      const pcnn_parameters & p_parameters);

  void calculate_states(const pcnn_stimulus & stimulus);

  void store_dynamic(const std::size_t step, pcnn_dynamic & dynamic) const;

  void fast_linking(const std::vector<double> & feeding, std::vector<double> & linking, std::vector<double> & output);
};


}

}