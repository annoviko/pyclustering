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
#include <cstddef>

#include <pyclustering/definitions.hpp>


namespace pyclustering {

namespace nnet {


/**
*
* @brief   Connection structures that can be established in self-organized feature map.
*
*/
enum class som_conn_type {
    /*!< Each node is connected with four neighbors: left, upper, right and lower. */
    SOM_GRID_FOUR = 0,

    /*!< Grid type of connections when each oscillator has connections with left, upper-left, upper, upper-right, right, right-lower, lower, lower-left neighbors. */
    SOM_GRID_EIGHT = 1,

    /*!< Grid type of connections when each oscillator has connections with left, upper-left, upper-right, right, right-lower, lower-left neighbors. */
    SOM_HONEYCOMB = 2,

    /*!< Grid type of connections when existance of each connection is defined by the SOM rule on each step of simulation. */
    SOM_FUNC_NEIGHBOR = 3
};


/**
*
* @brief   Types of inititalization of weights in self-organized feature map.
*
*/
enum class som_init_type {
    /*!< Weights are randomly distributed using Gaussian distribution (0, 1). */
    SOM_RANDOM = 0,

    /*!< Weights are randomly distributed using Gaussian distribution (input data centroid, 1). */
    SOM_RANDOM_CENTROID = 1,

    /*!< Weights are randomly distrbiuted using Gaussian distribution (input data centroid, surface of input data). */
    SOM_RANDOM_SURFACE = 2,

    /*!< Weights are distributed as a uniform grid that covers whole surface of the input data. */
    SOM_UNIFORM_GRID = 3
};


/**
*
* @brief   Parameters of self-organized feature map.
*
*/
struct som_parameters {
    som_init_type init_type       = som_init_type::SOM_UNIFORM_GRID;
    double init_radius            = 0.0;
    double init_learn_rate        = 0.1;
    double adaptation_threshold   = 0.01;

public:
    som_parameters() = default;

    som_parameters(som_parameters && p_other) = default;

    som_parameters(const som_parameters & p_other) = default;

    ~som_parameters() = default;

public:
    som_parameters & operator=(const som_parameters & p_other);
};


using som_award_sequence    = std::vector<size_t>;

using som_gain_sequence     = std::vector<std::vector<size_t> >;

using som_neighbor_sequence = std::vector<std::vector<size_t> >;


/**
 *
 * @brief   Self-Orzanized Feature Map based on Kohonen desription of SOM.
 *
 */
class som {
private:
    /* network description */
    std::size_t m_rows;
    std::size_t m_cols;
    std::size_t m_size;

    som_conn_type m_conn_type;

    dataset             m_weights;
    dataset             m_previous_weights;
    som_award_sequence  m_awards;

    /* store pointer to training data for convinience */
    const dataset     * m_data = nullptr;

    /* just for convenience (avoid excess calculation during learning) */
    dataset                 m_location;
    dataset                 m_sqrt_distances;
    som_gain_sequence       m_capture_objects;
    som_neighbor_sequence   m_neighbors;

    /* describe learning process and internal state */
    std::size_t     m_epouchs = 0;
    som_parameters  m_params;

    /* dynamic changes learning parameters */
    double m_local_radius = 0.0;
    double m_learn_rate = 0.0;

public:
    /**
     *
     * @brief   Constructor of self-organized map.
     *
     * @param[in] rows: number of neurons in the column (number of rows).
     * @param[in] cols: number of neurons in the row (number of columns).
     * @param[in] conn_type: type of connection between oscillators in the network.
     * @param[in] parameters: others parameters of the network.
     *
     */
    som(const std::size_t num_rows, const std::size_t num_cols, const som_conn_type type_conn, const som_parameters & parameters);

    /**
     *
     * @brief   Copy constructor.
     *
     * @param[in] p_other: self-organized map that should be copied.
     *
     */
    som(const som & p_other);

    /**
     *
     * @brief   Default destructor.
     *
     */
    ~som();

public:
    /**
     *
     * @brief   Trains self-organized feature map (SOM).
     *
     * @param[in] input_data: input dataset for training.
     * @param[in] num_epochs: number of epochs for training.
     * @param[in] autostop: stop learining when convergance is too low.
     *
     * @return  Returns number of learining iterations.
     *
     */
    std::size_t train(const dataset & input_data, const size_t num_epochs, bool autostop);

    /**
     *
     * @brief   Initialize SOM network by loading weights.
     * @details This method is provided service to load trained network parameters to avoid network training that may take
     *           a lot of time.
     *
     * @param[in] p_weights: neuron weights.
     * @param[in] p_awards: amount of captured objects by each neuron during training (can be empty if it is not required).
     * @param[in] p_capture_objects: captured objects by each neuron during training (can be empty if it is not required).
     *
     * @return  Returns number of learining iterations.
     *
     */
    void load(const dataset & p_weights, const som_award_sequence & p_awards, const som_gain_sequence & p_capture_objects);

    /**
     *
     * @brief   Processes input pattern (no learining) and returns index of neuron-winner.
     * @details Using index of neuron winner catched object can be obtained by get_capture_objects().
     *
     * @param[in] input_pattern: input pattern for processing.
     *
     * @return  Returns index of neuron-winner.
     *
     */
    std::size_t simulate(const pattern & input_pattern) const;

    /**
     *
     * @return  Returns number of winner at the last step of learning process.
     *
     */
    std::size_t get_winner_number() const;

    /**
     *
     * @return  Returns size of self-organized map (number of neurons).
     *
     */
    inline size_t get_size() const { return m_size; }

    /**
    *
    * @return  Constant reference to neurons weights for read-only purposes.
    *
    */
    inline const dataset & get_weights() const {
        return m_weights;
    }

    /**
    *
    * @return  Constant reference to sequence of captured objects by each neuron during training for read-only purposes.
    *
    */
    inline const som_gain_sequence & get_capture_objects() const {
        return m_capture_objects;
    }

    /**
    *
    * @return  Constant reference to neighbors of each neuron for read-only purposes.
    *
    */
    inline const som_neighbor_sequence & get_neighbors() const {
        return m_neighbors;
    }

    /**
    *
    * @return  Constant reference to amount of captured objects by each neuron during training for read-only purposes.
    *
    */
    inline const som_award_sequence & get_awards() const {
       return m_awards;
    }

    /**
    *
    * @return  Reference to amount of captured objects by each neuron during training.
    *
    */
    inline som_award_sequence & get_awards() {
        return m_awards;
    }

private:
    /**
     *
     * @brief   Create connections in line with input rule (grid four, grid eight, honeycomb,
     *          function neighbour).
     *
     * @param[in] type: type of connection between oscillators in the network.
     *
     */
    void create_connections(const som_conn_type type);

    /**
     *
     * @brief   Creates initial weights for neurons in line with the specified initialization.
     *
     * @param[in] type: type of initialization of initial neuron weights (random,
     *             random in center of the input data, random distributed in
     *             data, ditributed in line with uniform grid).
     *
     */
    void create_initial_weights(const som_init_type type);

    /**
     *
     * @brief   Returns neuron winner (distance, neuron index).
     *
     * @param[in] input_pattern: input pattern from the input data set, for example it can be
     *             coordinates of point.
     *
     * @return  Returns index of neuron that is winner.
     *
     */
    std::size_t competition(const pattern & input_pattern) const;

    /**
     *
     * @brief   Change weight of neurons in line with won neuron.
     *
     * @param[in] index_winner: index of neuron-winner.
     * @param[in] input_pattern: input pattern from the input data set.
     *
     */
    std::size_t adaptation(const size_t index_winner, const pattern & input_pattern);

    /**
     *
     * @brief   Returns maximum changes of weight in line with comparison between previous weights
     *          and current weights.
     *
     * @return  Returns value that represents maximum changes of weight after adaptation process.
     *
     */
    double calculate_maximal_adaptation() const;

    /**
    *
    * @brief   Calculates appropriate initial radius.
    *
    * @param[in] p_rows: amount of rows in the map.
    * @param[in] p_cals: amount of columns in the map.
    *
    * @return  Initial radius.
    *
    */
    static double calculate_init_radius(const size_t p_rows, const size_t p_cols);

public:
    /**
    *
    * @brief   Store network to stream.
    *
    * @param[in] p_stream: stream that is used to store network.
    * @param[in] p_network: SOM network that is stored to the stream 'p_stream'.
    *
    * @return  Stream where network is stored.
    *
    */
    friend std::ostream & operator<<(std::ostream & p_stream, const som & p_network);

    /**
    *
    * @brief   Overloaded assignment operator to make deep copy of SOM.
    *
    * @param[in] p_other: another instance of SOM.
    *
    * @return  Reference to updated SOM instance.
    *
    */
    som & operator=(const som & p_other);
};


}

}