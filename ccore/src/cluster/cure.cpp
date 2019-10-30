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


#include <limits>
#include <set>
#include <iostream>

#include <pyclustering/cluster/cure.hpp>

#include <pyclustering/utils/metric.hpp>


using namespace pyclustering::container;
using namespace pyclustering::utils::metric;


namespace pyclustering {

namespace clst {


cure_cluster::cure_cluster() : mean(nullptr), closest(nullptr), distance_closest(0) {
    points = new std::vector< std::vector<double> * >();
    rep = new std::vector< std::vector<double> * >();
}


cure_cluster::cure_cluster(std::vector<double> * point) : closest(nullptr), distance_closest(0) {
    mean = new std::vector<double>(*point);

    points = new std::vector< std::vector<double> * >(1, point);    /* use user data points */
    rep = new std::vector< std::vector<double> * >(1, new std::vector<double>(*point));       /* it's our - despite at the beginning it the same */
}


cure_cluster::~cure_cluster() {
    if (mean != nullptr) {
        delete mean;
        mean = nullptr;
    }

    delete points;  /* only storage, we are not owners of points */
    points = nullptr;

    for (auto point_ptr : *rep) {
        delete point_ptr;
    }

    delete rep;     /* only storage, we are not owners of points */
    rep = nullptr;
}


void cure_cluster::insert_points(std::vector<std::vector<double> *> * append_points) {
    points->insert(points->end(), append_points->begin(), append_points->end());
}


std::ostream & operator<<(std::ostream & p_stream, cure_cluster & p_cluster) {
    p_stream << p_cluster.distance_closest << "[";
    for (auto & point : *(p_cluster.points)) {
        p_stream << "[ ";
        for (auto & coordinate : *point) {
            p_stream << coordinate << " ";
        }
        p_stream << "]";
    }
    p_stream << "]";
    return p_stream;
}



bool cure_cluster_comparator::operator()(const cure_cluster * const obj1, const cure_cluster * const obj2) const {
    return obj1->distance_closest < obj2->distance_closest;
}



cure_queue::cure_queue() {
    queue = new std::multiset<cure_cluster *, cure_cluster_comparator>();
    tree = new kdtree();
}


cure_queue::cure_queue(const std::vector< std::vector<double> > * data) {
    queue = new std::multiset<cure_cluster *, cure_cluster_comparator>();
    create_queue(data);

    tree = new kdtree();

    for (auto cluster : *queue) {
        for (auto point : *(cluster->rep)) {
            tree->insert(*point, cluster);
        }
    }
}


cure_queue::~cure_queue() {
    if (queue != nullptr) {
        for (auto cluster : *queue) {
            delete cluster;
        }

        delete queue;
        queue = nullptr;
    }

    if (tree != nullptr) {
        delete tree;
        tree = nullptr;
    }
}


void cure_queue::create_queue(const dataset * data) {
    std::list<cure_cluster *> temporary_storage;

    for (auto & data_point : (*data)) {
        cure_cluster * cluster = new cure_cluster((std::vector<double> *) &data_point);
        temporary_storage.push_back(cluster);
    }

    for (auto & first_cluster : temporary_storage) {
        double minimal_distance = std::numeric_limits<double>::max();
        cure_cluster * closest_cluster = nullptr;

        for (auto & second_cluster : temporary_storage) {
            if (first_cluster != second_cluster) {
                double dist = get_distance(first_cluster, second_cluster);
                if (dist < minimal_distance) {
                    minimal_distance = dist;
                    closest_cluster = second_cluster;
                }
            }
        }

        first_cluster->closest = closest_cluster;
        first_cluster->distance_closest = minimal_distance;
    }

    for (const auto & cluster : temporary_storage) {
        queue->insert(cluster);
    }
}


double cure_queue::get_distance(cure_cluster * cluster1, cure_cluster * cluster2) {
    double distance = std::numeric_limits<double>::max();
    for (auto & point1 : *(cluster1->rep)) {
        for (auto & point2 : *(cluster2->rep)) {
            double candidate_distance = euclidean_distance_square(*point1, *point2);
            if (candidate_distance < distance) {
                distance = candidate_distance;
            }
        }
    }

    return distance;
}


bool cure_queue::are_all_elements_same(cure_cluster * merged_cluster) {
    auto & data_points = *(merged_cluster->points);
    auto & first_point = data_points.front();

    for (std::size_t i = 1; i < data_points.size(); i++) {
        if (data_points[i] != first_point) {
          return false;
        }
    }

    return true;
}


void cure_queue::merge(cure_cluster * cluster1, cure_cluster * cluster2, const size_t number_repr_points, const double compression) {
    remove_representative_points(cluster1);
    remove_representative_points(cluster2);

    remove_cluster(cluster1);
    remove_cluster(cluster2);

    cure_cluster * merged_cluster = new cure_cluster();
    merged_cluster->insert_points(cluster1->points);
    merged_cluster->insert_points(cluster2->points);

    merged_cluster->mean = new std::vector<double>((*cluster1->points)[0]->size(), 0);

    //If all elements were same then avoid calculating the mean mathematically as it may lead to precision error.
    if (are_all_elements_same(merged_cluster)) {
        for (std::size_t i = 0; i < (*merged_cluster->points)[0]->size(); i++) {
            (*merged_cluster->mean)[i] = (*(*merged_cluster->points)[0])[i];
        }

    }
    else {
        for (std::size_t dimension = 0; dimension < merged_cluster->mean->size(); dimension++) {
            (*merged_cluster->mean)[dimension] = (cluster1->points->size() * (*cluster1->mean)[dimension] + cluster2->points->size() * (*cluster2->mean)[dimension]) / (cluster1->points->size() + cluster2->points->size());
        }
    }

    std::set<std::vector<double> *> * temporary = new std::set<std::vector<double> *>();

    for (std::size_t index = 0; index < number_repr_points; index++) {
        double maximal_distance = 0;
        std::vector<double> * maximal_point = nullptr;

        for (auto & point : *(merged_cluster->points)) {
            double minimal_distance = 0;
            if (index == 0) {
                minimal_distance = euclidean_distance_square(*point, *(merged_cluster->mean));
            }
            else {
                double temp_minimal_distance = std::numeric_limits<double>::max();
                for (auto p : (*temporary)) {
                    double minimal_candidate = euclidean_distance_square(*point, *p);
                    if (minimal_candidate < temp_minimal_distance) {
                        temp_minimal_distance = minimal_candidate;
                    }
                }

                minimal_distance = temp_minimal_distance;
            }

            if (minimal_distance >= maximal_distance) {
                maximal_distance = minimal_distance;
                maximal_point = point;
            }
        }

        if (temporary->find(maximal_point) == temporary->end()) {
            temporary->insert(maximal_point);
        }
    }

    for (auto & point : *temporary) {
        std::vector<double> * representative_point = new std::vector<double>(point->size(), 0);
        for (std::size_t index = 0; index < point->size(); index++) {
            (*representative_point)[index] = (*point)[index] + compression * ( (*merged_cluster->mean)[index] - (*point)[index] );
        }

        merged_cluster->rep->push_back(representative_point);
    }

    delete temporary;
    temporary = nullptr;

    insert_representative_points(merged_cluster);

    std::list<relocation_info> relocation_request;

    if (!queue->empty()) {
        merged_cluster->closest = *(queue->begin());
        merged_cluster->distance_closest = get_distance(merged_cluster, merged_cluster->closest);

        /* relocation request */
        for (auto iterator_cluster = queue->begin(); iterator_cluster != queue->end(); iterator_cluster++) {
            auto cluster = *iterator_cluster;

            const double distance = get_distance(merged_cluster, cluster);
            const double real_euclidean_distance = std::sqrt(distance);

            /* Check if distance between new cluster and current is the best than now. */
            if (distance < merged_cluster->distance_closest) {
                merged_cluster->closest = cluster;
                merged_cluster->distance_closest = distance;
            }

            /* Check if current cluster has removed neighbor. */
            if ( (cluster->closest == cluster1) || (cluster->closest == cluster2) ) {
                /* If previous distance was less then distance to new cluster then nearest cluster should be found in the tree. */
                if (cluster->distance_closest < distance) {
                    cure_cluster * nearest_cluster = nullptr;
                    double nearest_distance = std::numeric_limits<double>::max();

                    for (auto & point : *(cluster->rep)) {
                        /* we are using Eucliean Square metric, but kdtree searcher requires common Eucliean distance (but output results are square) */
                        kdtree_searcher searcher(*point, tree->get_root(), real_euclidean_distance);

                        std::vector<double> nearest_node_distances;
                        std::vector<kdnode::ptr> nearest_nodes;
                        searcher.find_nearest_nodes(nearest_node_distances, nearest_nodes);

                        for (std::size_t index = 0; index < nearest_nodes.size(); index++) {
                            if ( (nearest_node_distances[index] < nearest_distance) && ( nearest_nodes[index]->get_payload() != cluster ) ) {
                                nearest_distance = nearest_node_distances[index];
                                nearest_cluster = static_cast<cure_cluster *>(nearest_nodes[index]->get_payload());
                            }
                        }
                    }

                    if (nearest_cluster == nullptr) {
                        relocation_request.emplace_back(iterator_cluster, merged_cluster, distance);
                    }
                    else {
                        relocation_request.emplace_back(iterator_cluster, nearest_cluster, nearest_distance);
                    }
                }
                else {
                    relocation_request.emplace_back(iterator_cluster, merged_cluster, distance);
                }
            }
        }
    }

    delete cluster1; cluster1 = nullptr;
    delete cluster2; cluster2 = nullptr;

    /* insert merged cluster */
    insert_cluster(merged_cluster);

    /* relocate requested clusters */
    if (!relocation_request.empty()) {
        for (auto & info : relocation_request) {
            auto cluster = *(info.get_cluster_iterator());
            queue->erase(info.get_cluster_iterator());

            cluster->closest = info.get_closest_cluster();
            cluster->distance_closest = info.get_closest_distance();
            insert_cluster(cluster);
        }
    }
}


void cure_queue::insert_cluster(cure_cluster * inserted_cluster) {
    queue->insert(inserted_cluster);
}


void cure_queue::remove_cluster(cure_cluster * removed_cluster) {
    auto range = queue->equal_range(removed_cluster);
    for (auto iter = range.first; iter != range.second; iter++) {
        if (*iter == removed_cluster) {
            queue->erase(iter);
            return;
        }
    }

    throw std::runtime_error("CURE queue corruption detected, impossible to remove cluster from the queue. Please report to 'pyclustering@yandex.ru'.");
}


void cure_queue::remove_representative_points(cure_cluster * cluster) {
    for (auto & point : *(cluster->rep)) {
        tree->remove(*point, (void *) cluster);
    }
}


void cure_queue::insert_representative_points(cure_cluster * cluster) {
    for (auto & point : *(cluster->rep)) {
        tree->insert(*point, cluster);
    }
}



relocation_info::relocation_info(const cure_queue::iterator & cluster_iterator, cure_cluster * closest_cluster, const double closest_distance) :
    m_cluster_iterator(cluster_iterator),
    m_closest_cluster(closest_cluster),
    m_closest_distance(closest_distance)
{ }


cure_queue::iterator relocation_info::get_cluster_iterator() const {
    return m_cluster_iterator; 
}


cure_cluster * relocation_info::get_closest_cluster() {
    return m_closest_cluster;
}


double relocation_info::get_closest_distance() const {
    return m_closest_distance;
}



cure::cure(const size_t clusters_number, size_t points_number, const double level_compression) :
    queue(nullptr),
    number_points(points_number),
    number_clusters(clusters_number),
    compression(level_compression),
    data(nullptr)
{ }


cure::~cure() {
    delete queue;
}


void cure::process(const dataset & p_data, cluster_data & p_result) {
    delete queue;

    queue = new cure_queue(&p_data);
    data = &p_data;

    std::size_t allocated_clusters = queue->size();
    while(allocated_clusters > number_clusters) {
        cure_cluster * cluster1 = *(queue->begin());
        cure_cluster * cluster2 = cluster1->closest;

        /* merge new cluster using these clusters */
        queue->merge(cluster1, cluster2, number_points, compression);

        allocated_clusters = queue->size();
    }

    p_result = cure_data();
    cure_data & result = (cure_data &) p_result;

    /* prepare standard representation of clusters */
    cluster_sequence & clusters = result.clusters();
    representor_sequence & representors = result.representors();

    clusters.resize(queue->size());
    representors.resize(queue->size());

    size_t cluster_index = 0;
    for (auto cure_cluster = queue->begin(); cure_cluster != queue->end(); ++cure_cluster, cluster_index++) {
        cluster & standard_cluster = clusters[cluster_index];
        for (auto point = (*cure_cluster)->points->begin(); point != (*cure_cluster)->points->end(); ++point) {
            size_t index_point = (size_t) (*point - &(*(data->begin())));
            standard_cluster.push_back(index_point);
        }

        dataset & cluster_representors = representors[cluster_index];
        for (auto point : *(*cure_cluster)->rep) {
            cluster_representors.push_back(*point);
        }

        result.means().push_back((*(*cure_cluster)->mean));
    }

    p_result = result;

    delete queue;
    queue = nullptr;
}


}

}
