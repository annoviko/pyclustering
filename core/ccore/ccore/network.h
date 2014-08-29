#ifndef _INTERFACE_NETWORK_H_
#define _INTERFACE_NETWORK_H_

#include <cmath>
#include <vector>
#include <stdexcept>

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
	TOTAL_NUMBER_CONN_TYPES
} conn_type;


typedef enum conn_repr_type {
	MATRIX_CONN_REPRESENTATION,
	BITMAP_CONN_REPRESENTATION,
	TOTAL_NUMBER_CONN_REPR_TYPES
} conn_repr_type;


class network {
protected:
	unsigned int									num_osc;
	conn_repr_type									conn_representation;

private:
	std::vector<std::vector<unsigned int> * >		* osc_conn;

public:
	network(const unsigned int number_oscillators, const conn_type connection_type);
	virtual ~network();

	inline unsigned int size(void) const { return num_osc; }

	inline unsigned int get_connection(const unsigned int index1, const unsigned int index2) const { 
		switch(conn_representation) {
			case MATRIX_CONN_REPRESENTATION: {
				return (*(*osc_conn)[index1])[index2];
			}
			case BITMAP_CONN_REPRESENTATION: {
				const unsigned int index_element = index2 / ( sizeof(unsigned int) << 3 );
				const unsigned int bit_number = index2 - ( index_element * (sizeof(unsigned int) << 3) );

				return ( (*(*osc_conn)[index1])[index_element] >> bit_number ) & (unsigned int) 0x01;
			}
			default: {
				throw std::runtime_error("Unknown type of representation of connections");
			}
		}
	}

	inline void set_connection(const unsigned int index1, const unsigned int index2) {
		switch(conn_representation) {
			case MATRIX_CONN_REPRESENTATION: {
				(*(*osc_conn)[index1])[index2] = 1;
				break;
			}
			case BITMAP_CONN_REPRESENTATION: {
				unsigned int index_element = index2 / ( sizeof(unsigned int) << 3 );
				unsigned int bit_number = index2 % ( sizeof(unsigned int) << 3 );

				(*(*osc_conn)[index1])[index_element] = (*(*osc_conn)[index1])[index_element] | ( (unsigned int) 0x01 << bit_number );
				break;
			}
			default: {
				throw std::runtime_error("Unknown type of representation of connections");
			}
		}
	}

	std::vector<unsigned int> * get_neighbors(const unsigned int index) const;

	virtual void create_structure(const conn_type connection_structure);

private:
	void create_all_to_all_connections(void);
	void create_grid_four_connections(void);
	void create_grid_eight_connections(void);
	void create_list_bidir_connections(void);
	void create_none_connections(void);
};

#endif