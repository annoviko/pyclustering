/*!

@authors Andrei Novikov (pyclustering@yandex.ru)
@date 2014-2020
@copyright BSD-3-Clause

*/


#include <pyclustering/cluster/pam_build.hpp>

#include <algorithm>
#include <numeric>
#include <unordered_set>


namespace pyclustering {

namespace clst {


pam_build::pam_build(const std::size_t p_amount) :
    m_amount(p_amount)
{ }


pam_build::pam_build(const std::size_t p_amount, const metric & p_metric) :
    m_amount(p_amount),
    m_metric(p_metric)
{ }


void pam_build::initialize(const dataset & p_data, const medoids & p_medoids) const {
    initialize(p_data, data_t::POINTS, p_medoids);
}


void pam_build::initialize(const dataset & p_data, const data_t p_type, const medoids & p_medoids) const {
    m_data_ptr = (dataset *) &p_data;
    m_medoids_ptr = (medoids *) &p_medoids;

    create_distance_calculator(p_type);
    m_distance_closest_medoid = std::vector<double>(p_data.size(), 0.0);

    calculate_first_medoid();
    calculate_next_medoids();
}


void pam_build::calculate_first_medoid() const {
    double optimal_deviation = std::numeric_limits<double>::max();
    std::size_t optimal_medoid = INVALID_MEDOID;

    std::vector<double> current_distances(m_data_ptr->size());

    for (std::size_t i = 0; i < m_data_ptr->size(); i++) {
        double total_deviation = 0.0;
        for (std::size_t j = 0; j != m_data_ptr->size(); j++) {
            if (i == j) {
                current_distances[j] = 0;
                continue;
            }

            const double distance = m_calculator(i, j);
            total_deviation += distance;
            current_distances[j] = distance;
        }

        if (total_deviation < optimal_deviation) {
            optimal_medoid = i;
            optimal_deviation = total_deviation;
            std::swap(m_distance_closest_medoid, current_distances);
        }
    }

    if (optimal_medoid == INVALID_MEDOID) {
        throw std::logic_error("Impossible to calculate the first medoid.");
    }

    m_medoids_ptr->push_back(optimal_medoid);
}


void pam_build::calculate_next_medoids() const {
    std::vector<double> optimal_distances(m_data_ptr->size(), 0.0);
    std::vector<double> current_distances(m_data_ptr->size(), 0.0);

    std::vector<bool>   medoids(m_data_ptr->size(), false);
    medoids[m_medoids_ptr->at(0)] = true;

    while (m_medoids_ptr->size() < m_amount) {
        std::size_t optimal_medoid = INVALID_MEDOID;
        double optimal_deviation = std::numeric_limits<double>::max();

        for (std::size_t i = 0; i < m_data_ptr->size(); ++i) {
            if (medoids[i]) {
                continue;   /* already assigned as a medoid */
            }

            double total_deviation = 0.0;
            for (std::size_t j = 0; j < m_data_ptr->size(); ++j) {
                if ((i == j) || (medoids[j])) {
                    current_distances[j] = 0;
                    continue;
                }

                current_distances[j] = std::min(m_calculator(i, j), m_distance_closest_medoid[j]);
                total_deviation += current_distances[j];
            }

            if (total_deviation < optimal_deviation) {
                optimal_medoid = i;
                optimal_deviation = total_deviation;
                std::swap(optimal_distances, current_distances);
            }
        }

        if (optimal_medoid == INVALID_MEDOID) {
            throw std::logic_error("Impossible to calculate the next medoid (medoid number: '" + std::to_string(m_medoids_ptr->size() + 1) + "').");
        }

        m_medoids_ptr->push_back(optimal_medoid);
        medoids[optimal_medoid] = true;
        std::swap(m_distance_closest_medoid, optimal_distances);
    }
}


double pam_build::calculate_distance_using_points(const std::size_t p_index1, const std::size_t p_index2) const {
    return m_metric((*m_data_ptr)[p_index1], (*m_data_ptr)[p_index2]);
}


double pam_build::calculate_distance_using_distance_matrix(const std::size_t p_index1, const std::size_t p_index2) const {
    return (*m_data_ptr)[p_index1][p_index2];
}


void pam_build::create_distance_calculator(const data_t p_type) const {
    if (p_type == data_t::POINTS) {
        m_calculator = std::bind(&pam_build::calculate_distance_using_points, this, std::placeholders::_1, std::placeholders::_2);
    }
    else if (p_type == data_t::DISTANCE_MATRIX) {
        m_calculator = std::bind(&pam_build::calculate_distance_using_distance_matrix, this, std::placeholders::_1, std::placeholders::_2);
    }
    else {
        throw std::invalid_argument("Unknown type data is specified (type code: '" + std::to_string(static_cast<std::size_t>(p_type)) + "').");
    }
}


}

}