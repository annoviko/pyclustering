"""!

@brief Module for representing clustering results.

@authors Andrei Novikov (pyclustering@yandex.ru)
@date 2014-2016
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


from enum import IntEnum;


class type_cluster_result(IntEnum):
    ## Results are represented by list of indexes and belonging to the cluster is defined by cluster index and element's position corresponds to object's position in input data, for example [0, 0, 1, 1, 1, 0].
    CLUSTER_INDEX_LABELING = 0;
    
    ## Results are represented by list of lists, where each list consists of object indexes, for example [ [0, 1, 2], [3, 4, 5], [6, 7] ].
    CLUSTER_INDEX_LIST_SEPARATION = 1;
    
    ## Results are represented by list of lists, where each list consists of objects, for example [ [obj1, obj2], [obj3, obj4, obj5], [obj6, obj7] ].
    CLUSTER_OBJECT_LIST_SEPARATION = 2;


class cluster_result_representor:
    """!
    @brief Provides service to change clustering result representation.
    
    Example:
    @code
        # load list of points for cluster analysis
        sample = read_sample(path);
        
        # create instance of K-Means algorithm
        kmeans_instance = kmeans(sample, [ [0.0, 0.1], [2.5, 2.6] ]);
        
        # run cluster analysis and obtain results
        kmeans_instance.process();
        clusters = kmeans_instance.get_clusters();
        
        # by default k-means returns representation CLUSTER_INDEX_LIST_SEPARATION
        type_repr = type_cluster_result.CLUSTER_INDEX_LIST_SEPARATION;
        representor = cluster_result_representor(type_repr, clusters, sample);
        
        # change representation from index list to label list
        representor.get_representation(type_cluster_result.CLUSTER_INDEX_LABELING);
        
        # change representation from label to object list
        representor.get_representation(type_cluster_result.CLUSTER_OBJECT_LIST_SEPARATION);
    @endcode
    """
    
    def __init__(self, type_representation, clusters, data):
        """!
        @brief Constructor of cluster result representor.
        
        @param[in] type_representation (type_cluster_result): Type of clusters representation (index list, object list or labels).
        @param[in] clusters (list): Current clusters representation.
        @param[in] data (list): Data that corresponds to clusters.
        
        """
    
        self.__type_representation = type_representation;
        self.__clusters = clusters;
        self.__data = data;


    @property
    def get_representation(self):
        """!
        @brief Returns current cluster representation.
        
        """
        return self.__type_representation;


    def get_clusters(self):
        """!
        @brief Returns clusters representation.
        
        """
        return self.__clusters;


    def get_data(self):
        """!
        @brief Returns data that corresponds to clusters.
        
        """
        return self.__data;


    def set_representation(self, type_representation):
        """!
        @brief Change clusters representation to specified type.
        
        @param[in] type_representation (type_cluster_result): New type of clusters representation.
        
        """
        
        if(type_representation == self.__type_representation):
            return;
        
        if (self.__type_representation == type_cluster_result.CLUSTER_INDEX_LABELING):
            if (type_representation == type_cluster_result.CLUSTER_INDEX_LIST_SEPARATION):
                self.__clusters = self.__convert_label_to_index();
            
            else:
                self.__clusters = self.__convert_label_to_object();
        
        elif (self.__type_representation == type_cluster_result.CLUSTER_INDEX_LIST_SEPARATION):
            if (type_representation == type_cluster_result.CLUSTER_INDEX_LABELING):
                self.__clusters = self.__convert_index_to_label();
            
            else:
                self.__clusters = self.__convert_index_to_object();
        
        else:
            if (type_representation == type_cluster_result.CLUSTER_INDEX_LABELING):
                self.__clusters = self.__convert_object_to_label();
            
            else:
                self.__clusters = self.__convert_object_to_index();
        
        self.__type_representation = type_representation;


    def __convert_index_to_label(self):
        clusters = [0] * len(self.__data);
        index_cluster = 0;
        
        for cluster in self.__clusters:
            for index_object in cluster:
                clusters[index_object] = index_cluster;
        
            index_cluster += 1;
        
        return clusters;


    def __convert_index_to_object(self):
        clusters = [ [] for _ in range(len(self.__clusters)) ];
        for index_cluster in range(len(self.__clusters)):
            for index_object in self.__clusters[index_cluster]:
                data_object = self.__data[index_object];
                clusters[index_cluster].append(data_object);

        return clusters;


    def __convert_object_to_label(self):
        positions = dict();
        clusters = [0] * len(self.__data);
        index_cluster = 0;
        
        for cluster in self.__clusters:
            for data_object in cluster:
                index_object = -1;
                if (data_object in positions):
                    index_object = self.__data.index(data_object, positions[data_object] + 1);
                else:
                    index_object = self.__data.index(data_object);
                    
                clusters[index_object] = index_cluster;
                positions[data_object] = index_object;
            
            index_cluster += 1;
        
        return clusters;


    def __convert_object_to_index(self):
        positions = dict();
        clusters = [ [] for _ in range(len(self.__clusters)) ];
        for index_cluster in range(len(self.__clusters)):
            for data_object in self.__clusters[index_cluster]:
                index_object = -1;
                if (data_object in positions):
                    index_object = self.__data.index(data_object, positions[data_object] + 1);
                else:
                    index_object = self.__data.index(data_object);

                clusters[index_cluster].append(index_object);
                positions[data_object] = index_object;

        return clusters;


    def __convert_label_to_index(self):
        clusters = [ [] for _ in range(max(self.__clusters) + 1) ];
        
        for index_object in range(len(self.__data)):
            index_cluster = self.__clusters[index_object];
            clusters[index_cluster].append(index_object);
        
        return clusters;
    
    
    def __convert_label_to_object(self):
        clusters = [ [] for _ in range(max(self.__clusters) + 1) ];
        
        for index_object in range(len(self.__data)):
            index_cluster = self.__clusters[index_object];
            clusters[index_cluster].append(self.__data[index_object]);
        
        return clusters;