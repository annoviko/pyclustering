#include "cluster/kmedians_data.hpp"


namespace cluster_analysis {


kmedians_data::kmedians_data(void) :
        cluster_data(),
        m_medians(new dataset())
{ }


kmedians_data::kmedians_data(const kmedians_data & p_other) :
        cluster_data(p_other),
        m_medians(p_other.m_medians)
{ }


kmedians_data::kmedians_data(kmedians_data && p_other) :
        cluster_data(p_other),
        m_medians(std::move(p_other.m_medians))
{ }


kmedians_data::~kmedians_data(void) { }


dataset_ptr kmedians_data::medians(void) { return m_medians; }


}
