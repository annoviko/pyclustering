#ifndef _HIERARCHICAL_H_
#define _HIERARCHICAL_H_

#include <vector>
#include <list>

class hierarchical_cluster {
private:
	std::vector<std::vector<double> >	* dataset;	/* pointer to input data set */
	std::vector<unsigned int>		* indexes; 	/* indexes of objects in input data set */
	std::vector<double>			* center; 	/* center of the cluster */

public:
	hierarchical_cluster(const std::vector<std::vector<double> > * const data, const unsigned int index, const std::vector<double> * const point);

	~hierarchical_cluster(void);

	void append(const hierarchical_cluster * const cluster2);

	inline const std::vector<double> * const get_center(void) const {
		return center;
	}

	inline const std::vector<unsigned int> * const get_indexes(void) const {
		return indexes;
	}
};


class hierarchical {
private:
	std::list<hierarchical_cluster *>		* clusters;
	std::vector<std::vector<unsigned int> * >	* standard_clusters;
	std::vector<std::vector<double> >		* data;
	unsigned int 					number_clusters;

public:
	hierarchical(const std::vector<std::vector<double> > * const dataset, unsigned int cluster_number);

	~hierarchical(void);

	void process(void);

	inline const std::vector<std::vector<unsigned int> *> * const get_clusters(void) const {
		return standard_clusters;
	}

private:
	void merge_nearest_clusters(void);
};

#endif
