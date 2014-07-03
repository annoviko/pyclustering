#ifndef _KMEANS_H_
#define _KMEANS_H_

#include <vector>

class kmeans {
private:
	std::vector<std::vector<double> >			* dataset;
	std::vector<std::vector<unsigned int> *>	* clusters;
	std::vector<std::vector<double> >			* centers;

	double										tolerance;

public:
	kmeans(const std::vector<std::vector<double> > * const data, const std::vector<std::vector<double> > * const centers, const double tolerance);

	~kmeans(void);

	void process(void);

	inline const std::vector<std::vector<unsigned int> *> * const get_clusters(void) const {
		return clusters;
	}

private:
	void update_clusters(void);

	double update_centers(void);
};

#endif