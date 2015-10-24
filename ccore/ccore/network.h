/**************************************************************************************************************

Abstract network representation that is used as a basic class.

Based on book description:
 - J.B.MacQueen. Some Methods for Classification and Analysis of Multivariate Observations. 1967.

Copyright (C) 2015    Andrei Novikov (pyclustering@yandex.ru)

pyclustering is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

pyclustering is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.

**************************************************************************************************************/

#ifndef _INTERFACE_NETWORK_H_
#define _INTERFACE_NETWORK_H_

#include <cmath>
#include <vector>
#include <stdexcept>
#include <memory>

#include "dynamic_data.h"

#define MAXIMUM_OSCILLATORS_MATRIX_REPRESENTATION	(unsigned int) 4096

typedef enum initial_type {
	RANDOM_GAUSSIAN,
	EQUIPARTITION,
	TOTAL_NUMBER_INITIAL_TYPES
} initial_type;


typedef enum solve_type {
	FAST,
	RK4,
	RKF45,
	TOTAL_NUMBER_SOLVE_TYPES
} solve_type;


typedef enum conn_type {
	NONE,
	ALL_TO_ALL,
	GRID_FOUR,
	GRID_EIGHT,
	LIST_BIDIR,
	DYNAMIC,
	TOTAL_NUMBER_CONN_TYPES
} conn_type;


typedef enum conn_repr_type {
	MATRIX_CONN_REPRESENTATION,
	BITMAP_CONN_REPRESENTATION,
	LIST_CONN_REPRESENTATION,
	TOTAL_NUMBER_CONN_REPR_TYPES
} conn_repr_type;



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


class network {
private:
	unsigned int			num_osc;
	unsigned int            width_osc;
	unsigned int            height_osc; 
	conn_repr_type			conn_representation;
	conn_type				m_conn_type;

	std::vector<std::vector<unsigned int> >		m_osc_conn;

public:
	network(const unsigned int number_oscillators, 
		 	const conn_type connection_type,
		 	const unsigned int width_oscillators,
    	 	const unsigned int height_oscillators);

	virtual ~network();

	inline unsigned int size(void) const { return num_osc; }

	virtual unsigned int get_connection(const unsigned int index1, const unsigned int index2) const;

	virtual void set_connection(const unsigned int index1, const unsigned int index2);

	virtual void get_neighbors(const unsigned int index, std::vector<unsigned int> & result) const;

    virtual void create_structure(const conn_type connection_structure);
	
private:
	void create_grid_four_connections(void);
	void create_grid_eight_connections(void);
	void create_list_bidir_connections(void);
};

#endif
