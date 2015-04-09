#ifndef _DIFFERENTIAL_H_
#define _DIFFERENTIAL_H_

#include <vector>
#include <initializer_list>

namespace differential {

template <typename state_type>
class differ_state : std::vector<state_type> {
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

template <typename input_type>
void runge_kutta_fehlberg_45(void);

}

#endif