"""!

@brief BIRCH (Balanced Iterative Reducing and Clustering using Hierarchies) cluster analysis algorithm.
@details Implementation based on paper @cite article::birch::1.
         
@authors Andrei Novikov (pyclustering@yandex.ru)
@date 2014-2019
@copyright GNU Public License

@cond GNU_PUBLIC_LICENSE
    PyClustering is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.
    
    PyClustering is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.
    
    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
@endcond

"""

import numpy

from pyclustering.cluster.agglomerative import agglomerative, type_link
from pyclustering.cluster.encoder import cluster_encoder, type_encoding

from pyclustering.container.cftree import cftree, measurement_type


class birch:
    """!
    @brief Class represents the clustering algorithm BIRCH (Balanced Iterative Reducing and Clustering using
            Hierarchies).

    @details BIRCH is suitable for large databases. The algorithm incrementally and dynamically clusters
              incoming multi-dimensional metric data points using the concepts of Clustering Feature and CF tree.
              A Clustering Feature is a triple summarizing the information that is maintained about a cluster.
              The Clustering Feature vector is defined as a triple:
              \f[CF=\left ( N, \overrightarrow{LS}, SS \right )\f]

    Example how to extract clusters from 'OldFaithful' sample using BIRCH algorithm:
    @code
        from pyclustering.cluster.birch import birch
        from pyclustering.cluster import cluster_visualizer
        from pyclustering.utils import read_sample
        from pyclustering.samples.definitions import FAMOUS_SAMPLES

        # Sample for cluster analysis (represented by list)
        sample = read_sample(FAMOUS_SAMPLES.SAMPLE_OLD_FAITHFUL)

        # Create BIRCH algorithm
        birch_instance = birch(sample, 2, diameter=3.0)

        # Cluster analysis
        birch_instance.process()

        # Obtain results of clustering
        clusters = birch_instance.get_clusters()

        # Visualize allocated clusters
        visualizer = cluster_visualizer()
        visualizer.append_clusters(clusters, sample)
        visualizer.show()
    @endcode

    Here is the clustering result produced by BIRCH algorithm:
    @image html birch_clustering_old_faithful.png "Fig. 1. BIRCH clustering - sample 'OldFaithful'."

    Methods 'get_cf_entries' and 'get_cf_clusters' can be used to obtain information how does an input data is
    encoded. Here is an example how the encoding information can be extracted and visualized:
    @code
        from pyclustering.cluster.birch import birch
        from pyclustering.cluster import cluster_visualizer
        from pyclustering.utils import read_sample
        from pyclustering.samples.definitions import FCPS_SAMPLES

        # Sample 'Lsun' for cluster analysis (represented by list of points)
        sample = read_sample(FCPS_SAMPLES.SAMPLE_LSUN)

        # Create BIRCH algorithm
        birch_instance = birch(sample, 3, diameter=0.5)

        # Cluster analysis
        birch_instance.process()

        # Obtain results of clustering
        clusters = birch_instance.get_clusters()

        # Obtain information how does the 'Lsun' sample is encoded in the CF-tree.
        cf_entries = birch_instance.get_cf_entries()
        cf_clusters = birch_instance.get_cf_cluster()

        cf_centroids = [entry.get_centroid() for entry in cf_entries]

        # Visualize allocated clusters
        visualizer = cluster_visualizer(2, 2, titles=["Encoded data by CF-entries", "Data clusters"])
        visualizer.append_clusters(cf_clusters, cf_centroids, canvas=0)
        visualizer.append_clusters(clusters, sample, canvas=1)
        visualizer.show()
    @endcode

    Here is the clustering result produced by BIRCH algorithm:
    @image html birch_cf_encoding_lsun.png "Fig. 2. CF-tree encoding and BIRCH clustering of 'Lsun' sample."

    """
    
    def __init__(self, data, number_clusters, branching_factor=50, max_node_entries=200, diameter=0.5,
                 type_measurement=measurement_type.CENTROID_EUCLIDEAN_DISTANCE,
                 entry_size_limit=500,
                 diameter_multiplier=1.5,
                 ccore=True):
        """!
        @brief Constructor of clustering algorithm BIRCH.
        
        @param[in] data (list): An input data represented as a list of points (objects) where each point is be represented by list of coordinates.
        @param[in] number_clusters (uint): Amount of clusters that should be allocated.
        @param[in] branching_factor (uint): Maximum number of successor that might be contained by each non-leaf node in CF-Tree.
        @param[in] max_node_entries (uint): Maximum number of entries that might be contained by each leaf node in CF-Tree.
        @param[in] diameter (double): CF-entry diameter that used for CF-Tree construction, it might be increase if 'entry_size_limit' is exceeded.
        @param[in] type_measurement (measurement_type): Type measurement used for calculation distance metrics.
        @param[in] entry_size_limit (uint): Maximum number of entries that can be stored in CF-Tree, if it is exceeded
                    during creation then the 'diameter' is increased and CF-Tree is rebuilt.
        @param[in] diameter_multiplier (double): Multiplier that is used for increasing diameter when 'entry_size_limit' is exceeded.
        @param[in] ccore (bool): If True than C++ part of the library is used for processing.

        """
        
        self.__pointer_data = data
        self.__number_clusters = number_clusters
        
        self.__measurement_type = type_measurement
        self.__entry_size_limit = entry_size_limit
        self.__diameter_multiplier = diameter_multiplier
        self.__ccore = ccore

        self.__verify_arguments()

        self.__features = None
        self.__tree = cftree(branching_factor, max_node_entries, diameter, type_measurement)
        
        self.__clusters = []
        self.__cf_clusters = []


    def process(self):
        """!
        @brief Performs cluster analysis in line with rules of BIRCH algorithm.
        
        @return (birch) Returns itself (BIRCH instance).
        
        @see get_clusters()
        
        """
        
        self.__insert_data()
        self.__extract_features()

        cf_data = [feature.get_centroid() for feature in self.__features]

        algorithm = agglomerative(cf_data, self.__number_clusters, type_link.SINGLE_LINK).process()
        self.__cf_clusters = algorithm.get_clusters()

        cf_labels = cluster_encoder(type_encoding.CLUSTER_INDEX_LIST_SEPARATION, self.__cf_clusters, cf_data).\
            set_encoding(type_encoding.CLUSTER_INDEX_LABELING).get_clusters()

        self.__clusters = [[] for _ in range(len(self.__cf_clusters))]
        for index_point in range(len(self.__pointer_data)):
            index_cf_entry = numpy.argmin(numpy.sum(numpy.square(
                numpy.subtract(cf_data, self.__pointer_data[index_point])), axis=1))
            index_cluster = cf_labels[index_cf_entry]
            self.__clusters[index_cluster].append(index_point)

        return self


    def get_clusters(self):
        """!
        @brief Returns list of allocated clusters, each cluster is represented by a list of indexes where each index
                corresponds to a point in an input dataset.

        @return (list) List of allocated clusters.
        
        @see process()
        
        """
        
        return self.__clusters


    def get_cf_entries(self):
        """!
        @brief Returns CF-entries that encodes an input dataset.

        @return (list) CF-entries that encodes an input dataset.

        @see get_cf_cluster

        """
        return self.__features


    def get_cf_cluster(self):
        """!
        @brief Returns list of allocated CF-entry clusters where each cluster is represented by indexes (each index
                corresponds to CF-entry).

        @return (list) List of allocated CF-entry clusters.

        @see get_cf_entries

        """
        return self.__cf_clusters


    def get_cluster_encoding(self):
        """!
        @brief Returns clustering result representation type that indicate how clusters are encoded.
        
        @return (type_encoding) Clustering result representation.
        
        @see get_clusters()
        
        """
        
        return type_encoding.CLUSTER_INDEX_LIST_SEPARATION


    def __verify_arguments(self):
        """!
        @brief Verify input parameters for the algorithm and throw exception in case of incorrectness.

        """
        if len(self.__pointer_data) == 0:
            raise ValueError("Input data is empty (size: '%d')." % len(self.__pointer_data))

        if self.__number_clusters <= 0:
            raise ValueError("Amount of cluster (current value: '%d') for allocation should be greater than 0." %
                             self.__number_clusters)

        if self.__entry_size_limit <= 0:
            raise ValueError("Limit entry size (current value: '%d') should be greater than 0." %
                             self.__entry_size_limit)


    def __extract_features(self):
        """!
        @brief Extracts features from CF-tree cluster.
        
        """
        
        self.__features = []
        
        if len(self.__tree.leafes) == 1:
            # parameters are too general, copy all entries
            for entry in self.__tree.leafes[0].entries:
                self.__features.append(entry)

        else:
            # copy all leaf clustering features
            for leaf_node in self.__tree.leafes:
                self.__features += leaf_node.entries


    def __insert_data(self):
        """!
        @brief Inserts input data to the tree.
        
        @remark If number of maximum number of entries is exceeded than diameter is increased and tree is rebuilt.
        
        """
        
        for index_point in range(0, len(self.__pointer_data)):
            point = self.__pointer_data[index_point]
            self.__tree.insert_point(point)
            
            if self.__tree.amount_entries > self.__entry_size_limit:
                self.__tree = self.__rebuild_tree(index_point)
    
    
    def __rebuild_tree(self, index_point):
        """!
        @brief Rebuilt tree in case of maxumum number of entries is exceeded.
        
        @param[in] index_point (uint): Index of point that is used as end point of re-building.
        
        @return (cftree) Rebuilt tree with encoded points till specified point from input data space.
        
        """

        rebuild_result = False
        increased_diameter = self.__tree.threshold * self.__diameter_multiplier
        
        tree = None
        
        while rebuild_result is False:
            # increase diameter and rebuild tree
            if increased_diameter == 0.0:
                increased_diameter = 1.0
            
            # build tree with update parameters
            tree = cftree(self.__tree.branch_factor, self.__tree.max_entries, increased_diameter, self.__tree.type_measurement)
            
            for index_point in range(0, index_point + 1):
                point = self.__pointer_data[index_point]
                tree.insert_point(point)

                if tree.amount_entries > self.__entry_size_limit:
                    increased_diameter *= self.__diameter_multiplier
                    continue
            
            # Re-build is successful.
            rebuild_result = True
        
        return tree
