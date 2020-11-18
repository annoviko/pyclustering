/*!

@authors Andrei Novikov (pyclustering@yandex.ru)
@date 2014-2020
@copyright BSD-3-Clause

*/


#include <pyclustering/interface/silhouette_interface.h>


pyclustering::clst::silhouette_ksearch_allocator::ptr get_silhouette_ksearch_allocator(
    const silhouette_ksearch_type p_algorithm)
{
    switch(p_algorithm) {
      case silhouette_ksearch_type::KMEANS:
          return std::make_shared<pyclustering::clst::kmeans_allocator>();
      case silhouette_ksearch_type::KMEDIANS:
          return std::make_shared<pyclustering::clst::kmedians_allocator>();
      case silhouette_ksearch_type::KMEDOIDS:
          return std::make_shared<pyclustering::clst::kmedoids_allocator>();
      default:
          throw std::invalid_argument("Unknown allocator '" + std::to_string(static_cast<int>(p_algorithm)) + "' is specified.");
    }
}


pyclustering_package * silhouette_algorithm(
    const pyclustering_package * const p_sample,
    const pyclustering_package * const p_clusters,
    const void * const p_metric,
    const std::size_t p_data_type)
{
    pyclustering::dataset data;
    p_sample->extract(data);

    pyclustering::clst::cluster_sequence clusters;
    p_clusters->extract(clusters);

    distance_metric<pyclustering::point> * metric = ((distance_metric<pyclustering::point> *) p_metric);
    distance_metric<pyclustering::point> default_metric = distance_metric_factory<pyclustering::point>::euclidean_square();

    if (!metric) {
        metric = &default_metric;
    }

    pyclustering::clst::silhouette_data result;
    pyclustering::clst::silhouette(*metric).process(data, clusters, static_cast<pyclustering::clst::silhouette_data_t>(p_data_type), result);

    return create_package(&result.get_score());
}


pyclustering_package * silhouette_ksearch_algorithm(
    const pyclustering_package * const p_sample,
    const std::size_t p_kmin,
    const std::size_t p_kmax,
    const std::size_t p_algorithm,
    const long long p_random_state)
{
    pyclustering::dataset data;
    p_sample->extract(data);

    auto allocator = get_silhouette_ksearch_allocator(static_cast<silhouette_ksearch_type>(p_algorithm));

    pyclustering::clst::silhouette_ksearch_data result;
    pyclustering::clst::silhouette_ksearch(p_kmin, p_kmax, allocator, p_random_state).process(data, result);

    pyclustering_package * package = new pyclustering_package(pyclustering_data_t::PYCLUSTERING_TYPE_LIST);
    package->size = SILHOUETTE_KSEARCH_PACKAGE_SIZE;
    package->data = new pyclustering_package * [SILHOUETTE_KSEARCH_PACKAGE_SIZE];

    std::vector<std::size_t> amount_cluters = { result.get_amount() };
    std::vector<double> score = { result.get_score() };

    ((pyclustering_package **) package->data)[SILHOUETTE_KSEARCH_PACKAGE_AMOUNT]  = create_package(&amount_cluters);
    ((pyclustering_package **) package->data)[SILHOUETTE_KSEARCH_PACKAGE_SCORE]   = create_package(&score);
    ((pyclustering_package **) package->data)[SILHOUETTE_KSEARCH_PACKAGE_SCORES]  = create_package(&result.scores());

    return package;
}