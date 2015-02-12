#ifndef _SOM_H_
#define _SOM_H_

#include <vector>

typedef enum som_conn_type {
	SOM_GRID_FOUR,
	SOM_GRID_EIGHT,
	SOM_HONEYCOMB,
	SOM_FUNC_NEIGHBOR
} som_conn_type;

typedef enum som_init_type {
	SOM_RANDOM,
	SOM_RANDOM_CENTROID,
	SOM_RANDOM_SURFACE,
	SOM_UNIFORM_GRID
} som_init_type;

/***********************************************************************************************
 *
 * @brief   Self-Orzanized Feature Map based on Kohonen desription of SOM.
 *
 ***********************************************************************************************/
class som {
private:
	/* network description */
	unsigned int rows;
	unsigned int cols;
	unsigned int size;

	som_conn_type conn_type;

	std::vector<std::vector<double> * > * weights;
	std::vector<std::vector<double> * > * previous_weights;
	std::vector<unsigned int> * awards;

	std::vector<std::vector<double> > * data;

	/* just for convenience (avoid excess calculation during learning) */
	std::vector<std::vector<double> * > * location;
	std::vector<std::vector<double> * > *  sqrt_distances;
	std::vector<std::vector<unsigned int> * > * capture_objects;
	std::vector<std::vector<unsigned int> * > * neighbors;

	/* describe learning process and internal state */
	unsigned int epouchs;
	double init_radius;
	double init_learn_rate;
	double adaptation_threshold;

	/* dynamic changes learning parameters */
	double local_radius;
	double learn_rate;

public:
	som(std::vector<std::vector<double> > * input_data, const unsigned int num_rows, const unsigned int num_cols, const unsigned int num_epochs, const som_conn_type type_conn, const som_init_type type_init);
	
	~som(void);

	unsigned int train(bool autostop);

	unsigned int simulate(const std::vector<double> * pattern) const;

	unsigned int get_winner_number(void) const;

	inline unsigned int get_size(void) const { return size; }

	inline const std::vector<std::vector<double> * > * const get_weights(void) const { return weights; }

	inline const std::vector<std::vector<unsigned int> * > * const get_capture_objects(void) const { return capture_objects; }

	inline const std::vector<std::vector<unsigned int> * > * const get_neighbors(void) const { return neighbors; }
	
	inline const std::vector<unsigned int> * const get_awards(void) const { return awards; }

private:
	void create_connections(const som_conn_type type_conn);

	void create_initial_weights(const som_init_type type_init);

	unsigned int competition(const std::vector<double> * pattern) const;

	unsigned int adaptation(const unsigned int index_winner, const std::vector<double> * pattern);

	double calculate_maximal_adaptation(void) const;
};

#endif