/**************************************************************************************************************

Cluster analysis algorithm: CURE

Based on article description:
 - S.Guha, R.Rastogi, K.Shim. CURE: An Efficient Clustering Algorithm for Large Databases. 1998.

Copyright (C) 2015    Andrei Novikov (pyclustering@yandex.ru)

pyclustering is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

pyclustering is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.

**************************************************************************************************************/

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
	void create_queue(const std::vector< std::vector<double> > * data);

	/***********************************************************************************************
	*
	* @brief   Remove representative points of specified cluster from KD Tree.
	*
	* @param   cluster             - pointer to points.
	*
	***********************************************************************************************/
	void remove_representative_points(cure_cluster * cluster);

	/***********************************************************************************************
	*
	* @brief   Insert representative points of specified cluster to KD tree.
	*
	* @param   cluster             - pointer to points.
	*
	***********************************************************************************************/
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
	cure_queue(const std::vector< std::vector<double> > * data);

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

	/***********************************************************************************************
	*
	* @brief   Merge cure clusters in line with the rule of merging of cure algorithm.
	*
	* @param   cluster1            - pointer to cure cluster 1.
	* @param   cluster2            - pointer to cure cluster 2.
	* @param   number_repr_points  - number of representative points for merged cluster.
	* @param   compression         - level of compression for calculation representative points.
	*
	***********************************************************************************************/
	void merge(cure_cluster * cluster1, cure_cluster * cluster2, const unsigned int number_repr_points, const double compression);

	/***********************************************************************************************
	*
	* @brief   Checks if all elements of a merged cluster are same
	*
	* @param   merged_cluster            - pointer to cure merged_cluster.
	*
	* @return  Returns true if all the elements in the cluster were found to be same.
	*
	***********************************************************************************************/
	bool are_all_elements_same(cure_cluster * merged_cluster);

	inline iterator begin(void) { return queue->begin(); }

	inline const_iterator begin(void) const { return queue->begin(); };

	inline iterator end(void) { return queue->end(); }

	inline const_iterator end(void) const { return queue->end(); }

	inline unsigned int size(void) { return queue->size(); }
};


/***********************************************************************************************
*
* @brief   CURE algorithm.
*
***********************************************************************************************/
class cure {
private:
	cure_queue * queue;

	unsigned int number_points;
	unsigned int number_clusters;
	double compression;

	std::vector<std::vector<unsigned int> * >	* clusters;
	std::vector<std::vector<double> >			* data;

public:
	/***********************************************************************************************
	*
	* @brief   Constructor of CURE solver (algorithm representer).
	*
	* @param   sample              - pointer to input data for clustering.
	* @param   clusters_number     - number of clusters that should be allocated.
	* @param   points_number       - number of representative points in each cluster.
	* @param   level_compression   - level of copression for calculation new representative points
	*                                for merged cluster.
	*
	***********************************************************************************************/
	cure(const std::vector<std::vector<double> > * sample, const unsigned int clusters_number, const unsigned int points_number, const double level_compression);

	/***********************************************************************************************
	*
	* @brief   Default destructor.
	*
	***********************************************************************************************/
	~cure(void);

	/***********************************************************************************************
	*
	* @brief   Performs cluster analysis of input data. Results of clustering can be obtained
	*          via corresponding get method.
	*
	***********************************************************************************************/
	void process(void);

	inline const std::vector<std::vector<unsigned int> *> * const get_clusters(void) const {
		return clusters;
	}
};

#endif
