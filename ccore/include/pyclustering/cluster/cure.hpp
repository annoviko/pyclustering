/*!

@authors Andrei Novikov (pyclustering@yandex.ru)
@date 2014-2020
@copyright BSD-3-Clause

*/

#pragma once


#include <algorithm>
#include <list>
#include <set>
#include <vector>

#include <pyclustering/container/kdtree.hpp>

#include <pyclustering/cluster/cure_data.hpp>


using namespace pyclustering::container;


namespace pyclustering {

namespace clst {


/*!

@class   cure_cluster cure.hpp pyclustering/cluster/cure.hpp

@brief   CURE cluster description.

*/
struct cure_cluster {
public:
    std::vector<double> * mean;                         /**< Center of the cluster that is defined by mean value among cluster points. */
    std::vector< std::vector<double> * > * points;      /**< Points that are contained by the cluster. */
    std::vector< std::vector<double> * > * rep;         /**< Representative points of the cluster. */

    cure_cluster *          closest;                    /**< Pointer to the closest cluster. */
    double                  distance_closest;           /**< Distance to the closest cluster. */

public:
    /*!
    
    @brief   Default constructor of CURE cluster.
    
    */
    cure_cluster();

    /*!
    
    @brief   Construct CURE cluster using signle point.
    
    */
    explicit cure_cluster(std::vector<double> * point);

    /*!
    
    @brief   Default destructor.
    
    */
    ~cure_cluster();

    /*!
    
    @brief   Copy constructor is deleted due to safety reasons.
    
    */
    cure_cluster(const cure_cluster & p_other) = delete;

public:
    /*!
    
    @brief   Insert points to cluster.
    
    */
    void insert_points(std::vector<std::vector<double> *> * append_points);

public:
    /*!

    @brief   Assignment operator is deleted due to safety reasons.

    */
    cure_cluster & operator=(const cure_cluster & p_other) = delete;

    /*!

    @brief   Write object operator to represent CURE cluster by text.

    */
    friend std::ostream & operator<<(std::ostream & p_stream, cure_cluster & p_cluster);
};



/*!

@class   cure_cluster_comparator cure.hpp pyclustering/cluster/cure.hpp

@brief   CURE cluster comparator using closest distance.

*/
class cure_cluster_comparator {
public:
    /*!
    
    @brief   Defines compare procedure using closest distance without checking for nullptr.
    @details Arguments are not checked for nullptr, this checking should be done by client code.
    
    @param[in] obj1: pointer to left operand (CURE cluster 1).
    @param[in] obj2: pointer to right operand (CURE cluster 2).
    
    @return  Returns `true` if left operand is less than right.
    
    */
    bool operator()(const cure_cluster * const obj1, const cure_cluster * const obj2) const;
};



/*!

@class   cure_queue cure.hpp pyclustering/cluster/cure.hpp

@brief   Cure sorted queue of cure clusters. Sorting is defined by distances between clusters.
          First element is always occupied by cluster whose distance to the neighbor cluster
          is the smallest in the queue.

*/
class cure_queue {
private:
    std::multiset<cure_cluster *, cure_cluster_comparator> * queue;
    kdtree * tree;

private:
    /*!
    
    @brief   Creates sorted queue of points for specified data.
    
    @param[in] data: pointer to points.
    
    */
    void create_queue(const dataset * data);

    /*!
    
    @brief   Remove representative points of specified cluster from KD Tree.
    
    @param[in] cluster: pointer to points.
    
    */
    void remove_representative_points(cure_cluster * cluster);

    /*!
    
    @brief   Insert representative points of specified cluster to KD tree.
    
    @param[in] cluster: pointer to points.
    
    */
    void insert_representative_points(cure_cluster * cluster);

    /*!
    
    @brief   Insert cluster to sorted queue (it's not insertion of new object).
    @details Used by sorting procedures.
    
    @param[in] inserted_cluster: pointer to points.
    
    */
    void insert_cluster(cure_cluster * inserted_cluster);

    /*!
    
    @brief   Remove cluster from sorted queue (it's not removing of new object). Used by sorting
              procedures.
    
    @param[in] removed_cluster: pointer to points.
    
    */
    void remove_cluster(cure_cluster * removed_cluster);

    /*!
    
    @brief   Calculate distance between clusters.
    
    @param[in] cluster1: pointer to cure cluster 1.
    @param[in] cluster2: pointer to cure cluster 2.
    
    @return  Return distance between clusters.
    
    */
    static double get_distance(cure_cluster * cluster1, cure_cluster * cluster2);

    /*!
    
    @brief   Checks if all elements of a merged cluster are same.
    
    @param[in] merged_cluster: pointer to cure merged_cluster.
    
    @return  Returns true if all the elements in the cluster were found to be same.
    
    */
    static bool are_all_elements_same(cure_cluster * merged_cluster);

public:
    /*!
    
    @brief  Iterator to iterate though CURE clusters in the sorted queue.
    
    */
    using iterator        = std::multiset<cure_cluster *, cure_cluster_comparator>::iterator;

    /*!

    @brief  Constant iterator to iterate though CURE clusters in the sorted queue.

    */
    using const_iterator  = std::multiset<cure_cluster *, cure_cluster_comparator>::const_iterator;

    /*!
    
    @brief   Default constructor of cure queue (always keeps sorted state).
    
    */
    cure_queue();

    /*!
    
    @brief   Default constructor of sorted queue of cure clusters.
    
    @param[in] data: pointer to points.
    
    */
    explicit cure_queue(const std::vector< std::vector<double> > * data);

    /*!
    
    @brief   Default copy constructor of sorted queue of cure clusters is forbidden.
    
    @param[in] p_other: other cure queue to copy.
    
    */
    cure_queue(const cure_queue & p_other) = delete;

    /*!
    
    @brief   Default destructor.
    
    */
    ~cure_queue();

    /*!
    
    @brief   Merge cure clusters in line with the rule of merging of cure algorithm.
    
    @param[in,out] cluster1: pointer to cure cluster 1.
    @param[in,out] cluster2: pointer to cure cluster 2.
    @param[in] number_repr_points: number of representative points for merged cluster.
    @param[in] compression: level of compression for calculation representative points.
    
    */
    void merge(cure_cluster * cluster1, cure_cluster * cluster2, const size_t number_repr_points, const double compression);

    /*!
    
    @brief   Returns iterator to the first CURE cluster.
    
    */
    inline iterator begin() { return queue->begin(); }

    /*!
    
    @brief   Returns constant iterator to the first CURE cluster.
    
    */
    inline const_iterator begin() const { return queue->begin(); };

    /*!
    
    @brief   Returns iterator to the end of CURE cluster collection (not a last element).
    
    */
    inline iterator end() { return queue->end(); }

    /*!
    
    @brief   Returns constant iterator to the end of CURE cluster collection (not a last element).
    
    */
    inline const_iterator end() const { return queue->end(); }

    /*!
    
    @brief   Returns amount of CURE clusters in the queue.
    
    */
    inline std::size_t size() const { return queue->size(); }

public:
    /*!
    
    @brief   Assignment operator is forbidden.
    
    @param[in] p_other: other cure queue to copy.
    
    */
    cure_queue & operator=(const cure_queue & p_other) = delete;
};



/*!

@class  relocation_info cure.hpp pyclustering/cluster/cure.hpp

@brief  Defines relocation request for specific cluster in CURE queue.

*/
class relocation_info {
private:
    cure_queue::iterator m_cluster_iterator;
    cure_cluster * m_closest_cluster;
    double m_closest_distance;

public:
    /*!
    
    @brief  Constructor for relocation request.

    @param[in] cluster_iterator: iterator that points to the cluster in the queue.
    @param[in] closest_cluster: new closest cluster for the cluster that should be relocated.
    @param[in] closest_distance: distance to the closest cluster.
    
    */
    relocation_info(const cure_queue::iterator & cluster_iterator, cure_cluster * closest_cluster, const double closest_distance);

public:
    /*!
    
    @brief  Returns iterator to cluster in CURE queue.

    @return Iterator to cluster in CURE queue that should be relocated.

    */
    cure_queue::iterator get_cluster_iterator() const;

    /*!

    @brief  Returns distance to the closest cluster.

    @return Distance to the closest cluster.

    */
    double get_closest_distance() const;

    /*!

    @brief  Returns pointer to the closest cluster.

    @return Pointer to the closest cluster.

    */
    cure_cluster * get_closest_cluster();
};



/*!

@class   cure cure.hpp pyclustering/cluster/cure.hpp

@brief   CURE clustering algorithm that employes a hierarchical clustering algorithm that adopts a middle
          ground between the centroid-based and the all-point extremes.

@details CURE algorithm identifies clusters having non-spherical shapes and wide variances in size. CURE 
          algorithm represents each cluster by a certain fixed number of points that are generated
          by selecting well scattered points from the cluster and then shrinking them toward the center
          of the cluster by a specified fraction. Having more than one representative point per cluster
          allows CURE to adjust well to the geometry of non-spherical shapes.

Implementation based on paper @cite article::cure::1.

*/
class cure {
private:
    cure_queue * queue;

    std::size_t number_points;

    std::size_t number_clusters;

    double compression;

    const dataset   * data;

public:
    /*!
    
    @brief   Default CURE algorithm constructor.
    
    */
    cure() = default;

    /*!
    
    @brief   Constructor of CURE algorithm.
    
    @param[in] clusters_number: number of clusters that should be allocated.
    @param[in] points_number: number of representative points in each cluster.
    @param[in] level_compression: level of compression for calculation new representative points for merged cluster.
    
    */
    cure(const size_t clusters_number, const size_t points_number, const double level_compression);

    /*!
    
    @brief   Default destructor.
    
    */
    ~cure();

public:
    /*!
    
    @brief    Performs cluster analysis of an input data.
    
    @param[in]  p_data: input data for cluster analysis.
    @param[out] p_result: clustering result of an input data.
    
    */
    void process(const dataset & p_data, cure_data & p_result);
};


}

}