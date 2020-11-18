/*!

@authors Andrei Novikov (pyclustering@yandex.ru)
@date 2014-2020
@copyright BSD-3-Clause

*/
#pragma once


#include <vector>


using cluster = std::vector<std::size_t>;
using cluster_sequence = std::vector<cluster>;

using length_sequence = std::vector<std::size_t>;


class answer {
private:
    cluster_sequence m_clusters;
    length_sequence  m_cluster_lengths;
    cluster          m_noise;

public:
    const cluster_sequence & clusters() const { return m_clusters; }

    cluster_sequence & clusters() { return m_clusters; }

    const length_sequence & cluster_lengths() const { return m_cluster_lengths; }

    length_sequence & cluster_lengths() { return m_cluster_lengths; }

    const cluster & noise() const { return m_noise; }

    cluster & noise() { return m_noise; }
};