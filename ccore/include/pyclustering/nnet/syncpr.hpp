/*!

@authors Andrei Novikov (pyclustering@yandex.ru)
@date 2014-2020
@copyright BSD-3-Clause

*/

#pragma once


#include <pyclustering/nnet/sync.hpp>


namespace pyclustering {

namespace nnet {


typedef std::vector<std::vector<double> >   matrix;
typedef std::vector<int>                    syncpr_pattern;


/* it is enough functionality in parent dynamic */
typedef sync_dynamic                        syncpr_dynamic;


class syncpr_invalid_pattern : public std::runtime_error {
public:
    syncpr_invalid_pattern();

    explicit syncpr_invalid_pattern(const std::string & description);
};


class syncpr: public sync_network {
private:
    using sync_network::simulate_static;
    using sync_network::simulate_dynamic;

protected:
    double m_increase_strength1;
    double m_increase_strength2;
    matrix m_coupling;

public:
    syncpr(const unsigned int num_osc, 
           const double increase_strength1, 
           const double increase_strength2);

    syncpr(const unsigned int num_osc,
           const size_t height,
           const size_t width,
           const double increase_strength1,
           const double increase_strength2);

    virtual ~syncpr() = default;

public:
    void train(const std::vector<syncpr_pattern> & patterns);

    void simulate_static(const unsigned int steps, 
                         const double time, 
                         const syncpr_pattern & input_pattern,
                         const solve_type solver, 
                         const bool collect_dynamic, 
                         syncpr_dynamic & output_dynamic);

    void simulate_dynamic(const syncpr_pattern & input_pattern,
                          const double order,
                          const double step,
                          const solve_type solver, 
                          const bool collect_dynamic,
                          syncpr_dynamic & output_dynamic);

    double memory_order(const syncpr_pattern & input_pattern) const;

protected:
    double phase_kuramoto(const double t, const double teta, const std::vector<void *> & argv) const override;

    void phase_kuramoto_equation(const double t, const differ_state<double> & inputs, const differ_extra<void *> & argv, differ_state<double> & outputs) const override;

private:
    void validate_pattern(const syncpr_pattern & sample) const;

    void initialize_phases(const syncpr_pattern & sample);

    double calculate_memory_order(const syncpr_pattern & input_pattern) const;
};


}

}