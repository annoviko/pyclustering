#ifndef _DIFFERENTIAL_H_
#define _DIFFERENTIAL_H_

#include <vector>
#include <initializer_list>
#include <cmath>

namespace differential {

namespace factor {

#define A2		(double) 1.0 / 4.0
#define B2		(double) 1.0 / 4.0

#define A3		(double) 3.0 / 8.0
#define B3		(double) 3.0 / 32.0
#define C3      (double) 9.0 / 32.0

#define A4		(double) 12.0 / 13.0
#define B4		(double) 1932.0 / 2197.0
#define C4		(double) -7200.0 / 2197.0
#define D4		(double) 7296.0 / 2197.0

#define A5		(double) 1.0
#define B5		(double) 439.0 / 216.0
#define C5		(double) -8.0
#define D5		(double) 3680.0 / 513.0
#define E5		(double) -845.0 / 4104.0

#define A6		(double) 1.0 / 2.0
#define B6		(double) -8.0 / 27.0
#define C6		(double) 2.0
#define D6		(double) -3544.0 / 2565.0
#define E6		(double) 1859.0 / 4104.0
#define F6		(double) -11.0 / 40.0

#define N1		(double) 25.0 / 216.0
#define N3		(double) 1408.0 / 2565.0
#define N4		(double) 2197.0 / 4104.0
#define N5		(double) -1.0 / 5.0

#define R1		(double) 1.0 / 360.0
#define R3		(double) -128.0 / 4275.0
#define R4		(double) -2197.0 / 75240.0
#define R5		(double) 1.0 / 50.0
#define R6		(double) 2.0 / 55.0

}

template <typename state_type>
class differ_state {
public:
	typedef state_type							value_type;
	typedef std::vector<value_type>				differ_variables;

	typedef typename differ_variables::iterator					iterator;
	typedef typename differ_variables::const_iterator			const_iterator;
	typedef typename differ_variables::reverse_iterator			reverse_iterator;
	typedef typename differ_variables::const_reverse_iterator	const_reverse_iterator;

public:
	differ_state(void) : m_variable_state(new std::vector<state_type>()) { }

	differ_state(const size_t size) : m_variable_state(new std::vector<state_type>(size)) { }

	differ_state(const size_t size, const state_type value) : m_variable_state(new std::vector<state_type>(size, value)) { }

	differ_state(const std::initializer_list<state_type> & value) : m_variable_state(new std::vector<state_type>(value)) { }

	differ_state(const differ_state & instance) {
		m_variable_state = new std::vector<state_type>(instance.size());
		std::copy(instance.cbegin(), instance.cend(), m_variable_state->begin());
	}

	~differ_state(void) { delete m_variable_state; }

public:
	inline void insert(iterator position, const value_type & value) { 
		m_variable_state->insert(position, value); 
	}

	inline void push_back(const value_type & value) { 
		m_variable_state->push_back(value); 
	}

	inline void pop_back(void) { 
		m_variable_state->pop_back(); 
	}

	inline iterator begin(void) { 
		return m_variable_state->begin(); 
	}

	inline iterator end(void) { 
		return m_variable_state->end(); 
	}

	inline const_iterator cbegin(void) const { 
		return m_variable_state->begin(); 
	}

	inline const_iterator cend(void) const { 
		return m_variable_state->end(); 
	}

	inline reverse_iterator rbegin(void) { 
		return m_variable_state->rbegin(); 
	}

	inline reverse_iterator rend(void) { 
		return m_variable_state->rend(); 
	}

	inline const_reverse_iterator crbegin(void) const { 
		return m_variable_state->crbegin(); 
	}

	inline const_reverse_iterator crend(void) const { 
		return m_variable_state->crend(); 
	}

	inline void reserve(size_t size) { 
		m_variable_state->reserve(size); 
	}

	inline void resize(size_t size) { 
		m_variable_state->resize(size); 
	}

	inline void clear(void) { 
		m_variable_state->clear(); 
	}

	inline bool empty(void) const { 
		return m_variable_state->empty(); 
	}

	inline size_t size(void) const { 
		return m_variable_state->size(); 
	}

public:
	inline value_type & operator[](size_t index) { 
		return (*m_variable_state)[index]; 
	}

	inline const value_type & operator[](size_t index) const { 
		return (*m_variable_state)[index]; 
	}

	/* Comparison */
	inline bool operator==(const differ_state & rhs) const {
		bool result = true;
		if (this->size() != rhs.size()) {
			result = false;
		}
		else {
			for (size_t i = 0; i < size(); i++) {
				if ((*this)[i] != rhs[i]) {
					result = false;
					break;
				}
			}
		}
		return result;
	}

	inline bool operator!=(const differ_state & rhs) const {
		return !(*this == rhs);
	}

	/* Assignment */
	inline differ_state & operator=(const differ_state & rhs) {
		if (this != &rhs) {
			m_variable_state->resize(rhs.size());
			std::copy(rhs.cbegin(), rhs.cend(), m_variable_state->begin());
		}

		return *this;
	}

	inline differ_state & operator+=(const double & rhs) {
		for (size_t i = 0; i < size(); i++) { 
			(*this)[i] += rhs; 
		}

		return *this;
	}

	inline differ_state & operator+=(const differ_state & rhs) {
		if (this->size() != rhs.size()) {
			throw std::runtime_error("Differetial states should consist of the same number of variables");
		}

		for (size_t i = 0; i < size(); i++) { 
			(*this)[i] += rhs[i]; 
		}

		return *this;
	}

	inline differ_state & operator-=(const double & rhs) {
		for (size_t i = 0; i < size(); i++) { 
			(*this)[i] -= rhs; 
		}

		return *this;
	}

	inline differ_state & operator-=(const differ_state & rhs) {
		if (this->size() != rhs.size()) {
			throw std::runtime_error("Differetial states should consist of the same number of variables");
		}

		for (size_t i = 0; i < size(); i++) { 
			(*this)[i] -= rhs[i]; 
		}

		return *this;
	}

	inline differ_state & operator*=(const double & rhs) {
		for (size_t i = 0; i < size(); i++) { 
			(*this)[i] *= rhs; 
		}

		return *this;
	}

	inline differ_state & operator*=(const differ_state & rhs) {
		if (this->size() != rhs.size()) {
			throw std::runtime_error("Differetial states should consist of the same number of variables");
		}

		for (size_t i = 0; i < size(); i++) { 
			(*this)[i] *= rhs[i]; 
		}

		return *this;
	}

	inline differ_state & operator/=(const double & rhs) {
		for (size_t i = 0; i < size(); i++) { 
			(*this)[i] /= rhs; 
		}

		return *this;
	}

	inline differ_state & operator/=(const differ_state & rhs) {
		if (this->size() != rhs.size()) {
			throw std::runtime_error("Differetial states should consist of the same number of variables");
		}

		for (size_t i = 0; i < size(); i++) { 
			(*this)[i] /= rhs[i]; 
		}

		return *this;
	}

	/* Arithmetic */
	inline differ_state operator+() const {
		return this;
	}

	inline differ_state operator-() const {
		return 0 - *this;
	}

	inline friend differ_state operator+(const differ_state & lhs, const double rhs) {
		differ_state result(lhs.size());
		for (unsigned int i = 0; i < result.size(); i++) { 
			result[i] = lhs[i] + rhs; 
		}

		return result;
	}

	inline friend differ_state operator+(const double lhs, const differ_state & rhs) { 
		return rhs + lhs; 
	}

	inline differ_state operator+(const differ_state & rhs) const {
		if (this->size() != rhs.size()) {
			throw std::runtime_error("Differetial states should consist of the same number of variables");
		}

		differ_state result(size());
		for (size_t i = 0; i < size(); i++) {
			result[i] = (*this)[i] + rhs[i];
		}

		return result;
	}

	inline friend differ_state operator-(const differ_state & lhs, const double rhs) {
		differ_state result(lhs.size());
		for (unsigned int i = 0; i < result.size(); i++) { 
			result[i] = lhs[i] - rhs; 
		}

		return result;
	}

	inline friend differ_state operator-(const double lhs, const differ_state & rhs) {
		differ_state result(rhs.size());
		for (unsigned int i = 0; i < result.size(); i++) { 
			result[i] = lhs - rhs[i]; 
		}

		return result;
	}

	inline differ_state operator-(const differ_state & rhs) const {
		if (this->size() != rhs.size()) {
			throw std::runtime_error("Differetial states should consist of the same number of variables");
		}

		differ_state result(size());
		for (size_t i = 0; i < size(); i++) {
			result[i] = (*this)[i] - rhs[i];
		}

		return result;
	}

	inline friend differ_state operator/(const differ_state & lhs, const double rhs) {
		differ_state result(lhs.size());
		for (unsigned int i = 0; i < result.size(); i++) { 
			result[i] = lhs[i] / rhs; 
		}

		return result;		
	}

	inline friend differ_state operator/(const double lhs, const differ_state & rhs) {
		differ_state result(rhs.size());
		for (unsigned int i = 0; i < result.size(); i++) { 
			result[i] = lhs / rhs[i]; 
		}

		return result;	
	}

	inline friend differ_state operator*(const differ_state & lhs, const double rhs) {
		differ_state result(lhs.size());
		for (unsigned int i = 0; i < result.size(); i++) { 
			result[i] = lhs[i] * rhs; 
		}

		return result;		
	}

	inline friend differ_state operator*(const double lhs, const differ_state & rhs) {
		return rhs * lhs;
	}

private:
	differ_variables * m_variable_state;
};


template <typename extra_type> using differ_extra = std::vector<extra_type>;

template <typename state_type> struct differ_output {
	double                    time;
	differ_state<state_type>  state;
};

template <typename state_type> using differ_result = std::vector<differ_output<state_type> >;


template <typename state_type, typename extra_type = void *> 
void runge_kutta_4(void (*function_pointer)(const double t, const differ_state<state_type> & inputs, const differ_extra<extra_type> & argv, differ_state<state_type> & outputs),
                   const differ_state<state_type> &		inputs,
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

	differ_output<state_type> current_result;
	current_result.time = time_start;
	current_result.state = inputs;

	for (unsigned int i = 0; i < steps; i++) {
		differ_state<state_type> fp1, fp2, fp3, fp4;
		differ_state<state_type> k1, k2, k3, k4;

		function_pointer(current_result.time, current_result.state, argv, fp1);
		k1 = fp1 * step;

		function_pointer(current_result.time + step / 2.0, current_result.state + k1 / 2.0, argv, fp2);
		k2 = fp2 * step;

		function_pointer(current_result.time + step / 2.0, current_result.state + k2 / 2.0, argv, fp3);
		k3 = fp3 * step;

		function_pointer(current_result.time + step, current_result.state + k3, argv, fp4);
		k4 = fp4 * step;

		current_result.state += (k1 + 2.0 * k2 + 2.0 * k3 + k4) / 6.0;
		current_result.time += step;

		if (flag_collect) {
			outputs[i].time = current_result.time;
			outputs[i].state = current_result.state;
		}
	}

	if (!flag_collect) {
		outputs[0].time = current_result.time;
		outputs[0].state = current_result.state;
	}
}


template <typename state_type, typename extra_type = void *> 
void runge_kutta_fehlberg_45(void (*function_pointer)(const double t, const differ_state<state_type> & inputs, const differ_extra<extra_type> & argv, differ_state<state_type> & outputs),
                   const differ_state<state_type> &		inputs,
                   const double							time_start,
                   const double							time_end,
                   const double					        tolerance,
                   const bool							flag_collect,
                   const differ_extra<extra_type> &		argv,
                   differ_result<state_type> &			outputs) {
	
	using namespace factor;

	if (flag_collect) {
		outputs.clear();
	}
	else {
		outputs.resize(1);
	}

	differ_output<state_type> current_result;
	current_result.time = time_start;
	current_result.state = inputs;

	double h = (time_end - time_start) / 10.0;		/* default number of steps */
	const double hmin = h / 1000.0;	/* default multiplier for maximum step size */
	const double hmax = 1000.0 * h;	/* default multiplier for minimum step size */

	const double br = time_end - 0.00001 * (double) std::abs(time_end);
	const unsigned int iteration_limit = 300;

	unsigned int iteration_counter = 0;

	while (current_result.time < time_end) {
		const double current_time = current_result.time;
		const differ_state<state_type> current_value = current_result.state;

		if ( (current_time + h) > br ) {
			h = time_end - current_result.time;
		}

		differ_state<state_type> fp1, fp2, fp3, fp4, fp5, fp6;
		differ_state<state_type> k1, k2, k3, k4, k5, k6;
		differ_state<state_type> y2, y3, y4, y5, y6;

		function_pointer(current_time, current_value, argv, fp1);
		k1 = h * fp1;
		y2 = current_value + B2 * k1;

		function_pointer(current_time + A2 * h, y2, argv, fp2);
		k2 = h * fp2;
		y3 = current_value + B3 * k1 + C3 * k2;

		function_pointer(current_time + A3 * h, y3, argv, fp3);
		k3 = h * fp3;
		y4 = current_value + B4 * k1 + C4 * k2 + D4 * k3;

		function_pointer(current_time + A4 * h, y4, argv, fp4);
		k4 = h * fp4;
		y5 = current_value + B5 * k1 + C5 * k2 + D5 * k3 + E5 * k4;

		function_pointer(current_time + A5 * h, y5, argv, fp5);
		k5 = h * fp5;
		y6 = current_value + B6 * k1 + C6 * k2 + D6 * k3 + E6 * k4 + F6 * k5;

		function_pointer(current_time + A6 * h, y6, argv, fp6);
		k6 = h * fp6;

		/* Calculate error (difference between Runge-Kutta 4 and Runge-Kutta 5) and new value. */
		differ_state<state_type> errors = R1 * k1 + R3 * k3 + R4 * k4 + R5 * k5 + R6 * k6;

		double err = 0.0;
		for (typename differ_state<state_type>::const_iterator iter = errors.cbegin(); iter != errors.cend(); iter++) {
			double current_error = std::abs(*iter);
			if (current_error > err) {
				err = current_error;
			}
		}

		/* Calculate new value. */
		differ_state<state_type> ynew = current_value + N1 * k1 + N3 * k3 + N4 * k4 + N5 * k5;

		if ( (err < tolerance) || (h < 2.0 * hmin) ) {
			current_result.state = ynew;

			if (current_time + h > br) {
				current_result.time = time_end;
			}
			else {
				current_result.time = current_time + h;
			}

			if (flag_collect) {
				outputs.push_back(current_result);
			}
			else {
				outputs[0] = current_result;
			}

			iteration_counter++;
		}

		double s = 0.0;
		if (err != 0.0) {
			s = 0.84 * std::pow( (tolerance * h / err), 0.25 );
		}

		if ( (s < 0.75) && (h > 2.0 * hmin) ) {
			h = h / 2.0;
		}

		if ( (s > 1.5) && (h * 2.0 < hmax) ) {
			h = 2.0 * h;
		}

		if (iteration_counter >= iteration_limit) {
			break;
		}
	}
}

}

#endif
