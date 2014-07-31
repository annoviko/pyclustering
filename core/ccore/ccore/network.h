#ifndef _INTERFACE_NETWORK_H_
#define _INTERFACE_NETWORK_H_

#include <vector>

typedef enum initial_type {
	RANDOM_GAUSSIAN,
	EQUIPARTITION,
	TOTAL_NUMBER_INITIAL_TYPES
} initial_type;


typedef enum solve_type {
	FAST,
	RK4,
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


class network {
protected:
	unsigned int									num_osc;
	std::vector<std::vector<unsigned int> * >		* osc_conn;

public:
	network(const unsigned int number_oscillators, const conn_type connection_type);
	virtual ~network();

	inline unsigned int size(void) const { return num_osc; }
	inline unsigned int get_connection(const unsigned int index1, const unsigned int index2) const { return (*(*osc_conn)[index1])[index2]; }

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