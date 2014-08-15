#ifndef _XMEANS_H_
#define _XMEANS_H_

#include <vector>

#define FAST_SOLUTION

class xmeans {
private:
	std::vector<std::vector<double> >			* dataset;
	std::vector<std::vector<unsigned int> *>	* clusters;
	std::vector<std::vector<double> >			* centers;

	unsigned int								maximum_clusters;
	double										tolerance;

public:
	xmeans(const std::vector<std::vector<double> > * const data, const std::vector<std::vector<double> > * const initial_centers, const unsigned int kmax, const double minimum_change);

	~xmeans(void);

	void process(void);

	inline const std::vector<std::vector<unsigned int> *> * const get_clusters(void) const {
		return clusters;
	}

private:
	void update_clusters(std::vector<std::vector<unsigned int> *> * clusters, std::vector<std::vector<double> > * centers, const std::vector<unsigned int> * const available_indexes);

	double update_centers(std::vector<std::vector<unsigned int> *> * clusters, std::vector<std::vector<double> > * centers);

	void improve_structure(void);

	void improve_parameters(std::vector<std::vector<unsigned int> *> * clusters, std::vector<std::vector<double> > * centers, const std::vector<unsigned int> * const available_indexes);

	double splitting_criterion(const std::vector<std::vector<unsigned int> * > * const clusters, const std::vector<std::vector<double> > * const centers) const;

	unsigned int find_proper_cluster(std::vector<std::vector<double> > * analysed_centers, const std::vector<double> * const point) const;
};

#endif
