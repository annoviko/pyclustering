#ifndef _DYNAMIC_DATA_H_
#define _DYNAMIC_DATA_H_

#include <vector>

/***********************************************************************************************
*
* @brief   Collection that stores dynamic of oscillatory networks - state of each oscillator on
*          each iteration.
*
* @details Requires type of network dynamic state that supports method 'size() const'.
*
***********************************************************************************************/
template <typename network_dynamic_type>
class dynamic_data {
public:
    typedef network_dynamic_type				value_type;
    typedef std::vector<value_type>				output_dynamic;

    typedef typename output_dynamic::iterator					iterator;
    typedef typename output_dynamic::const_iterator				const_iterator;
    typedef typename output_dynamic::reverse_iterator			reverse_iterator;
    typedef typename output_dynamic::const_reverse_iterator		const_reverse_iterator;

public:
    dynamic_data(void) : m_dynamic(new output_dynamic()), m_number_oscillators(0) { };

    dynamic_data(const size_t size) : m_dynamic(new output_dynamic(size)) { };

    dynamic_data(const size_t size, const value_type & initial_value) : m_dynamic(new output_dynamic(size, initial_value)), m_number_oscillators(initial_value.size()) { };

    dynamic_data(const dynamic_data & rhs) {
        m_number_oscillators = rhs.m_number_oscillators;

        m_dynamic = new output_dynamic(rhs.size());
        std::copy(rhs.cbegin(), rhs.cend(), m_dynamic->begin());
    }

    ~dynamic_data(void) { delete m_dynamic; }

public:
    inline void insert(iterator position, const value_type & value) {
        if (empty()) {
            m_number_oscillators = value.size();
        }
        else if (m_number_oscillators != value.size()) {
            throw std::runtime_error("Dynamic collection can consist of network states with the same size only");
        }

        m_dynamic->insert(position, value);
    }

    inline void push_back(const value_type & value) {
        if (empty()) {
            m_number_oscillators = value.size();
        }
        else if (m_number_oscillators != value.size()) {
            throw std::runtime_error("Dynamic collection can consist of network states with the same size only");
        }

        m_dynamic->push_back(value);
    }

    inline void pop_back(void) {
        m_dynamic->pop_back();

        if (empty()) {
            m_number_oscillators = 0;
        }
        else {
            m_number_oscillators--;
        }
    }

    inline iterator begin(void) { return m_dynamic->begin(); }
    inline iterator end(void) { return m_dynamic->end(); }

    inline const_iterator cbegin(void) const { return m_dynamic->begin(); }
    inline const_iterator cend(void) const { return m_dynamic->end(); }

    inline reverse_iterator rbegin(void) { return m_dynamic->rbegin(); }
    inline reverse_iterator rend(void) { return m_dynamic->rend(); }

    inline const_reverse_iterator crbegin(void) const { return m_dynamic->crbegin(); }
    inline const_reverse_iterator crend(void) const { return m_dynamic->crend(); }

    inline void reserve(size_t size) {
        m_dynamic->reserve(size);
    }

    inline void resize(size_t size, size_t number_oscillators) {
        m_dynamic->resize(size);
        m_number_oscillators = number_oscillators;
    }

    inline void clear(void) {
        m_dynamic->clear();
        m_number_oscillators = 0;
    }

    inline bool empty(void) const { return m_dynamic->empty(); }
    inline size_t size(void) const { return m_dynamic->size(); }
    inline size_t number_oscillators(void) const { return m_number_oscillators; }

    inline value_type & operator[](size_t index) { return (*m_dynamic)[index]; };
    inline const value_type & operator[](size_t index) const { return (*m_dynamic)[index]; };

public:
    /***********************************************************************************************
    *
    * @brief   Returns dynamic state of the network at the specified iteration step.
    *
    * @param[in] iteration (size_t): number of iteration at which dynamic is required.
    *
    * @return (value_type &) reference to dynamic state of the network at the specified iteration.
    *
    ***********************************************************************************************/
    inline const value_type & dynamic_at(const size_t iteration) const {
        return (*m_dynamic)[iteration];
    }

private:
    output_dynamic * m_dynamic;
    size_t m_number_oscillators;
};

#endif
