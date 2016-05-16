#include "cluster/dbscan_data.hpp"


namespace cluster_analysis {


dbscan_data::dbscan_data(void) :
        cluster_data(),
        m_noise(new cluster_analysis::noise())
{ }


dbscan_data::dbscan_data(const dbscan_data & p_other) :
        cluster_data(p_other),
        m_noise(p_other.m_noise)
{ }


dbscan_data::dbscan_data(dbscan_data && p_other) :
        cluster_data(p_other),
        m_noise(std::move(p_other.m_noise))
{ }


dbscan_data::~dbscan_data(void) { }


noise_ptr dbscan_data::noise(void) { return m_noise; }


}
