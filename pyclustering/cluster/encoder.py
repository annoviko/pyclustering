"""!

@brief Module for representing clustering results.

@authors Andrei Novikov (pyclustering@yandex.ru)
@date 2014-2020
@copyright BSD-3-Clause

"""

import math

from enum import IntEnum


class type_encoding(IntEnum):
    """!
    @brief Enumeration of encoding types (index labeling, index list separation, object list separation).
    
    """
    
    ## Results are represented by list of indexes and belonging to the cluster is defined by cluster index and element's position corresponds to object's position in input data, for example [0, 0, 1, 1, 1, 0].
    CLUSTER_INDEX_LABELING = 0
    
    ## Results are represented by list of lists, where each list consists of object indexes from input data, for example [ [0, 1, 2], [3, 4, 5], [6, 7] ].
    CLUSTER_INDEX_LIST_SEPARATION = 1
    
    ## Results are represented by list of lists, where each list consists of objects from input data, for example [ [obj1, obj2], [obj3, obj4, obj5], [obj6, obj7] ].
    CLUSTER_OBJECT_LIST_SEPARATION = 2


class cluster_encoder:
    """!
    @brief Provides service to change clustering result representation.
    @details There are three general types of representation:
    1. Index List Separation that is defined by `CLUSTER_INDEX_LIST_SEPARATION`, for example `[[0, 1, 2], [3, 4], [5, 6, 7]`.
    2. Index Labeling that is defined by `CLUSTER_INDEX_LABELING`, for example `[0, 0, 0, 1, 1, 2, 2, 2]`.
    3. Object List Separation that is defined by `CLUSTER_OBJECT_LIST_SEPARATION`, for example `[[obj1, obj2, obj3], [obj4, obj5], [obj5, obj6, obj7]`.

    There is an example how to covert default Index List Separation to other types:
    @code
        from pyclustering.utils import read_sample
        from pyclustering.samples.definitions import SIMPLE_SAMPLES

        from pyclustering.cluster.encoder import type_encoding, cluster_encoder
        from pyclustering.cluster.kmeans import kmeans

        # load list of points for cluster analysis
        sample = read_sample(SIMPLE_SAMPLES.SAMPLE_SIMPLE1)

        # create instance of K-Means algorithm
        kmeans_instance = kmeans(sample, [[3.0, 5.1], [6.5, 8.6]])

        # run cluster analysis and obtain results
        kmeans_instance.process()
        clusters = kmeans_instance.get_clusters()
        print("Index List Separation:", clusters)

        # by default k-means returns representation CLUSTER_INDEX_LIST_SEPARATION
        type_repr = kmeans_instance.get_cluster_encoding()
        encoder = cluster_encoder(type_repr, clusters, sample)

        # change representation from index list to label list
        encoder.set_encoding(type_encoding.CLUSTER_INDEX_LABELING)
        print("Index Labeling:", encoder.get_clusters())

        # change representation from label to object list
        encoder.set_encoding(type_encoding.CLUSTER_OBJECT_LIST_SEPARATION)
        print("Object List Separation:", encoder.get_clusters())
    @endcode

    Output of the code above is following:
    @code
        Index List Separation: [[0, 1, 2, 3, 4], [5, 6, 7, 8, 9]]
        Index Labeling: [0, 0, 0, 0, 0, 1, 1, 1, 1, 1]
        Object List Separation: [[[3.522979, 5.487981], [3.768699, 5.364477], [3.423602, 5.4199], [3.803905, 5.389491], [3.93669, 5.663041]], [[6.968136, 7.755556], [6.750795, 7.269541], [6.593196, 7.850364], [6.978178, 7.60985], [6.554487, 7.498119]]]
    @endcode

    If there is no index or object in clusters that exists in an input data then it is going to be marked as `NaN` in
    case of Index Labeling. Here is an example:
    @code
        from pyclustering.cluster.encoder import type_encoding, cluster_encoder

        # An input data.
        sample = [[1.0, 1.2], [1.2, 2.3], [114.3, 54.1], [2.2, 1.4], [5.3, 1.3]]

        # Clusters do not contains object with index 2 ([114.3, 54.1]) because it is outline.
        clusters = [[0, 1], [3, 4]]

        encoder = cluster_encoder(type_encoding.CLUSTER_INDEX_LIST_SEPARATION, clusters, sample)
        encoder.set_encoding(type_encoding.CLUSTER_INDEX_LABELING)

        print("Index Labeling:", encoder.get_clusters())
    @endcode

    Here is an output of the code above. Pay attention to `NaN` value for the object with index 2 `[114.3, 54.1]`.
    @code
        Index Labeling: [0, 0, nan, 1, 1]
    @endcode

    """
    
    def __init__(self, encoding, clusters, data):
        """!
        @brief Constructor of clustering result representor.
        
        @param[in] encoding (type_encoding): Type of clusters representation (Index List, Object List or Labels).
        @param[in] clusters (list): Clusters that were allocated from an input data.
        @param[in] data (list): Data that was used for cluster analysis.

        @see type_encoding

        """
    
        self.__type_representation = encoding
        self.__clusters = clusters
        self.__data = data


    @property
    def get_encoding(self):
        """!
        @brief Returns current cluster representation.
        
        """
        return self.__type_representation


    def get_clusters(self):
        """!
        @brief Returns clusters that are represented in line with type that is defined by `get_encoding()`.

        @see get_encoding()

        """
        return self.__clusters


    def get_data(self):
        """!
        @brief Returns data that was used for cluster analysis.
        
        """
        return self.__data


    def set_encoding(self, encoding):
        """!
        @brief Change clusters encoding to specified type (Index List, Object List, Labeling).
        
        @param[in] encoding (type_encoding): New type of clusters representation.

        @return (cluster_encoder) Return itself.

        """
        
        if encoding == self.__type_representation:
            return self
        
        if self.__type_representation == type_encoding.CLUSTER_INDEX_LABELING:
            if encoding == type_encoding.CLUSTER_INDEX_LIST_SEPARATION:
                self.__clusters = self.__convert_label_to_index()
            
            else:
                self.__clusters = self.__convert_label_to_object()
        
        elif self.__type_representation == type_encoding.CLUSTER_INDEX_LIST_SEPARATION:
            if encoding == type_encoding.CLUSTER_INDEX_LABELING:
                self.__clusters = self.__convert_index_to_label()
            
            else:
                self.__clusters = self.__convert_index_to_object()
        
        else:
            if encoding == type_encoding.CLUSTER_INDEX_LABELING:
                self.__clusters = self.__convert_object_to_label()
            
            else:
                self.__clusters = self.__convert_object_to_index()
        
        self.__type_representation = encoding
        return self


    def __convert_index_to_label(self):
        clusters = [float('NaN')] * len(self.__data)
        index_cluster = 0
        
        for cluster in self.__clusters:
            for index_object in cluster:
                clusters[index_object] = index_cluster
        
            index_cluster += 1
        
        return clusters


    def __convert_index_to_object(self):
        clusters = [ [] for _ in range(len(self.__clusters)) ]
        for index_cluster in range(len(self.__clusters)):
            for index_object in self.__clusters[index_cluster]:
                data_object = self.__data[index_object]
                clusters[index_cluster].append(data_object)

        return clusters


    def __convert_object_to_label(self):
        positions = dict()
        clusters = [float('NaN')] * len(self.__data)
        index_cluster = 0
        
        for cluster in self.__clusters:
            for data_object in cluster:
                hashable_data_object = str(data_object)
                if hashable_data_object in positions:
                    index_object = self.__data.index(data_object, positions[hashable_data_object] + 1)
                else:
                    index_object = self.__data.index(data_object)
                    
                clusters[index_object] = index_cluster
                positions[hashable_data_object] = index_object
            
            index_cluster += 1
        
        return clusters


    def __convert_object_to_index(self):
        positions = dict()
        clusters = [[] for _ in range(len(self.__clusters))]
        for index_cluster in range(len(self.__clusters)):
            for data_object in self.__clusters[index_cluster]:
                hashable_data_object = str(data_object)
                if hashable_data_object in positions:
                    index_object = self.__data.index(data_object, positions[hashable_data_object] + 1)
                else:
                    index_object = self.__data.index(data_object)

                clusters[index_cluster].append(index_object)
                positions[hashable_data_object] = index_object

        return clusters


    def __convert_label_to_index(self):
        clusters = [[] for _ in range(max(self.__clusters) + 1)]
        
        for index_object in range(len(self.__data)):
            index_cluster = self.__clusters[index_object]
            if not math.isnan(index_cluster):
                clusters[index_cluster].append(index_object)
        
        return clusters


    def __convert_label_to_object(self):
        clusters = [[] for _ in range(max(self.__clusters) + 1)]
        
        for index_object in range(len(self.__data)):
            index_cluster = self.__clusters[index_object]
            if not math.isnan(index_cluster):
                clusters[index_cluster].append(self.__data[index_object])
        
        return clusters
