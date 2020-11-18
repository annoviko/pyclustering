/*!

@authors Andrei Novikov (pyclustering@yandex.ru)
@date 2014-2020
@copyright BSD-3-Clause

*/

#include <pyclustering/cluster/somsc.hpp>


using namespace pyclustering::nnet;


namespace pyclustering {

namespace clst {


somsc::somsc(const std::size_t p_amount_clusters, const std::size_t p_epoch) :
        m_amount_clusters(p_amount_clusters),
        m_epoch(p_epoch)
{ }


void somsc::process(const dataset & p_data, somsc_data & p_result) {
    som_parameters params;
    som som_map(1, m_amount_clusters, som_conn_type::SOM_GRID_FOUR, params);
    som_map.train(p_data, m_epoch, true);

    p_result.clusters() = som_map.get_capture_objects();
}


}

}