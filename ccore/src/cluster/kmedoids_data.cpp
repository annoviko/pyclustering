#include "cluster/kmedoids_data.hpp"


namespace cluster_analysis {


kmedoids_data::kmedoids_data(void) :
        cluster_data(),
        m_medoids(new medoid_sequence())
{ }


kmedoids_data::kmedoids_data(const kmedoids_data & p_other) :
        cluster_data(p_other),
        m_medoids(p_other.m_medoids)
{ }


kmedoids_data::kmedoids_data(kmedoids_data && p_other) :
        cluster_data(p_other),
        m_medoids(std::move(p_other.m_medoids))
{ }


kmedoids_data::~kmedoids_data(void) { }


medoid_sequence_ptr kmedoids_data::medoids(void) { return m_medoids; }


}
