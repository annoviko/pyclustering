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

#include <pyclustering/nnet/som.hpp>

#include <chrono>
#include <cmath>
#include <climits>
#include <exception>
#include <random>

#include <pyclustering/utils/metric.hpp>


using namespace pyclustering::utils::metric;


namespace pyclustering {

namespace nnet {


som_parameters & som_parameters::operator=(const som_parameters & p_other) {
    if (&p_other != this) {
        init_type = p_other.init_type;
        init_radius = p_other.init_radius;
        init_learn_rate = p_other.init_learn_rate;
        adaptation_threshold = p_other.adaptation_threshold;
    }

    return *this;
}


som::som(const size_t num_rows, const size_t num_cols, const som_conn_type type_conn, const som_parameters & parameters) :
    m_rows(num_rows),
    m_cols(num_cols),
    m_size(num_rows * num_cols),
    m_conn_type(type_conn),
    m_awards(m_size, 0),
    m_data(nullptr),
    m_location(m_size),
    m_sqrt_distances(m_size, std::vector<double>(m_size, 0)),
    m_capture_objects(m_size),
    m_params(parameters) 
{
    if (m_params.init_radius == 0.0) {
        m_params.init_radius = calculate_init_radius(m_rows, m_cols);
    }

    /* location */
    for (size_t i = 0; i < m_rows; i++) {
        for (size_t j = 0; j < m_cols; j++) {
            std::vector<double> neuron_location(2, 0);
            neuron_location[0] = (double) i;
            neuron_location[1] = (double) j;

            m_location[i * m_cols + j] = neuron_location;
        }
    }

    /* distances */
    for (std::size_t i = 0; i < m_size; i++) {
        std::vector<double> column_distances(m_size, 0);
        m_sqrt_distances[i] = column_distances;
    }

    for (std::size_t i = 0; i < m_size; i++) {
        m_sqrt_distances[i][i] = 0.0;
        for (std::size_t j = i + 1; j < m_size; j++) {
            double distance = euclidean_distance_square(m_location[i], m_location[j]);
            m_sqrt_distances[i][j] = distance;
            m_sqrt_distances[j][i] = distance;
        }
    }

    /* connections */
    if (type_conn != som_conn_type::SOM_FUNC_NEIGHBOR) {
        create_connections(type_conn);
    }
}


som::som(const som & p_other) {
    operator=(p_other);
}


som::~som() { }


void som::create_connections(const som_conn_type type) {
    m_neighbors.resize(m_size);

    for (int index = 0; index < (int) m_size; index++) {
        std::vector<size_t> & neuron_neighbors = m_neighbors[index];

        int upper_index = index - (int) m_cols;
        int upper_left_index = index - (int) m_cols - 1;
        int upper_right_index = index - (int) m_cols + 1;

        int lower_index = index + (int) m_cols;
        int lower_left_index = index + (int) m_cols - 1;
        int lower_right_index = index + (int) m_cols + 1;

        int left_index = index - 1;
        int right_index = index + 1;

        int node_row_index = (int) std::floor( (double) index / (double) m_cols );
        int upper_row_index = node_row_index - 1;
        int lower_row_index = node_row_index + 1;

        if ( (type == som_conn_type::SOM_GRID_EIGHT) || (type == som_conn_type::SOM_GRID_FOUR) ) {
            if (upper_index >= 0) {
                neuron_neighbors.push_back(upper_index);
            }

            if (lower_index < (int) m_size) {
                neuron_neighbors.push_back(lower_index);
            }
        }

        if ( (type == som_conn_type::SOM_GRID_EIGHT) || (type == som_conn_type::SOM_GRID_FOUR) || (type == som_conn_type::SOM_HONEYCOMB) ) {
            if ( (left_index >= 0) && ( (int) std::floor((double) left_index / (double) m_cols) == node_row_index) ) {
                neuron_neighbors.push_back(left_index);
            }

            if ( (int) std::floor((double) right_index / (double) m_cols) == node_row_index ) {
                neuron_neighbors.push_back(right_index);
            }
        }

        if (type == som_conn_type::SOM_GRID_EIGHT) {
            if ( (upper_left_index >= 0) && ( (int) std::floor((double) upper_left_index / (double) m_cols) == upper_row_index) ) {
                neuron_neighbors.push_back(upper_left_index);
            }

            if ( (upper_right_index >= 0) && ( (int) std::floor((double) upper_right_index / (double) m_cols) == upper_row_index) ) {
                neuron_neighbors.push_back(upper_right_index);
            }

            if ( (lower_left_index < (int) m_size) && ( (int) std::floor((double) lower_left_index / (double) m_cols) == lower_row_index) ) {
                neuron_neighbors.push_back(lower_left_index);
            }

            if ( (lower_right_index < (int) m_size) && ( (int) std::floor((double) lower_right_index / (double) m_cols) == lower_row_index) ) {
                neuron_neighbors.push_back(lower_right_index);
            }
        }

        if (type == som_conn_type::SOM_HONEYCOMB) {
            if ( (node_row_index % 2) == 0 ) {
                upper_left_index = index - (int) m_cols;
                upper_right_index = index - (int) m_cols + 1;

                lower_left_index = index + (int) m_cols;
                lower_right_index = index + (int) m_cols + 1;
            }
            else {
                upper_left_index = index - (int) m_cols - 1;
                upper_right_index = index - (int) m_cols;

                lower_left_index = index + (int) m_cols - 1;
                lower_right_index = index + (int) m_cols;
            }

            if ( (upper_left_index >= 0) && ( (int) std::floor((double) upper_left_index / (double) m_cols) == upper_row_index) ) {
                neuron_neighbors.push_back(upper_left_index);
            }

            if ( (upper_right_index >= 0) && ( (int) std::floor((double) upper_right_index / (double) m_cols) == upper_row_index) ) {
                neuron_neighbors.push_back(upper_right_index);
            }

            if ( (lower_left_index < (int) m_size) && ( (int) std::floor((double) lower_left_index / (double) m_cols) == lower_row_index) ) {
                neuron_neighbors.push_back(lower_left_index);
            }

            if ( (lower_right_index < (int) m_size) && ( (int) std::floor((double) lower_right_index / (double) m_cols) == lower_row_index) ) {
                neuron_neighbors.push_back(lower_right_index);
            }
        }
    }
}


void som::create_initial_weights(const som_init_type type) {
    size_t dimension = (*m_data)[0].size();

    m_weights.resize(m_size, std::vector<double>(dimension, 0.0));

    std::vector<double> maximum_value_dimension(dimension, -std::numeric_limits<double>::max());
    std::vector<double> minimum_value_dimension(dimension, std::numeric_limits<double>::max());

    for (size_t i = 0; i < m_data->size(); i++) {
        for (size_t dim = 0; dim < dimension; dim++) {
            if (maximum_value_dimension[dim] < (*m_data)[i][dim]) {
                maximum_value_dimension[dim] = (*m_data)[i][dim];
            }

            if (minimum_value_dimension[dim] > (*m_data)[i][dim]) {
                minimum_value_dimension[dim] = (*m_data)[i][dim];
            }
        }
    }

    std::vector<double> width_value_dimension(dimension, 0);
    std::vector<double> center_value_dimension(dimension, 0);

    for (size_t dim = 0; dim < dimension; dim++) {
        width_value_dimension[dim] = maximum_value_dimension[dim] - minimum_value_dimension[dim];
        center_value_dimension[dim] = (maximum_value_dimension[dim] + minimum_value_dimension[dim]) / 2.0;
    }

    double step_x = center_value_dimension[0];
    double step_y = 0.0;
    if (dimension > 1) {
        step_y = center_value_dimension[1];
        if (m_cols > 1) { step_y = width_value_dimension[1] / (m_cols - 1.0); }
    }

    if (m_rows > 1) { step_x = width_value_dimension[0] / (m_rows - 1.0); }

    /* generate weights (topological coordinates) */
    std::random_device device;
    std::default_random_engine generator(device());

    generator.seed(static_cast<unsigned int>(std::chrono::system_clock::now().time_since_epoch().count()));

    switch (type) {
        /* Feature SOM 0002: Uniform grid. */
        case som_init_type::SOM_UNIFORM_GRID: {
            for (size_t i = 0; i < m_size; i++) {
                std::vector<double> & neuron_location = m_location[i];
                std::vector<double> & neuron_weight = m_weights[i];

                for (size_t dim = 0; dim < dimension; dim++) {
                    if (dim == 0) {
                        if (m_rows > 1) {
                            neuron_weight[dim] = minimum_value_dimension[dim] + step_x * neuron_location[dim];
                        }
                        else {
                            neuron_weight[dim] = center_value_dimension[dim];
                        }
                    }
                    else if (dim == 1) {
                        if (m_cols > 1) {
                            neuron_weight[dim] = minimum_value_dimension[dim] + step_y * neuron_location[dim];
                        }
                        else {
                            neuron_weight[dim] = center_value_dimension[dim];
                        }
                    }
                    else {
                        neuron_weight[dim] = center_value_dimension[dim];
                    }
                }
            }

            break;
        }

        case som_init_type::SOM_RANDOM_SURFACE: {
            /* Random weights at the full surface. */
            for (size_t i = 0; i < m_size; i++) {
                std::vector<double> & neuron_weight = m_weights[i];

                for (size_t dim = 0; dim < dimension; dim++) {
                    std::uniform_real_distribution<double> position_distribution(minimum_value_dimension[dim], maximum_value_dimension[dim]);
                    neuron_weight[dim] = position_distribution(generator);
                }
            }

            break;
        }

        case som_init_type::SOM_RANDOM_CENTROID:
        case som_init_type::SOM_RANDOM: {
            /* Random weights of input data. */
            std::uniform_real_distribution<double> position_distribution(-0.5, 0.5);

            for (size_t i = 0; i < m_size; i++) {
                std::vector<double> & neuron_weight = m_weights[i];

                for (size_t dim = 0; dim < dimension; dim++) {
                    neuron_weight[dim] = position_distribution(generator);
                }
            }

            break;
        }
    }

    m_previous_weights = m_weights;
}


size_t som::competition(const pattern & input_pattern) const {
    size_t index = 0;
    double minimum = euclidean_distance_square(m_weights[0], input_pattern);

    for (size_t i = 1; i < m_size; i++) {
        double candidate = euclidean_distance_square(m_weights[i], input_pattern);
        if (candidate < minimum) {
            index = i;
            minimum = candidate;
        }
    }

    return index;
}


size_t som::adaptation(const size_t index_winner, const pattern & input_pattern) {
    size_t dimensions = m_weights[0].size();
    size_t number_adapted_neurons = 0;

    if (m_conn_type == som_conn_type::SOM_FUNC_NEIGHBOR) {
        for (size_t neuron_index = 0; neuron_index < m_size; neuron_index++) {
            double distance = m_sqrt_distances[index_winner][neuron_index];

            if (distance < m_local_radius) {
                double influence = std::exp( -( distance / (2.0 * m_local_radius) ) );

                std::vector<double> & neuron_weight = m_weights[neuron_index];
                for (size_t dim = 0; dim < dimensions; dim++) {
                    neuron_weight[dim] += m_learn_rate * influence * (input_pattern[dim] - m_weights[neuron_index][dim]);
                }

                number_adapted_neurons++;
            }
        }
    }
    else {
        std::vector<double> & neuron_winner_weight = m_weights[index_winner];
        for (size_t dim = 0; dim < dimensions; dim++) {
            neuron_winner_weight[dim] += m_learn_rate * (input_pattern[dim] - neuron_winner_weight[dim] );
        }

        std::vector<size_t> & winner_neighbors = m_neighbors[index_winner];
        for (auto & neighbor_index : winner_neighbors) {
            double distance = m_sqrt_distances[index_winner][neighbor_index];

            if (distance < m_local_radius) {
                double influence = std::exp( -( distance / (2.0 * m_local_radius) ) );

                std::vector<double> & neighbor_weight = m_weights[neighbor_index];
                for (size_t dim = 0; dim < dimensions; dim++) {
                    neighbor_weight[dim] += m_learn_rate * influence * (input_pattern[dim] - neighbor_weight[dim]);
                }

                number_adapted_neurons++;
            }
        }
    }

    return number_adapted_neurons;
}


size_t som::train(const dataset & input_data, const size_t num_epochs, bool autostop) {
    for (size_t i = 0; i < m_capture_objects.size(); i++) {
        m_capture_objects[i].clear();
        m_awards[i] = 0;
    }

    /* number of epouch */
    m_epouchs = num_epochs;

    /* store pointer to data (we are not owners, we don't need them after training) */
    m_data = &input_data;

    /* create weights */
    create_initial_weights(m_params.init_type);

    size_t epouch = 1;
    for ( ; epouch < (m_epouchs + 1); epouch++) {
        /* Depression term of coupling */
        m_local_radius = std::pow( ( m_params.init_radius * std::exp(-( (double) epouch / (double) m_epouchs)) ), 2);
        m_learn_rate = m_params.init_learn_rate * std::exp(-( (double) epouch / (double) m_epouchs));

        /* Feature SOM 0003: Clear statistics */
        if (autostop == true) {
            for (size_t i = 0; i < m_size; i++) {
                m_awards[i] = 0;
                m_capture_objects[i].clear();
            }
        }

        for (size_t i = 0; i < m_data->size(); i++) {
            /* Step 1: Competition */
            size_t index_winner = competition((*m_data)[i]);

            /* Step 2: Adaptation */
            adaptation(index_winner, (*m_data)[i]);

            /* Update statistics */
            if ( (autostop == true) || (epouch == m_epouchs) ) {
                m_awards[index_winner]++;
                m_capture_objects[index_winner].push_back(i);
            }
        }

        /* Feature SOM 0003: Check requirement of stopping */
        if (autostop == true) {
            double maximal_adaptation = calculate_maximal_adaptation();
            if (maximal_adaptation < m_params.adaptation_threshold) {
                return epouch;
            }

            for (size_t i = 0; i < m_weights.size(); i++) {
                std::copy(m_weights[i].begin(), m_weights[i].end(), m_previous_weights[i].begin());
            }
        }
    }

    return epouch;
}


void som::load(const dataset & p_weights, const som_award_sequence & p_awards, const som_gain_sequence & p_capture_objects) {
    if (p_weights.size() != m_size) {
        throw std::invalid_argument("Provided weights (" + std::to_string(p_weights.size()) + 
          ") for loading does not correspond to network size (" + std::to_string(m_size) + ").");
    }

    m_weights = p_weights;

    if (!p_capture_objects.empty()) {
        if (p_capture_objects.size() != m_size) {
            throw std::invalid_argument("Provided capture objects (size '" + std::to_string(p_capture_objects.size()) + 
              "') for loading does not correspond to network size '" + std::to_string(m_size) + "'.");
        }

        m_capture_objects = p_capture_objects;
    }

    if (!p_awards.empty()) {
        if (p_awards.size() != m_size) {
            throw std::invalid_argument("Provided amount of capture objects by each neuron (size '" + std::to_string(p_awards.size()) +
              "') for loading does not correspond to network size '" + std::to_string(m_size) + "'.");
        }

        m_awards = p_awards;
    }
}


size_t som::simulate(const pattern & input_pattern) const {
    return competition(input_pattern);
}


double som::calculate_maximal_adaptation() const {
    size_t dimensions = (*m_data)[0].size();
    double maximal_adaptation = 0;

    for (size_t neuron_index = 0; neuron_index < m_size; neuron_index++) {
        const std::vector<double> & neuron_weight = m_weights[neuron_index];
        const std::vector<double> & previous_neuron_weight = m_previous_weights[neuron_index];

        for (size_t dim = 0; dim < dimensions; dim++) {
            double current_adaptation = previous_neuron_weight[dim] - neuron_weight[dim];

            if (current_adaptation < 0) { current_adaptation = -current_adaptation; }

            if (maximal_adaptation < current_adaptation) {
                maximal_adaptation = current_adaptation;
            }
        }
    }

    return maximal_adaptation;
}


std::size_t som::get_winner_number() const {
    std::size_t winner_number = 0;
    for (std::size_t i = 0; i < m_size; i++) {
        if (m_awards[i] > 0) {
            winner_number++;
        }
    }

    return winner_number;
}


double som::calculate_init_radius(const size_t p_rows, const size_t p_cols) {
    if ((double)(p_cols + p_rows) / 4.0 > 1.0) {
        return 2.0;
    }
    else if ((p_cols > 1) && (p_rows > 1)) {
        return 1.5;
    }
    else {
        return 1.0;
    }
}


std::ostream & operator<<(std::ostream & p_stream, const som & p_network) {
    p_stream << p_network.m_rows << "\n";
    p_stream << p_network.m_cols << "\n";
    p_stream << (unsigned) p_network.m_conn_type << "\n";
    p_stream << pyclustering::to_string(p_network.m_weights) << "\n";
    p_stream << pyclustering::to_string(p_network.m_awards) << "\n";
    p_stream << pyclustering::to_string(p_network.m_location) << "\n";
    p_stream << pyclustering::to_string(p_network.m_capture_objects) << "\n";
    p_stream << pyclustering::to_string(p_network.m_neighbors) << "\n";

    return p_stream;
}


som & som::operator=(const som & p_other) {
    if (&p_other == this) {
        return *this;
    }

    m_rows = p_other.m_rows;
    m_cols = p_other.m_cols;
    m_size = p_other.m_size;

    m_conn_type = p_other.m_conn_type;

    m_weights = p_other.m_weights;
    m_previous_weights = p_other.m_previous_weights;
    m_awards = p_other.m_awards;

    m_location = p_other.m_location;
    m_sqrt_distances = p_other.m_sqrt_distances;
    m_capture_objects = p_other.m_capture_objects;
    m_neighbors = p_other.m_neighbors;

    m_epouchs = p_other.m_epouchs;
    m_params = p_other.m_params;

    m_local_radius = p_other.m_local_radius;
    m_learn_rate = p_other.m_learn_rate;

    return *this;
}


}

}
