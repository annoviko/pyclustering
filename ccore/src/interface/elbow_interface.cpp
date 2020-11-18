/*!

@authors Andrei Novikov (pyclustering@yandex.ru)
@date 2014-2020
@copyright BSD-3-Clause

*/


#include <pyclustering/interface/elbow_interface.h>


pyclustering_package * elbow_method_ikpp(const pyclustering_package * const p_sample,
                                         const std::size_t p_kmin,
                                         const std::size_t p_kmax,
                                         const std::size_t p_kstep,
                                         const long long p_random_state) try
{
    return elbow_method<pyclustering::clst::kmeans_plus_plus>(p_sample, p_kmin, p_kmax, p_kstep, p_random_state);
}
catch (std::exception & p_exception) {
    return create_package(p_exception.what());
}


pyclustering_package * elbow_method_irnd(const pyclustering_package * const p_sample, 
                                         const std::size_t p_kmin, 
                                         const std::size_t p_kmax,
                                         const std::size_t p_kstep,
                                         const long long p_random_state) try
{
    return elbow_method<pyclustering::clst::random_center_initializer>(p_sample, p_kmin, p_kmax, p_kstep, p_random_state);
}
catch (std::exception & p_exception) {
    return create_package(p_exception.what());
}