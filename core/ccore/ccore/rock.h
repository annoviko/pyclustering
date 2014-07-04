#ifndef _ROCK_H_
#define _ROCK_H_

#include <vector>

class rock {
private:
	std::vector<std::vector<double> >			* dataset;
	std::vector<std::vector<unsigned int> >		* adjacency_matrix;

	std::vector<std::vector<unsigned int> *>	* clusters;

	double			degree_normalization;
	unsigned int	number_clusters;

public:
	rock(const std::vector<std::vector<double> > * const dataset, const double radius, const unsigned int number_clusters, const double threshold);

	~rock(void);

	void process(void);

	inline const std::vector<std::vector<unsigned int> *> * const get_clusters(void) const {
		return clusters;
	}

private:
	bool merge_cluster(void);

	std::vector<unsigned int> * find_pair_clusters(void) const;

	unsigned int calculate_links(const unsigned int index_cluster1, const unsigned int index_cluster2) const;

	double calculate_goodness(const unsigned int index_cluster1, const unsigned int index_cluster2) const;
};

#endif