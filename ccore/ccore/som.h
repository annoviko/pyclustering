#ifndef _SOM_H_
#define _SOM_H_

#include <vector>

typedef enum som_conn_type {
	GRID_FOUR,
	GRID_EIGHT,
	HONEYCOMB,
	FUNC_NEIGHBOR
} som_conn_type;

typedef enum som_init_type {
	RANDOM,
	RANDOM_CENTROID,
	RANDOM_SURFACE,
	UNIFORM_GRID
};

/***********************************************************************************************
 *
 * @brief   Self-Orzanized Feature Map based on Kohonen desription of SOM.
 *
 ***********************************************************************************************/
class som {
protected:
	/* network description */
	unsigned int rows;
	unsigned int cols;
	unsigned int size;

	som_conn_type conn_type;

	std::vector<std::vector<double> * > * weights;
	std::vector<std::vector<unsigned int> * > * awards;

	std::vector<std::vector<double> > * data;

	/* just for convenience (avoid excess calculation during learning) */
	std::vector<std::vector<double> * > * location;
	std::vector<std::vector<double> * > *  sqrt_distances;
	std::vector<std::vector<unsigned int> * > * capture_objects;
	std::vector<std::vector<unsigned int> * > * neighbors;

	/* describe learning process and internal state */
	unsigned int enophs;
	double init_radius;
	double init_learn_rate;
	double adaptation_threshold;

	/* dynamic changes learning parameters */
	double local_radius;
	double learn_rate;

public:
	som(std::vector<std::vector<double> > * input_data, const unsigned int num_rows, const unsigned int num_cols, const unsigned int num_epochs, const som_conn_type type_conn, const som_init_type type_init);
	
	~som(void);

private:
	void create_connections(som_conn_type type_conn);

	void create_initial_weights(som_init_type type_init);
};



#endif