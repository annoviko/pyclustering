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

#pragma once


#include <algorithm>
#include <list>
#include <set>
#include <vector>

#include <pyclustering/container/kdtree.hpp>

#include <pyclustering/cluster/cluster_algorithm.hpp>
#include <pyclustering/cluster/cure_data.hpp>


using namespace pyclustering::container;


namespace pyclustering {

namespace clst {


/**
*
* @brief   Cure cluster description.
*
*/
struct cure_cluster {
public:
    std::vector<double> * mean;
    std::vector< std::vector<double> * > * points;
    std::vector< std::vector<double> * > * rep;

    cure_cluster *          closest;
    double                  distance_closest;

public:
    /**
    *
    * @brief   Default constructor of cure cluster.
    *
    */
    cure_cluster();

    /**
    *
    * @brief   Default constructor of cure cluster that corresponds to specified point.
    *
    */
    explicit cure_cluster(std::vector<double> * point);

    /**
    *
    * @brief   Default destructor.
    *
    */
    ~cure_cluster();

    /**
    *
    * @brief   Default copy constructor.
    *
    */
    cure_cluster(const cure_cluster & p_other) = delete;

    /**
    *
    * @brief   Insert points to cluster.
    *
    */
    void insert_points(std::vector<std::vector<double> *> * append_points);

public:
    cure_cluster & operator=(const cure_cluster & p_other) = delete;

    friend std::ostream & operator<<(std::ostream & p_stream, cure_cluster & p_cluster);
};



/**
*
* @brief   Cluster comparator for set where pointers are stored.
*
*/
class cure_cluster_comparator {
public:
    /**
    *
    * @brief   Defines compare procedure using closest distance without checking for nullptr.
    *
    * @param[in] obj1: pointer to left operand (cluster 1).
    * @param[in] obj2: pointer to right operand (cluster 2).
    *
    * @return  Returns 'true' if left operand is less than right.
    *
    */
    bool operator()(const cure_cluster * const obj1, const cure_cluster * const obj2) const;
};



/**
*
* @brief   Cure sorted queue of cure clusters. Sorting is defined by distances between clusters.
*          First element is always occupied by cluster whose distance to the neighbor cluster
*          is the smallest in the queue.
*
*/
class cure_queue {
private:
    std::multiset<cure_cluster *, cure_cluster_comparator> * queue;
    kdtree * tree;

private:
    /**
    *
    * @brief   Creates sorted queue of points for specified data.
    *
    * @param[in] data: pointer to points.
    *
    */
    void create_queue(const dataset * data);

    /**
    *
    * @brief   Remove representative points of specified cluster from KD Tree.
    *
    * @param[in] cluster: pointer to points.
    *
    */
    void remove_representative_points(cure_cluster * cluster);

    /**
    *
    * @brief   Insert representative points of specified cluster to KD tree.
    *
    * @param[in] cluster: pointer to points.
    *
    */
    void insert_representative_points(cure_cluster * cluster);

    /**
    *
    * @brief   Insert cluster to sorted queue (it's not insertion of new object).
    * @details Used by sorting procedures.
    *
    * @param[in] inserted_cluster: pointer to points.
    *
    */
    void insert_cluster(cure_cluster * inserted_cluster);

    /**
    *
    * @brief   Remove cluster from sorted queue (it's not removing of new object). Used by sorting
    *          procedures.
    *
    * @param[in] removed_cluster: pointer to points.
    *
    */
    void remove_cluster(cure_cluster * removed_cluster);

    /**
    *
    * @brief   Calculate distance between clusters.
    *
    * @param[in] cluster1: pointer to cure cluster 1.
    * @param[in] cluster2: pointer to cure cluster 2.
    *
    * @return  Return distance between clusters.
    *
    */
    static double get_distance(cure_cluster * cluster1, cure_cluster * cluster2);

    /**
    *
    * @brief   Checks if all elements of a merged cluster are same.
    *
    * @param[in] merged_cluster: pointer to cure merged_cluster.
    *
    * @return  Returns true if all the elements in the cluster were found to be same.
    *
    */
    static bool are_all_elements_same(cure_cluster * merged_cluster);

public:
    using iterator        = std::multiset<cure_cluster *, cure_cluster_comparator>::iterator;
    using const_iterator  = std::multiset<cure_cluster *, cure_cluster_comparator>::const_iterator;

    /**
    *
    * @brief   Default constructor of cure queue (always keeps sorted state).
    *
    */
    cure_queue();

    /**
    *
    * @brief   Default constructor of sorted queue of cure clusters.
    *
    * @param[in] data: pointer to points.
    *
    */
    explicit cure_queue(const std::vector< std::vector<double> > * data);

    /**
    *
    * @brief   Default copy constructor of sorted queue of cure clusters is forbidden.
    *
    * @param[in] p_other: other cure queue to copy.
    *
    */
    cure_queue(const cure_queue & p_other) = delete;

    /**
    *
    * @brief   Default destructor.
    *
    */
    ~cure_queue();

    /**
    *
    * @brief   Merge cure clusters in line with the rule of merging of cure algorithm.
    *
    * @param[in|out] cluster1: pointer to cure cluster 1.
    * @param[in|out] cluster2: pointer to cure cluster 2.
    * @param[in] number_repr_points: number of representative points for merged cluster.
    * @param[in] compression: level of compression for calculation representative points.
    *
    */
    void merge(cure_cluster * cluster1, cure_cluster * cluster2, const size_t number_repr_points, const double compression);

    /**
    *
    * @brief   Returns iterator to the first CURE cluster.
    *
    */
    inline iterator begin() { return queue->begin(); }

    /**
    *
    * @brief   Returns constant iterator to the first CURE cluster.
    *
    */
    inline const_iterator begin() const { return queue->begin(); };

    /**
    *
    * @brief   Returns iterator to the end of CURE cluster collection (not a last element).
    *
    */
    inline iterator end() { return queue->end(); }

    /**
    *
    * @brief   Returns constant iterator to the end of CURE cluster collection (not a last element).
    *
    */
    inline const_iterator end() const { return queue->end(); }

    /**
    *
    * @brief   Returns amount of CURE clusters in the queue.
    *
    */
    inline size_t size() const { return queue->size(); }

public:
    /**
    *
    * @brief   Copy assignment operator is forbidden.
    *
    * @param[in] p_other: other cure queue to copy.
    *
    */
    cure_queue & operator=(const cure_queue & p_other) = delete;
};



class relocation_info {
private:
    cure_queue::iterator m_cluster_iterator;
    cure_cluster * m_closest_cluster;
    double m_closest_distance;

public:
    relocation_info(const cure_queue::iterator & cluster_iterator, cure_cluster * closest_cluster, const double closest_distance);

public:
    cure_queue::iterator get_cluster_iterator() const;

    double get_closest_distance() const;

    cure_cluster * get_closest_cluster();
};



/**
*
* @brief   CURE algorithm.
*
*/
class cure : public cluster_algorithm {
private:
    cure_queue * queue;

    size_t number_points;

    size_t number_clusters;

    double compression;

    const dataset   * data;

public:
    /**
    *
    * @brief   Default constructor.
    *
    */
    cure() = default;

    /**
    *
    * @brief   Constructor of CURE solver (algorithm representer).
    *
    * @param[in] clusters_number: number of clusters that should be allocated.
    * @param[in] points_number: number of representative points in each cluster.
    * @param[in] level_compression: level of compression for calculation new representative points for merged cluster.
    *
    */
    cure(const size_t clusters_number, const size_t points_number, const double level_compression);

    /**
    *
    * @brief   Default destructor.
    *
    */
    virtual ~cure();

public:
    /**
    *
    * @brief    Performs cluster analysis of an input data.
    *
    * @param[in]  p_data: input data for cluster analysis.
    * @param[out] p_result: clustering result of an input data.
    *
    */
    virtual void process(const dataset & p_data, cluster_data & p_result) override;
};


}

}