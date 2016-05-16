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

#ifndef _ENSEMBLE_DATA_H_
#define _ENSEMBLE_DATA_H_


#include <vector>


namespace container {

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

}

#endif
