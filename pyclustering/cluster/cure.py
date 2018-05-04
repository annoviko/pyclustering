"""!

@brief Cluster analysis algorithm: CURE
@details Implementation based on paper @cite article::cure::1.

@authors Andrei Novikov (pyclustering@yandex.ru)
@date 2014-2018
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


from pyclustering.cluster.encoder import type_encoding;

from pyclustering.utils import euclidean_distance;

from pyclustering.container.kdtree import kdtree;

from pyclustering.core.wrapper import ccore_library

import pyclustering.core.cure_wrapper as wrapper;


class cure_cluster:
    """!
    @brief Represents data cluster in CURE term. 
    @details CURE cluster is described by points of cluster, representation points of the cluster and by the cluster center.
    
    """
    
    def __init__(self, point, index):
        """!
        @brief Constructor of CURE cluster.
        
        @param[in] point (list): Point represented by list of coordinates.
        @param[in] index (uint): Index point in dataset.
        
        """
        
        ## List of points that make up cluster.
        self.points = [ ];
        
        ## Point indexes in dataset.
        self.indexes = -1;
        
        ## Mean of points that make up cluster.
        self.mean = None;
        
        ## List of points that represents clusters.
        self.rep = [ ];
        
        if (point is not None):
            self.points = [ point ];
            self.indexes = [ index ];
            self.mean = point;
            self.rep = [ point ];
        
        ## Pointer to the closest cluster.
        self.closest = None;
        
        ## Distance to the closest cluster.
        self.distance = float('inf');      # calculation of distance is really complexity operation (even square distance), so let's store distance to closest cluster.

    def __repr__(self):
        """!
        @brief Displays distance to closest cluster and points that are contained by current cluster.
        
        """
        return "%s, %s" % (self.distance, self.points);
        

class cure:
    """!
    @brief Class represents clustering algorithm CURE with KD-tree optimization.
    @details CCORE option can be used to use the pyclustering core - C/C++ shared library for processing that significantly increases performance.
    
    Example:
    @code
        # read data for clustering from some file
        sample = read_sample(path_to_data);
        
        # create instance of cure algorithm for cluster analysis
        # request for allocation of two clusters.
        cure_instance = cure(sample, 2, 5, 0.5, True);
        
        # run cluster analysis
        cure_instance.process();
        
        # get results of clustering
        clusters = cure_instance.get_clusters();
    @endcode
    
    """
    
    def __init__(self, data, number_cluster, number_represent_points = 5, compression = 0.5, ccore = True):
        """!
        @brief Constructor of clustering algorithm CURE.
        
        @param[in] data (list): Input data that is presented as list of points (objects), each point should be represented by list or tuple.
        @param[in] number_cluster (uint): Number of clusters that should be allocated.
        @param[in] number_represent_points (uint): Number of representative points for each cluster.
        @param[in] compression (double): Coefficient defines level of shrinking of representation points toward the mean of the new created cluster after merging on each step. Usually it destributed from 0 to 1.
        @param[in] ccore (bool): If True than DLL CCORE (C++ solution) will be used for solving.
        
        """
        
        self.__pointer_data = data;
        
        self.__clusters = None;
        self.__representors = None;
        self.__means = None;
        
        self.__number_cluster = number_cluster;
        self.__number_represent_points = number_represent_points;
        self.__compression = compression;
        
        self.__ccore = ccore;
        if (self.__ccore):
            self.__ccore = ccore_library.workable();
        
        if (self.__ccore is False):
            self.__create_queue();      # queue
            self.__create_kdtree();     # create k-d tree

    
    def process(self):
        """!
        @brief Performs cluster analysis in line with rules of CURE algorithm.
        
        @remark Results of clustering can be obtained using corresponding get methods.
        
        @see get_clusters()
        
        """
        
        if (self.__ccore is True):
            cure_data_pointer = wrapper.cure_algorithm(self.__pointer_data, self.__number_cluster, self.__number_represent_points, self.__compression);
            
            self.__clusters = wrapper.cure_get_clusters(cure_data_pointer);
            self.__representors = wrapper.cure_get_representors(cure_data_pointer);
            self.__means = wrapper.cure_get_means(cure_data_pointer);
            
            wrapper.cure_data_destroy(cure_data_pointer);
            
        else:
            while (len(self.__queue) > self.__number_cluster):
                cluster1 = self.__queue[0];            # cluster that has nearest neighbor.
                cluster2 = cluster1.closest;    # closest cluster.
                
                #print("Merge decision: \n\t", cluster1, "\n\t", cluster2);
                
                self.__queue.remove(cluster1);
                self.__queue.remove(cluster2);
                
                self.__delete_represented_points(cluster1);
                self.__delete_represented_points(cluster2);
        
                merged_cluster = self.__merge_clusters(cluster1, cluster2);
        
                self.__insert_represented_points(merged_cluster);
                
                # Pointers to clusters that should be relocated is stored here.
                cluster_relocation_requests = [];
                
                # Check for the last cluster
                if (len(self.__queue) > 0):
                    merged_cluster.closest = self.__queue[0];  # arbitrary cluster from queue
                    merged_cluster.distance = self.__cluster_distance(merged_cluster, merged_cluster.closest);
                    
                    for item in self.__queue:
                        distance = self.__cluster_distance(merged_cluster, item);
                        # Check if distance between new cluster and current is the best than now.
                        if (distance < merged_cluster.distance):
                            merged_cluster.closest = item;
                            merged_cluster.distance = distance;
                        
                        # Check if current cluster has removed neighbor.
                        if ( (item.closest is cluster1) or (item.closest is cluster2) ):
                            # If previous distance was less then distance to new cluster then nearest cluster should be found in the tree.
                            #print("Update: ", item);
                            if (item.distance < distance):
                                (item.closest, item.distance) = self.__closest_cluster(item, distance);
                                
                                # TODO: investigation of root cause is required.
                                # Itself and merged cluster should be always in list of neighbors in line with specified radius.
                                # But merged cluster may not be in list due to error calculation, therefore it should be added
                                # manually.
                                if (item.closest is None):
                                    item.closest = merged_cluster;
                                    item.distance = distance;
                                
                            # Otherwise new cluster is nearest.
                            else:
                                item.closest = merged_cluster;
                                item.distance = distance;
                            
                            cluster_relocation_requests.append(item);
                        elif (item.distance > distance):
                            item.closest = merged_cluster;
                            item.distance = distance;
                            
                            cluster_relocation_requests.append(item);
                
                # New cluster and updated clusters should relocated in queue
                self.__insert_cluster(merged_cluster);
                for item in cluster_relocation_requests:
                    self.__relocate_cluster(item);
        
            # Change cluster representation
            self.__clusters = [ cure_cluster_unit.indexes for cure_cluster_unit in self.__queue ];
            self.__representors = [ cure_cluster_unit.rep for cure_cluster_unit in self.__queue ];
            self.__means = [ cure_cluster_unit.mean for cure_cluster_unit in self.__queue ];
    
    
    def get_clusters(self):
        """!
        @brief Returns list of allocated clusters, each cluster contains indexes of objects in list of data.
        
        @return (list) List of allocated clusters.
        
        @see process()
        @see get_representors()
        @see get_means()
        
        """
        
        return self.__clusters;
    
    
    def get_representors(self):
        """!
        @brief Returns list of point-representors of each cluster.
        @details Cluster index should be used for navigation between lists of point-representors.
        
        @return (list) List of point-representors of each cluster.
        
        @see get_clusters()
        @see get_means()
        
        """
        
        return self.__representors;
    
    
    def get_means(self):
        """!
        @brief Returns list of mean values of each cluster.
        @details Cluster index should be used for navigation between mean values.
        
        @return (list) List of mean values of each cluster.
        
        @see get_clusters()
        @see get_representors()
        
        """
        
        return self.__means;
    
    
    def get_cluster_encoding(self):
        """!
        @brief Returns clustering result representation type that indicate how clusters are encoded.
        
        @return (type_encoding) Clustering result representation.
        
        @see get_clusters()
        
        """
        
        return type_encoding.CLUSTER_INDEX_LIST_SEPARATION;
    
    
    def __insert_cluster(self, cluster):
        """!
        @brief Insert cluster to the list (sorted queue) in line with sequence order (distance).
        
        @param[in] cluster (cure_cluster): Cluster that should be inserted.
        
        """
        
        for index in range(len(self.__queue)):
            if (cluster.distance < self.__queue[index].distance):
                self.__queue.insert(index, cluster);
                return;
    
        self.__queue.append(cluster);


    def __relocate_cluster(self, cluster):
        """!
        @brief Relocate cluster in list in line with distance order.
        
        @param[in] cluster (cure_cluster): Cluster that should be relocated in line with order.
        
        """
        
        self.__queue.remove(cluster);
        self.__insert_cluster(cluster);


    def __closest_cluster(self, cluster, distance):
        """!
        @brief Find closest cluster to the specified cluster in line with distance.
        
        @param[in] cluster (cure_cluster): Cluster for which nearest cluster should be found.
        @param[in] distance (double): Closest distance to the previous cluster.
        
        @return (tuple) Pair (nearest CURE cluster, nearest distance) if the nearest cluster has been found, otherwise None is returned.
        
        """
        
        nearest_cluster = None;
        nearest_distance = float('inf');
        
        for point in cluster.rep:
            # Nearest nodes should be returned (at least it will return itself).
            nearest_nodes = self.__tree.find_nearest_dist_nodes(point, distance);
            for (candidate_distance, kdtree_node) in nearest_nodes:
                if ( (candidate_distance < nearest_distance) and (kdtree_node is not None) and (kdtree_node.payload is not cluster) ):
                    nearest_distance = candidate_distance;
                    nearest_cluster = kdtree_node.payload;
                    
        return (nearest_cluster, nearest_distance);


    def __insert_represented_points(self, cluster):
        """!
        @brief Insert representation points to the k-d tree.
        
        @param[in] cluster (cure_cluster): Cluster whose representation points should be inserted.
        
        """
        
        for point in cluster.rep:
            self.__tree.insert(point, cluster);


    def __delete_represented_points(self, cluster): 
        """!
        @brief Remove representation points of clusters from the k-d tree
        
        @param[in] cluster (cure_cluster): Cluster whose representation points should be removed.
        
        """
        
        for point in cluster.rep:
            self.__tree.remove(point, payload=cluster);


    def __merge_clusters(self, cluster1, cluster2):
        """!
        @brief Merges two clusters and returns new merged cluster. Representation points and mean points are calculated for the new cluster.
        
        @param[in] cluster1 (cure_cluster): Cluster that should be merged.
        @param[in] cluster2 (cure_cluster): Cluster that should be merged.
        
        @return (cure_cluster) New merged CURE cluster.
        
        """
        
        merged_cluster = cure_cluster(None, None);
        
        merged_cluster.points = cluster1.points + cluster2.points;
        merged_cluster.indexes = cluster1.indexes + cluster2.indexes;
        
        # merged_cluster.mean = ( len(cluster1.points) * cluster1.mean + len(cluster2.points) * cluster2.mean ) / ( len(cluster1.points) + len(cluster2.points) );
        dimension = len(cluster1.mean);
        merged_cluster.mean = [0] * dimension;
        if merged_cluster.points[1:] == merged_cluster.points[:-1]:
            merged_cluster.mean = merged_cluster.points[0]
        else:
            for index in range(dimension):
                merged_cluster.mean[index] = ( len(cluster1.points) * cluster1.mean[index] + len(cluster2.points) * cluster2.mean[index] ) / ( len(cluster1.points) + len(cluster2.points) );
        
        temporary = list();
        
        for index in range(self.__number_represent_points):
            maximal_distance = 0;
            maximal_point = None;
            
            for point in merged_cluster.points:
                minimal_distance = 0;
                if (index == 0):
                    minimal_distance = euclidean_distance(point, merged_cluster.mean);
                    #minimal_distance = euclidean_distance_sqrt(point, merged_cluster.mean);
                else:
                    minimal_distance = min([euclidean_distance(point, p) for p in temporary]);
                    #minimal_distance = cluster_distance(cure_cluster(point), cure_cluster(temporary[0]));
                    
                if (minimal_distance >= maximal_distance):
                    maximal_distance = minimal_distance;
                    maximal_point = point;
        
            if (maximal_point not in temporary):
                temporary.append(maximal_point);
                
        for point in temporary:
            representative_point = [0] * dimension;
            for index in range(dimension):
                representative_point[index] = point[index] + self.__compression * (merged_cluster.mean[index] - point[index]);
                
            merged_cluster.rep.append(representative_point);
        
        return merged_cluster;


    def __create_queue(self):
        """!
        @brief Create queue of sorted clusters by distance between them, where first cluster has the nearest neighbor. At the first iteration each cluster contains only one point.
        
        @param[in] data (list): Input data that is presented as list of points (objects), each point should be represented by list or tuple.
        
        @return (list) Create queue of sorted clusters by distance between them.
        
        """
        
        self.__queue = [cure_cluster(self.__pointer_data[index_point], index_point) for index_point in range(len(self.__pointer_data))];
        
        # set closest clusters
        for i in range(0, len(self.__queue)):
            minimal_distance = float('inf');
            closest_index_cluster = -1;
            
            for k in range(0, len(self.__queue)):
                if (i != k):
                    dist = self.__cluster_distance(self.__queue[i], self.__queue[k]);
                    if (dist < minimal_distance):
                        minimal_distance = dist;
                        closest_index_cluster = k;
            
            self.__queue[i].closest = self.__queue[closest_index_cluster];
            self.__queue[i].distance = minimal_distance;
        
        # sort clusters
        self.__queue.sort(key = lambda x: x.distance, reverse = False);
    

    def __create_kdtree(self):
        """!
        @brief Create k-d tree in line with created clusters. At the first iteration contains all points from the input data set.
        
        @return (kdtree) k-d tree that consist of representative points of CURE clusters.
        
        """
        
        self.__tree = kdtree();
        for current_cluster in self.__queue:
            for representative_point in current_cluster.rep:
                self.__tree.insert(representative_point, current_cluster);    


    def __cluster_distance(self, cluster1, cluster2):
        """!
        @brief Calculate minimal distance between clusters using representative points.
        
        @param[in] cluster1 (cure_cluster): The first cluster.
        @param[in] cluster2 (cure_cluster): The second cluster.
        
        @return (double) Euclidean distance between two clusters that is defined by minimum distance between representation points of two clusters.
        
        """
        
        distance = float('inf');
        for i in range(0, len(cluster1.rep)):
            for k in range(0, len(cluster2.rep)):
                #dist = euclidean_distance_sqrt(cluster1.rep[i], cluster2.rep[k]);   # Fast mode
                dist = euclidean_distance(cluster1.rep[i], cluster2.rep[k]);        # Slow mode
                if (dist < distance):
                    distance = dist;
                    
        return distance;
