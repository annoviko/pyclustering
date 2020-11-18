/*!

@authors Andrei Novikov (pyclustering@yandex.ru)
@date 2014-2020
@copyright BSD-3-Clause

*/


#include <pyclustering/interface/metric_interface.h>

#include <pyclustering/utils/metric.hpp>


using namespace pyclustering;
using namespace pyclustering::utils::metric;


void * metric_create(const std::size_t p_type,
                     const pyclustering_package * const p_arguments,
                     double (*p_solver)(const void *, const void *))
{
    switch(p_type) {
        case EUCLIDEAN: {
            distance_metric<point> metric = distance_metric_factory<point>::euclidean();
            return new distance_metric<point>(std::move(metric));

        }

        case EUCLIDEAN_SQUARE: {
            distance_metric<point> metric = distance_metric_factory<point>::euclidean_square();
            return new distance_metric<point>(std::move(metric));
        }

        case MANHATTAN: {
            distance_metric<point> metric = distance_metric_factory<point>::manhattan();
            return new distance_metric<point>(std::move(metric));
        }

        case CHEBYSHEV: {
            distance_metric<point> metric = distance_metric_factory<point>::chebyshev();
            return new distance_metric<point>(std::move(metric));
        }

        case MINKOWSKI: {
            std::vector<double> arguments;
            p_arguments->extract(arguments);

            distance_metric<point> metric = distance_metric_factory<point>::minkowski(arguments[0]);
            return new distance_metric<point>(std::move(metric));
        }

        case CANBERRA: {
            distance_metric<point> metric = distance_metric_factory<point>::canberra();
            return new distance_metric<point>(std::move(metric));
        }

        case CHI_SQUARE: {
            distance_metric<point> metric = distance_metric_factory<point>::chi_square();
            return new distance_metric<point>(std::move(metric));
        }

        case GOWER: {
            point max_range;
            p_arguments->extract(max_range);

            distance_metric<point> metric = distance_metric_factory<point>::gower(max_range);
            return new distance_metric<point>(std::move(metric));
        }

        case USER_DEFINED: {
            auto functor_wrapper = [p_solver](const point & p1, const point & p2) {
                pyclustering_package * point1 = create_package(&p1);
                pyclustering_package * point2 = create_package(&p2);

                const double distance = p_solver(point1, point2);

                delete point1;
                delete point2;

                return distance;
            };

            distance_metric<point> metric = distance_metric_factory<point>::user_defined(functor_wrapper);
            return new distance_metric<point>(std::move(metric));
        }

        default:
            return nullptr;
    }
}


void metric_destroy(const void * p_pointer_metric) {
    delete (distance_metric<point> *) p_pointer_metric;
}


double metric_calculate(const void * p_pointer_metric,
                        const pyclustering_package * const p_point1,
                        const pyclustering_package * const p_point2)
{
    point point1, point2;
    p_point1->extract(point1);
    p_point2->extract(point2);

    distance_metric<point> & metric = *((distance_metric<point> *) p_pointer_metric);
    return metric(point1, point2);
}
