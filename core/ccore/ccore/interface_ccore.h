#ifndef _INTERFACE_CCORE_H_
#define _INTERFACE_CCORE_H_

typedef struct cluster_representation {
	unsigned int size;
	unsigned int * objects;
} cluster_representation;

typedef struct clustering_result {
	unsigned int size;
	cluster_representation * clusters;
} clustering_result;

typedef struct data_representation {
	unsigned int size;
	unsigned int dimension;
	double ** objects;
};

extern "C" __declspec(dllexport) void free_clustering_result(clustering_result * pointer);

extern "C" __declspec(dllexport) clustering_result * dbscan_algorithm(const data_representation * const sample, const double radius, const unsigned int minumum_neighbors);

extern "C" __declspec(dllexport) clustering_result * hierarchical_algorithm(const data_representation * const sample, const unsigned int number_clusters);

extern "C" __declspec(dllexport) clustering_result * kmeans_algorithm(const data_representation * const sample, const data_representation * const initial_centers, const double tolerance);

extern "C" __declspec(dllexport) clustering_result * rock_algorithm(const data_representation * const sample, const double radius, const unsigned int number_clusters, const double threshold);

#endif