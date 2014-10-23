#ifndef _CURE_H_
#define _CURE_H_

#include <vector>
#include <list>
#include <algorithm>

#include "kdtree.h"
#include "support.h"

/***********************************************************************************************
*
* @brief   Cure cluster description.
*
***********************************************************************************************/
struct cure_cluster {
public:
	std::vector<double> * mean;
	std::vector< std::vector<double> * > * points;
	std::vector< std::vector<double> * > * rep;

	cure_cluster *			closest;
	double					distance_closest;

public:
	/***********************************************************************************************
	*
	* @brief   Default constructor of cure cluster.
	*
	***********************************************************************************************/
	cure_cluster(void);

	/***********************************************************************************************
	*
	* @brief   Default constructor of cure cluster that corresponds to specified point.
	*
	***********************************************************************************************/
	cure_cluster(std::vector<double> * point);

	/***********************************************************************************************
	*
	* @brief   Default destructor.
	*
	***********************************************************************************************/
	~cure_cluster(void);

	/***********************************************************************************************
	*
	* @brief   Insert points to cluster.
	*
	***********************************************************************************************/
	inline void insert_points(std::vector<std::vector<double> *> * append_points) { points->insert(points->end(), append_points->begin(), append_points->end()); }
};



/***********************************************************************************************
*
* @brief   Cure sorted queue of cure clusters. Sorting is defined by distances between clusters.
*          First element is always occupied by cluster whose distance to the neighbor cluster
*          is the smallest in the queue.
*
***********************************************************************************************/
class cure_queue {
private:
	std::list<cure_cluster *> * queue;
	kdtree * tree;

private:

	/***********************************************************************************************
	*
	* @brief   Create sorted queue of points for specified data.
	*
	* @param   data            - pointer to points.
	*
	***********************************************************************************************/
	void create_queue(const std::vector< std::vector<double> * > * data);

	void remove_representative_points(cure_cluster * cluster);

	void insert_representative_points(cure_cluster * cluster);

	/***********************************************************************************************
	*
	* @brief   Insert cluster to sorted queue (it's not insertion of new object). Used by sorting
	*          procedures.
	*
	* @param   inserted_cluster    - pointer to points.
	*
	***********************************************************************************************/
	void insert_cluster(cure_cluster * inserted_cluster);

	/***********************************************************************************************
	*
	* @brief   Remove cluster from sorted queue (it's not removing of new object). Used by sorting
	*          procedures.
	*
	* @param   removed_cluster     - pointer to points.
	*
	***********************************************************************************************/
	inline void remove_cluster(cure_cluster * removed_cluster) { queue->remove(removed_cluster); }

public:
	typedef std::list<cure_cluster *>::iterator iterator;
	typedef std::list<cure_cluster *>::const_iterator const_iterator;

	/***********************************************************************************************
	*
	* @brief   Default constructor of cure queue (always keepds sorted state).
	*
	***********************************************************************************************/
	cure_queue(void);

	/***********************************************************************************************
	*
	* @brief   Default constructor of sorted queue of cure clusters.
	*
	* @param   data            - pointer to points.
	*
	***********************************************************************************************/
	cure_queue(const std::vector< std::vector<double> * > * data);

	/***********************************************************************************************
	*
	* @brief   Default destructor.
	*
	***********************************************************************************************/
	~cure_queue(void);

	/***********************************************************************************************
	*
	* @brief   Calculate distance between clusters.
	*
	* @param   cluster1            - pointer to cure cluster 1.
	* @param   cluster2            - pointer to cure cluster 2.
	*
	* @return  Return distance between clusters.
	*
	***********************************************************************************************/
	double get_distance(cure_cluster * cluster1, cure_cluster * cluster2);

	void merge(cure_cluster * cluster1, cure_cluster * cluster2, const unsigned int number_repr_points, const double compression);

	inline iterator begin(void) { return queue->begin(); }

	inline const_iterator begin(void) const { return queue->begin(); };

	inline iterator end(void) { return queue->end(); }

	inline const_iterator end(void) const { return queue->end(); }

	inline unsigned int size(void) { return queue->size(); }
};



class cure {
private:
	cure_queue * queue;

	unsigned int number_points;
	unsigned int number_clusters;
	double compression;

public:
	cure(const std::vector<std::vector<double> * > * data, const unsigned int clusters_number, const unsigned int points_number, const double compression);

	~cure(void);

	void process(void);

	const std::vector<std::vector<unsigned int> *> * const get_clusters(void) const;
};

#endif