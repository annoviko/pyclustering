#ifndef _SYNCPR_H_
#define _SYNCPR_H_

#include "sync.h"


typedef std::vector<std::vector<double> >   matrix;
typedef std::vector<int>                    pattern;


class syncpr: public sync_network {
protected:
    double m_increase_strength1;
    double m_increase_strength2;
    matrix m_coupling;

public:
    syncpr(const unsigned int num_osc, 
           const double increase_strength1, 
           const double increase_strength2);

    virtual ~syncpr(void);

public:
    void train(const std::vector<pattern> & patterns);

	void simulate_static(const unsigned int steps, 
		                 const double time, 
                         const pattern & input_pattern,
						 const solve_type solver, 
						 const bool collect_dynamic, 
						 sync_dynamic & output_dynamic);

	void simulate_dynamic(const pattern & input_pattern,
                          const double order, 
		                  const double step,
		                  const solve_type solver, 
						  const bool collect_dynamic,
						  sync_dynamic & output_dynamic);

    double memory_order(const pattern & input_pattern) const;

protected:
    virtual double phase_kuramoto(const double t, const double teta, const std::vector<void *> & argv);

};

#endif