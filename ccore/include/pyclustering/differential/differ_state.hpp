/**
*
* @authors Andrei Novikov (pyclustering@yandex.ru)
* @date 2014-2019
* @copyright GNU Public License
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

#pragma once


#include <vector>
#include <memory>

#include "solve_type.hpp"


namespace pyclustering {

namespace differential {


template <class state_type, class allocator = std::allocator<state_type>>
class differ_state {
public:
    typedef state_type                          value_type;
    typedef std::vector<value_type>             differ_variables;

    typedef typename differ_variables::iterator                 iterator;
    typedef typename differ_variables::const_iterator           const_iterator;
    typedef typename differ_variables::reverse_iterator         reverse_iterator;
    typedef typename differ_variables::const_reverse_iterator   const_reverse_iterator;

public:
    differ_state() : m_variable_state(std::vector<state_type>()) { }

    explicit differ_state(const size_t size) : m_variable_state(std::vector<state_type>(size)) { }

    differ_state(const size_t size, const state_type value) : m_variable_state(std::vector<state_type>(size, value)) { }

    differ_state(const std::initializer_list<state_type> & value, const allocator & alloc = allocator()) : m_variable_state(std::vector<state_type>(value, alloc)) { }

    differ_state(const differ_state & instance) : m_variable_state(instance.m_variable_state) { }

    differ_state(const differ_state && instance) : m_variable_state(std::move(instance.m_variable_state)) { }

    ~differ_state() { }

public:
    void insert(iterator position, const value_type & value) {
        m_variable_state.insert(position, value);
    }

    void push_back(const value_type & value) {
        m_variable_state.push_back(value);
    }

    void pop_back() {
        m_variable_state.pop_back();
    }

    iterator begin() {
        return m_variable_state.begin();
    }

    iterator end() {
        return m_variable_state.end();
    }

    const_iterator cbegin() const {
        return m_variable_state.begin();
    }

    const_iterator cend() const {
        return m_variable_state.end();
    }

    reverse_iterator rbegin() {
        return m_variable_state.rbegin();
    }

    reverse_iterator rend() {
        return m_variable_state.rend();
    }

    const_reverse_iterator crbegin() const {
        return m_variable_state.crbegin();
    }

    const_reverse_iterator crend() const {
        return m_variable_state.crend();
    }

    void reserve(size_t size) {
        m_variable_state.reserve(size);
    }

    void resize(size_t size) {
        m_variable_state.resize(size);
    }

    void clear() {
        m_variable_state.clear();
    }

    bool empty() const {
        return m_variable_state.empty();
    }

    std::size_t size() const {
        return m_variable_state.size();
    }

public:
    value_type & operator[](std::size_t index) {
        return m_variable_state[index];
    }

    const value_type & operator[](std::size_t index) const {
        return m_variable_state[index];
    }

    /* Comparison */
    bool operator==(const differ_state & rhs) const {
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

    bool operator!=(const differ_state & rhs) const {
        return !(*this == rhs);
    }

    differ_state & operator=(const differ_state & rhs) = default;

    differ_state & operator=(differ_state && rhs) = default;

    differ_state & operator+=(const double & rhs) {
        for (size_t i = 0; i < size(); i++) {
            (*this)[i] += rhs;
        }

        return *this;
    }

    differ_state & operator+=(const differ_state & rhs) {
        if (this->size() != rhs.size()) {
            throw std::runtime_error("Differetial states should consist of the same number of variables");
        }

        for (size_t i = 0; i < size(); i++) {
            (*this)[i] += rhs[i];
        }

        return *this;
    }

    differ_state & operator-=(const double & rhs) {
        for (size_t i = 0; i < size(); i++) {
            (*this)[i] -= rhs;
        }

        return *this;
    }

    differ_state & operator-=(const differ_state & rhs) {
        if (this->size() != rhs.size()) {
            throw std::runtime_error("Differetial states should consist of the same number of variables");
        }

        for (size_t i = 0; i < size(); i++) {
            (*this)[i] -= rhs[i];
        }

        return *this;
    }

    differ_state & operator*=(const double & rhs) {
        for (size_t i = 0; i < size(); i++) {
            (*this)[i] *= rhs;
        }

        return *this;
    }

    differ_state & operator*=(const differ_state & rhs) {
        if (this->size() != rhs.size()) {
            throw std::runtime_error("Differetial states should consist of the same number of variables");
        }

        for (size_t i = 0; i < size(); i++) {
            (*this)[i] *= rhs[i];
        }

        return *this;
    }

    differ_state & operator/=(const double & rhs) {
        for (size_t i = 0; i < size(); i++) {
            (*this)[i] /= rhs;
        }

        return *this;
    }

    differ_state & operator/=(const differ_state & rhs) {
        if (this->size() != rhs.size()) {
            throw std::runtime_error("Differetial states should consist of the same number of variables");
        }

        for (size_t i = 0; i < size(); i++) {
            (*this)[i] /= rhs[i];
        }

        return *this;
    }

    /* Arithmetic */
    differ_state operator+() const {
        return this;
    }

    differ_state operator-() const {
        return 0 - *this;
    }

    friend differ_state operator+(const differ_state & lhs, const double rhs) {
        differ_state result(lhs.size());
        for (std::size_t i = 0; i < result.size(); i++) {
            result[i] = lhs[i] + rhs;
        }

        return result;
    }

    friend differ_state operator+(const double lhs, const differ_state & rhs) {
        return rhs + lhs;
    }

    differ_state operator+(const differ_state & rhs) const {
        if (this->size() != rhs.size()) {
            throw std::runtime_error("Differetial states should consist of the same number of variables");
        }

        differ_state result(size());
        for (size_t i = 0; i < size(); i++) {
            result[i] = (*this)[i] + rhs[i];
        }

        return result;
    }

    friend differ_state operator-(const differ_state & lhs, const double rhs) {
        differ_state result(lhs.size());
        for (std::size_t i = 0; i < result.size(); i++) {
            result[i] = lhs[i] - rhs;
        }

        return result;
    }

    friend differ_state operator-(const double lhs, const differ_state & rhs) {
        differ_state result(rhs.size());
        for (std::size_t i = 0; i < result.size(); i++) {
            result[i] = lhs - rhs[i];
        }

        return result;
    }

    differ_state operator-(const differ_state & rhs) const {
        if (this->size() != rhs.size()) {
            throw std::runtime_error("Differetial states should consist of the same number of variables");
        }

        differ_state result(size());
        for (size_t i = 0; i < size(); i++) {
            result[i] = (*this)[i] - rhs[i];
        }

        return result;
    }

    friend differ_state operator/(const differ_state & lhs, const double rhs) {
        differ_state result(lhs.size());
        for (std::size_t i = 0; i < result.size(); i++) {
            result[i] = lhs[i] / rhs;
        }

        return result;
    }

    friend differ_state operator/(const double lhs, const differ_state & rhs) {
        differ_state result(rhs.size());
        for (std::size_t i = 0; i < result.size(); i++) {
            result[i] = lhs / rhs[i];
        }

        return result;
    }

    friend differ_state operator*(const differ_state & lhs, const double rhs) {
        differ_state result(lhs.size());
        for (std::size_t i = 0; i < result.size(); i++) {
            result[i] = lhs[i] * rhs;
        }

        return result;
    }

    friend differ_state operator*(const double lhs, const differ_state & rhs) {
        return rhs * lhs;
    }

private:
    differ_variables m_variable_state;
};


template <class extra_type = void *>
using differ_extra = std::vector<extra_type>;


template <class state_type = double>
struct differ_output {
    double                    time;
    differ_state<state_type>  state;
};


template <class state_type> 
using differ_result = std::vector< differ_output<state_type> >;


template <class state_type>
using differ_result_ptr = std::shared_ptr< differ_result<state_type> >;


}

}