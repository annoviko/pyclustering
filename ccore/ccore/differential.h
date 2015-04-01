#ifndef _DIFFERENTIAL_H_
#define _DIFFERENTIAL_H_

#include <vector>

namespace differential {

template <typename state_type>
class differ_state {
public:
	typedef state_type							value_type	;
	typedef std::vector<value_type>				differ_variables;

	typedef typename differ_variables::iterator			iterator;
	typedef typename differ_variables::const_iterator	const_iterator;
	typedef typename differ_variables::reverse_iterator	reverse_iterator;

public:
	differ_state(void) : variable_state(new std::vector<state_type>());
	differ_state(const size_t size) : variable_state(new std::vector<state_type>(size));
	differ_state(const size_t size, const state_type value) : variable_state(new std::vector<state_type>(size, value));
	differ_state(const differ_state & instance) {
		variable_state->resize(instance.size());
		/* std copy here */
	}

	~differ_state(void) { delete variable_state; }

public:


private:
	differ_variables * variable_state;
};

// template <typename state_type> using differ_state = std::vector<state_type>;
template <typename extra_type> using differ_extra = std::vector<extra_type>;

template <typename state_type> struct differ_output {
	double                    time;
	differ_state<state_type>  state;
};

template <typename state_type> using differ_result = std::vector<state_type>;


template <typename state_type, typename extra_type = void *> 
void runge_kutta_4(void (*function_pointer)(const double t, const differ_state<state_type> & inputs, const differ_extra<extra_type> & argv, differ_state<state_type> & outputs),
                   const differ_state<input_type> &		inputs,
                   const double							time_start,
                   const double							time_end,
                   const unsigned int					steps,
                   const bool							flag_collect,
                   const differ_extra<extra_type> &		argv,
                   differ_result<state_type> &			outputs) {

	const double step = (time_end - time_start) / (double) steps;
	
	if (flag_collect) {
		outputs.resize(steps);
	}
	else {
		outputs.resize(1);
	}

	differ_result<state_type> current_result;
	current_result.time = time_start;
	current_result.state = inputs;

	for (unsigned int i = 0; i < steps; i++) {
		double k1 = step * function_pointer(current_result.time, current_result.value, argv);
		double k2 = step * function_pointer(current_result.time + step / 2.0, current_result.value + k1 / 2.0, argv);
		double k3 = step * function_pointer(current_result.time + step / 2.0, current_result.value + k2 / 2.0, argv);
		double k4 = step * function_pointer(current_result.time + step, current_result.value + k3, argv);

		current_result.value += (k1 + 2.0 * k2 + 2.0 * k3 + k4) / 6.0;
		current_result.time += step;

		if (flag_collect) {
			(*result)[i] = current_result;
		}
		else {
			(*result)[0] = current_result;
		}
	}

	return result;

}

template <typename input_type>
void runge_kutta_fehlberg_45(void);

}

#endif