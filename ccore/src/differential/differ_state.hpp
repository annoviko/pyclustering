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

#ifndef CCORE_DIFFERENTIAL_DIFFER_STATE_HPP_
#define CCORE_DIFFERENTIAL_DIFFER_STATE_HPP_


#include <vector>
#include <memory>


namespace differential {

template <typename state_type>
class differ_state {
public:
    typedef state_type                          value_type;
    typedef std::vector<value_type>             differ_variables;

    typedef typename differ_variables::iterator                 iterator;
    typedef typename differ_variables::const_iterator           const_iterator;
    typedef typename differ_variables::reverse_iterator         reverse_iterator;
    typedef typename differ_variables::const_reverse_iterator   const_reverse_iterator;

public:
    differ_state(void) : m_variable_state(std::vector<state_type>()) { }

    differ_state(const size_t size) : m_variable_state(std::vector<state_type>(size)) { }

    differ_state(const size_t size, const state_type value) : m_variable_state(std::vector<state_type>(size, value)) { }

    differ_state(const std::initializer_list<state_type> & value) : m_variable_state(std::vector<state_type>(value)) { }

    differ_state(const differ_state & instance) : m_variable_state(instance.m_variable_state) { }

    differ_state(const differ_state && instance) : m_variable_state(std::move(instance.m_variable_state)) { }

    ~differ_state(void) { }

public:
    inline void insert(iterator position, const value_type & value) {
        m_variable_state.insert(position, value);
    }

    inline void push_back(const value_type & value) {
        m_variable_state.push_back(value);
    }

    inline void pop_back(void) {
        m_variable_state.pop_back();
    }

    inline iterator begin(void) {
        return m_variable_state.begin();
    }

    inline iterator end(void) {
        return m_variable_state.end();
    }

    inline const_iterator cbegin(void) const {
        return m_variable_state.begin();
    }

    inline const_iterator cend(void) const {
        return m_variable_state.end();
    }

    inline reverse_iterator rbegin(void) {
        return m_variable_state.rbegin();
    }

    inline reverse_iterator rend(void) {
        return m_variable_state.rend();
    }

    inline const_reverse_iterator crbegin(void) const {
        return m_variable_state.crbegin();
    }

    inline const_reverse_iterator crend(void) const {
        return m_variable_state.crend();
    }

    inline void reserve(size_t size) {
        m_variable_state.reserve(size);
    }

    inline void resize(size_t size) {
        m_variable_state.resize(size);
    }

    inline void clear(void) {
        m_variable_state.clear();
    }

    inline bool empty(void) const {
        return m_variable_state.empty();
    }

    inline size_t size(void) const {
        return m_variable_state.size();
    }

public:
    inline value_type & operator[](size_t index) {
        return m_variable_state[index];
    }

    inline const value_type & operator[](size_t index) const {
        return m_variable_state[index];
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
            m_variable_state.resize(rhs.size());
            std::copy(rhs.cbegin(), rhs.cend(), m_variable_state.begin());
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
    differ_variables m_variable_state;
};


template <typename extra_type> using differ_extra = std::vector<extra_type>;


template <typename state_type> struct differ_output {
    double                    time;
    differ_state<state_type>  state;
};


template <typename state_type> using differ_result = std::vector<differ_output<state_type> >;

}

#endif
