"""!

@brief Cluster analysis algorithm: K-Means
@details Based on book description:
         - J.B.MacQueen. Some Methods for Classification and Analysis of Multivariate Observations. 1967.

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


import numpy;

import matplotlib.pyplot as plt;

import pyclustering.core.kmeans_wrapper as wrapper;

from pyclustering.core.wrapper import ccore_library;

from pyclustering.cluster.encoder import type_encoding;
from pyclustering.cluster import cluster_visualizer;


class kmeans_observer:
    """!
    @brief Observer of K-Means algorithm that is used to collect information about clustering process on each iteration of the algorithm.
    
    @see kmeans
    
    """
    
    def __init__(self, evolution_clusters = [], evolution_centers = []):
        """!
        @brief Initializer of observer of K-Means algorithm.
        
        @param[in] evolution_clusters (array_like): Evolution of clusters changes during clustering process.
        @param[in] evolution_centers (array_like): Evolution of centers changes during clustering process.
        
        """
        self.__evolution_clusters   = [];
        self.__evolution_centers    = [];


    def __len__(self):
        """!
        @brief Returns amount of steps that were observer during clustering process in K-Means algorithm.
        
        """
        return len(self.__evolution_clusters);


    def notify(self, clusters, centers):
        """!
        @brief This method is called by K-Means algorithm to notify about changes.
        
        @param[in] clusters (array_like): Allocated clusters by K-Means algorithm.
        @param[in] centers (array_like): Allocated centers by K-Means algorithm.
        
        """
        self.__evolution_clusters.append(clusters);
        self.__evolution_clusters.append(centers);


    def get_centers(self, iteration):
        """!
        @brief Get method to return centers at specific iteration of clustering process.
        
        @param[in] iteration (uint): Clustering process iteration at which centers are required.
        
        @return (array_like) Centers at specific iteration.
        
        """
        return self.__evolution_centers[iteration];


    def get_clusters(self, iteration):
        """!
        @brief Get method to return allocated clusters at specific iteration of clustering process.
        
        @param[in] iteration (uint): Clustering process iteration at which clusters are required.
        
        @return (array_like) Clusters at specific iteration.
        
        """
        return self.__evolution_clusters[iteration];



class kmeans_visualizer:
    """!
    @brief Visualizer of K-Means algorithm's results.
    @details K-Means visualizer provides visualization services that are specific for K-Means algorithm.
    
    """
    
    __default_2d_marker_size = 15;
    __default_3d_marker_size = 70;
    
    
    @staticmethod
    def show_clusters(sample, clusters, centers, initial_centers = None, **kwargs):
        """!
        @brief Display K-Means clustering results.
        
        @param[in] sample (list): Dataset that were used for clustering.
        @param[in] clusters (array_like): Clusters that were allocated by the algorithm.
        @param[in] centers (array_like): Centers that were allocated by the algorithm.
        @param[in] initial_centers (array_like): Initial centers that were used by the algorithm, if 'None' then initial centers are not displyed.
        @param[in] **kwargs: Arbitrary keyword arguments (available arguments: 'figure', 'display').
        
        Keyword Args:
            figure (figure): If 'None' then new is figure is creater, otherwise specified figure is used for visualization.
            display (bool): If 'True' then figure will be shown by the method, otherwise it should be shown manually using matplotlib function 'plt.show()'.
            offset (uint): Specify axes index on the figure where results should be drawn (only if argument 'figure' is specified).
        
        @return (figure) Figure where clusters were drawn.
        
        """

        visualizer = cluster_visualizer();
        visualizer.append_clusters(clusters, sample);
        
        offset = kmeans_visualizer.__get_argument('offset', 0, **kwargs);
        
        if (kmeans_visualizer.__get_argument('figure', None, **kwargs) is None):
            figure = visualizer.show(display = False);
        else:
            visualizer.show(figure = figure, display = False);
        
        kmeans_visualizer.__draw_centers(figure, offset, visualizer, centers, initial_centers);
        kmeans_visualizer.__draw_rays(figure, offset, visualizer, sample, clusters, centers);
        
        if (kmeans_visualizer.__get_argument('display', True, **kwargs) is True):
            plt.show();

        return figure;


    @staticmethod
    def __draw_rays(figure, offset, visualizer, sample, clusters, centers):
        ax = figure.get_axes()[offset];
        
        for index_cluster in range(len(clusters)):
            color = visualizer.get_cluster_color(index_cluster, 0);
            kmeans_visualizer.__draw_cluster_rays(ax, color, sample, clusters[index_cluster], centers[index_cluster])


    @staticmethod
    def __draw_cluster_rays(ax, color, sample, cluster, center):
        dimension = len(sample[0]);
        
        for index_point in cluster:
            point = sample[index_point];
            if (dimension == 1):
                ax.plot([point[0], center[0]], [0.0, 0.0], '-', color=color, linewidth=0.5);
            elif (dimension == 2):
                ax.plot([point[0], center[0]], [point[1], center[1]], '-', color=color, linewidth=0.5);
            elif (dimension == 3):
                ax.plot([point[0], center[0]], [point[1], center[1]], [point[2], center[2]], '-', color=color, linewidth=0.5)


    @staticmethod
    def __draw_center(ax, center, color, marker, alpha):
        dimension = len(center);
        
        if (dimension == 1):
            ax.plot(center[0], 0.0, color=color, alpha=alpha, marker=marker, markersize=kmeans_visualizer.__default_2d_marker_size);
        elif (dimension == 2):
            ax.plot(center[0], center[1], color=color, alpha=alpha, marker=marker, markersize=kmeans_visualizer.__default_2d_marker_size);
        elif (dimension == 3):
            ax.scatter(center[0], center[1], center[2], c=color, alpha=alpha, marker=marker, s=kmeans_visualizer.__default_3d_marker_size);


    @staticmethod
    def __draw_centers(figure, offset, visualizer, centers, initial_centers):
        ax = figure.get_axes()[offset];
        
        for index_center in range(len(centers)):
            color = visualizer.get_cluster_color(index_center, 0);
            kmeans_visualizer.__draw_center(ax, centers[index_center], color, '*', 1.0);
            
            if initial_centers:
                kmeans_visualizer.__draw_center(ax, initial_centers[index_center], color, '*', 0.4);


    @staticmethod
    def __get_argument(argument_name, default_value, **kwargs):
        if (argument_name in kwargs):
            return kwargs[argument_name];
        
        return default_value;



class kmeans:
    """!
    @brief Class represents clustering algorithm K-Means.
    @details CCORE option can be used to use the pyclustering core - C/C++ shared library for processing that significantly increases performance.
    
             CCORE implementation of the algorithm uses thread pool to parallelize the clustering process.
             
             K-Means clustering results depend on initial centers. Algorithm K-Means++ can used for initialization 
             initial centers from module 'pyclustering.cluster.center_initializer'.
    
    Example #1 - Trivial clustering:
    @code
        # load list of points for cluster analysis
        sample = read_sample(path);
        
        # create instance of K-Means algorithm
        kmeans_instance = kmeans(sample, [ [0.0, 0.1], [2.5, 2.6] ]);
        
        # run cluster analysis and obtain results
        kmeans_instance.process();
        clusters = kmeans_instance.get_clusters();
    @endcode
    
    Example #2 - Clustering using K-Means++ for center initialization:
    @code
        # load list of points for cluster analysis
        sample = read_sample(SIMPLE_SAMPLES.SAMPLE_SIMPLE2);
        
        # initialize initial centers using K-Means++ method
        initial_centers = kmeans_plusplus_initializer(sample, 3).initialize();
        
        # create instance of K-Means algorithm with prepared centers
        kmeans_instance = kmeans(sample, initial_centers);
        
        # run cluster analysis and obtain results
        kmeans_instance.process();
        clusters = kmeans_instance.get_clusters();
        final_centers = kmeans_instance.get_centers();
    @endcode
    
    @see center_initializer
    
    """
    
    def __init__(self, data, initial_centers, tolerance = 0.001, ccore = True, **kwargs):
        """!
        @brief Constructor of clustering algorithm K-Means.
        @details Center initializer can be used for creating initial centers, for example, K-Means++ method.
        
        @param[in] data (array_like): Input data that is presented as array of points (objects), each point should be represented by array_like data structure.
        @param[in] initial_centers (array_like): Initial coordinates of centers of clusters that are represented by array_like data structure: [center1, center2, ...].
        @param[in] tolerance (double): Stop condition: if maximum value of change of centers of clusters is less than tolerance then algorithm stops processing.
        @param[in] ccore (bool): Defines should be CCORE library (C++ pyclustering library) used instead of Python code or not.
        @param[in] **kwargs: Arbitrary keyword arguments (available arguments: 'observer').
        
        Keyword Args:
            observer (kmeans_observer): Observer of the algorithm to collect information about clustering process on each iteration.
        
        @see center_initializer
        
        """
        self.__pointer_data = numpy.matrix(data);
        self.__clusters = [];
        self.__centers = numpy.matrix(initial_centers);
        self.__tolerance = tolerance;
        
        self.__observer = None;
        if 'observer' in kwargs:
            self.__observer = kwargs['observer'];
        
        self.__ccore = ccore;
        if (self.__ccore):
            self.__ccore = ccore_library.workable();


    def process(self):
        """!
        @brief Performs cluster analysis in line with rules of K-Means algorithm.
        
        @remark Results of clustering can be obtained using corresponding get methods.
        
        @see get_clusters()
        @see get_centers()
        
        """
        
        if (self.__ccore is True):
            results = wrapper.kmeans(self.__pointer_data, self.__centers, self.__tolerance, (self.__observer is not None));
            self.__clusters = results[0];
            self.__centers  = results[1];
            
            if self.__observer:
                self.__observer = kmeans_observer(results[2], results[3]);
        else:
            maximum_change = float('inf');
             
            stop_condition = self.__tolerance * self.__tolerance;   # Fast solution
            #stop_condition = self.__tolerance;              # Slow solution
             
            # Check for dimension
            if (len(self.__pointer_data[0]) != len(self.__centers[0])):
                raise NameError('Dimension of the input data and dimension of the initial cluster centers must be equal.');
             
            while (maximum_change > stop_condition):
                self.__clusters = self.__update_clusters();
                updated_centers = self.__update_centers();  # changes should be calculated before asignment
                
                if self.__observer:
                    self.__observer.notify(self.__clusters, updated_centers);
                
                if (len(self.__centers) != len(updated_centers)):
                    maximum_change = float('inf');
                
                else:
                    changes = numpy.sum(numpy.square(self.__centers - updated_centers), axis=1);
                    maximum_change = numpy.max(changes);
                
                self.__centers = updated_centers;


    def get_clusters(self):
        """!
        @brief Returns list of allocated clusters, each cluster contains indexes of objects in list of data.
        
        @see process()
        @see get_centers()
        
        """
        
        return self.__clusters;
    
    
    def get_centers(self):
        """!
        @brief Returns list of centers of allocated clusters.
        
        @see process()
        @see get_clusters()
        
        """

        if isinstance(self.__centers, list):
            return self.__centers;
        
        return self.__centers.tolist();


    def get_cluster_encoding(self):
        """!
        @brief Returns clustering result representation type that indicate how clusters are encoded.
        
        @return (type_encoding) Clustering result representation.
        
        @see get_clusters()
        
        """
        
        return type_encoding.CLUSTER_INDEX_LIST_SEPARATION;


    def __update_clusters(self):
        """!
        @brief Calculate Euclidean distance to each point from the each cluster. Nearest points are captured by according clusters and as a result clusters are updated.
        
        @return (list) updated clusters as list of clusters. Each cluster contains indexes of objects from data.
        
        """
        
        clusters = [[] for _ in range(len(self.__centers))];
        
        dataset_differences = numpy.zeros((len(clusters), len(self.__pointer_data)));
        for index_center in range(len(self.__centers)):
            dataset_differences[index_center] = numpy.sum(numpy.square(self.__pointer_data - self.__centers[index_center]), axis=1).T;
        
        optimum_indexes = numpy.argmin(dataset_differences, axis=0);
        for index_point in range(len(optimum_indexes)):
            index_cluster = optimum_indexes[index_point];
            clusters[index_cluster].append(index_point);
        
        clusters = [cluster for cluster in clusters if len(cluster) > 0];
        
        return clusters;
    
    
    def __update_centers(self):
        """!
        @brief Calculate centers of clusters in line with contained objects.
        
        @return (numpy.matrix) Updated centers as list of centers.
        
        """
        
        dimension = self.__pointer_data.shape[1];
        centers = numpy.zeros((len(self.__clusters), dimension));
        
        for index in range(len(self.__clusters)):
            cluster_points = self.__pointer_data[self.__clusters[index], :];
            centers[index] = cluster_points.mean(axis=0);

        return numpy.matrix(centers);
