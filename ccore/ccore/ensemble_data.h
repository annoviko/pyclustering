#ifndef _ENSEMBLE_DATA_H_
#define _ENSEMBLE_DATA_H_

#include <vector>

template <typename sync_ensemble_type>
class ensemble_data {
public:
    typedef sync_ensemble_type				value_type;
    typedef std::vector<value_type>			sync_ensembles;

    typedef typename sync_ensembles::iterator			iterator;
    typedef typename sync_ensembles::const_iterator		const_iterator;
    typedef typename sync_ensembles::reverse_iterator	reverse_iterator;

public:
    ensemble_data(void) : m_ensembles(new sync_ensembles()) { };
    ensemble_data(const ensemble_data & rhs) {
        (*m_ensembles) = rhs;
    }

    ~ensemble_data(void) { delete m_ensembles; }

public:
    inline void insert(iterator position, const value_type & value) { m_ensembles->insert(position, value); }

    inline void push_back(const value_type & ensemble) { m_ensembles->push_back(ensemble); }
    inline void pop_back(void) { m_ensembles->pop_back(); }

    inline iterator begin(void) { return m_ensembles->begin(); }
    inline iterator end(void) { return m_ensembles->end(); }

    inline const_iterator cbegin(void) const { return m_ensembles->begin(); }
    inline const_iterator cend(void) const { return m_ensembles->end(); }

    inline reverse_iterator rbegin(void) { return m_ensembles->rbegin(); }
    inline reverse_iterator rend(void) { return m_ensembles->rend(); }

    inline void reserve(size_t size) { m_ensembles->reserve(size); }
    inline void clear(void) { m_ensembles->clear(); }

    inline size_t size(void) { return m_ensembles->size(); }

    inline value_type & operator[](size_t index) { return (*m_ensembles)[index]; };
    inline const value_type & operator[](size_t index) const { return (*m_ensembles)[index]; };

private:
    sync_ensembles * m_ensembles;
};

#endif