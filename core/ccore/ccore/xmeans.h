#if 0
#ifndef _XMEANS_H_
#define _XMEANS_H_

#include <vector>

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
	void update_clusters(const std::vector<std::vector<unsigned int> > * const available_indexes = NULL);

	double update_centers(void);

	void improve_structure(void);

	void improve_parameters(const std::vector<std::vector<unsigned int> > * const available_indexes = NULL);

	double splitting_criterion(const std::vector<std::vector<unsigned int> > * const clusters, const std::vector<std::vector<double> > * const centers) const;
};

#endif
#endif