"""!

@brief The module contains K-Means algorithm and other related services.
@details Implementation based on paper @cite inproceedings::kmeans::1.

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
import warnings

try:
    import matplotlib.pyplot as plt
    import matplotlib.animation as animation
except Exception as error_instance:
    warnings.warn("Impossible to import matplotlib (please, install 'matplotlib'), pyclustering's visualization "
                  "functionality is not available (details: '%s')." % str(error_instance))

import pyclustering.core.kmeans_wrapper as wrapper

from pyclustering.core.wrapper import ccore_library
from pyclustering.core.metric_wrapper import metric_wrapper

from pyclustering.cluster.encoder import type_encoding
from pyclustering.cluster import cluster_visualizer

from pyclustering.utils.metric import distance_metric, type_metric


class kmeans_observer:
    """!
    @brief Observer of K-Means algorithm that is used to collect information about clustering process on each iteration of the algorithm.
    
    @see kmeans
    
    """
    
    def __init__(self):
        """!
        @brief Initializer of observer of K-Means algorithm.
        
        """
        self.__evolution_clusters = []
        self.__evolution_centers = []
        self.__initial_centers = []


    def __len__(self):
        """!
        @brief Returns amount of steps that were observer during clustering process in K-Means algorithm.
        
        """
        return len(self.__evolution_clusters)


    def notify(self, clusters, centers):
        """!
        @brief This method is called by K-Means algorithm to notify about changes.
        
        @param[in] clusters (array_like): Allocated clusters by K-Means algorithm.
        @param[in] centers (array_like): Allocated centers by K-Means algorithm.
        
        """
        self.__evolution_clusters.append(clusters)
        self.__evolution_centers.append(centers)


    def set_evolution_centers(self, evolution_centers):
        """!
        @brief Set evolution of changes of centers during clustering process.
        
        @param[in] evolution_centers (array_like): Evolution of changes of centers during clustering process.
        
        """
        self.__evolution_centers = evolution_centers


    def get_centers(self, iteration):
        """!
        @brief Get method to return centers at specific iteration of clustering process.
        
        @param[in] iteration (uint): Clustering process iteration at which centers are required.
        
        @return (array_like) Centers at specific iteration.
        
        """
        return self.__evolution_centers[iteration]


    def set_evolution_clusters(self, evolution_clusters):
        """!
        @brief Set evolution of changes of centers during clustering process.
        
        @param[in] evolution_clusters (array_like): Evolution of changes of clusters during clustering process.
        
        """
        self.__evolution_clusters = evolution_clusters


    def get_clusters(self, iteration):
        """!
        @brief Get method to return allocated clusters at specific iteration of clustering process.
        
        @param[in] iteration (uint): Clustering process iteration at which clusters are required.
        
        @return (array_like) Clusters at specific iteration.
        
        """
        return self.__evolution_clusters[iteration]



class kmeans_visualizer:
    """!
    @brief Visualizer of K-Means algorithm's results.
    @details K-Means visualizer provides visualization services that are specific for K-Means algorithm.
    
    """
    
    __default_2d_marker_size = 15
    __default_3d_marker_size = 70
    
    
    @staticmethod
    def show_clusters(sample, clusters, centers, initial_centers = None, **kwargs):
        """!
        @brief Display K-Means clustering results.
        
        @param[in] sample (list): Dataset that was used for clustering.
        @param[in] clusters (array_like): Clusters that were allocated by the algorithm.
        @param[in] centers (array_like): Centers that were allocated by the algorithm.
        @param[in] initial_centers (array_like): Initial centers that were used by the algorithm, if 'None' then initial centers are not displyed.
        @param[in] **kwargs: Arbitrary keyword arguments (available arguments: 'figure', 'display', 'offset').
        
        <b>Keyword Args:</b><br>
            - figure (figure): If 'None' then new is figure is created, otherwise specified figure is used for visualization.
            - display (bool): If 'True' then figure will be shown by the method, otherwise it should be shown manually using matplotlib function 'plt.show()'.
            - offset (uint): Specify axes index on the figure where results should be drawn (only if argument 'figure' is specified).
        
        @return (figure) Figure where clusters were drawn.
        
        """

        visualizer = cluster_visualizer()
        visualizer.append_clusters(clusters, sample)
        
        offset = kwargs.get('offset', 0)
        figure = kwargs.get('figure', None)
        display = kwargs.get('display', True)

        if figure is None:
            figure = visualizer.show(display=False)
        else:
            visualizer.show(figure=figure, display=False)
        
        kmeans_visualizer.__draw_centers(figure, offset, visualizer, centers, initial_centers)
        kmeans_visualizer.__draw_rays(figure, offset, visualizer, sample, clusters, centers)
        
        if display is True:
            plt.show()

        return figure


    @staticmethod
    def __draw_rays(figure, offset, visualizer, sample, clusters, centers):
        ax = figure.get_axes()[offset]
        
        for index_cluster in range(len(clusters)):
            color = visualizer.get_cluster_color(index_cluster, 0)
            kmeans_visualizer.__draw_cluster_rays(ax, color, sample, clusters[index_cluster], centers[index_cluster])


    @staticmethod
    def __draw_cluster_rays(ax, color, sample, cluster, center):
        dimension = len(sample[0])
        
        for index_point in cluster:
            point = sample[index_point]
            if dimension == 1:
                ax.plot([point[0], center[0]], [0.0, 0.0], '-', color=color, linewidth=0.5)
            elif dimension == 2:
                ax.plot([point[0], center[0]], [point[1], center[1]], '-', color=color, linewidth=0.5)
            elif dimension == 3:
                ax.plot([point[0], center[0]], [point[1], center[1]], [point[2], center[2]], '-', color=color, linewidth=0.5)


    @staticmethod
    def __draw_center(ax, center, color, marker, alpha):
        dimension = len(center)
        
        if dimension == 1:
            ax.plot(center[0], 0.0, color=color, alpha=alpha, marker=marker, markersize=kmeans_visualizer.__default_2d_marker_size)
        elif dimension == 2:
            ax.plot(center[0], center[1], color=color, alpha=alpha, marker=marker, markersize=kmeans_visualizer.__default_2d_marker_size)
        elif dimension == 3:
            ax.scatter(center[0], center[1], center[2], c=color, alpha=alpha, marker=marker, s=kmeans_visualizer.__default_3d_marker_size)


    @staticmethod
    def __draw_centers(figure, offset, visualizer, centers, initial_centers):
        ax = figure.get_axes()[offset]
        
        for index_center in range(len(centers)):
            color = visualizer.get_cluster_color(index_center, 0)
            kmeans_visualizer.__draw_center(ax, centers[index_center], color, '*', 1.0)
            
            if initial_centers is not None:
                kmeans_visualizer.__draw_center(ax, initial_centers[index_center], color, '*', 0.4)


    @staticmethod
    def animate_cluster_allocation(data, observer, animation_velocity=500, movie_fps=1, save_movie=None):
        """!
        @brief Animates clustering process that is performed by K-Means algorithm.

        @param[in] data (list): Dataset that is used for clustering.
        @param[in] observer (kmeans_observer): EM observer that was used for collection information about clustering process.
        @param[in] animation_velocity (uint): Interval between frames in milliseconds (for run-time animation only).
        @param[in] movie_fps (uint): Defines frames per second (for rendering movie only).
        @param[in] save_movie (string): If it is specified then animation will be stored to file that is specified in this parameter.

        """
        figure = plt.figure()

        def init_frame():
            return frame_generation(0)

        def frame_generation(index_iteration):
            figure.clf()

            figure.suptitle("K-Means algorithm (iteration: " + str(index_iteration) + ")", fontsize=18, fontweight='bold')

            clusters = observer.get_clusters(index_iteration)
            centers = observer.get_centers(index_iteration)
            kmeans_visualizer.show_clusters(data, clusters, centers, None, figure=figure, display=False)

            figure.subplots_adjust(top=0.85)

            return [figure.gca()]

        iterations = len(observer)
        cluster_animation = animation.FuncAnimation(figure, frame_generation, iterations, interval=animation_velocity,
                                                    init_func=init_frame, repeat_delay=5000)

        if save_movie is not None:
            cluster_animation.save(save_movie, writer='ffmpeg', fps=movie_fps, bitrate=3000)
        else:
            plt.show()



class kmeans:
    """!
    @brief Class implements K-Means clustering algorithm.
    @details K-Means clustering aims to partition n observations into k clusters in which each observation belongs to
              the cluster with the nearest mean, serving as a prototype of the cluster. This results in a partitioning
              of the data space into Voronoi cells.

    K-Means clustering results depend on initial centers. Algorithm K-Means++ can used for initialization of
    initial centers - see module 'pyclustering.cluster.center_initializer'.

    CCORE implementation (C/C++ part of the library) of the algorithm performs parallel processing to ensure maximum
    performance.

    Implementation based on the paper @cite inproceedings::kmeans::1.

    @image html kmeans_example_clustering.png "K-Means clustering results. At the left - 'Simple03.data' sample, at the right - 'Lsun.data' sample."

    Example #1 - Clustering using K-Means++ for center initialization:
    @code
        from pyclustering.cluster.kmeans import kmeans, kmeans_visualizer
        from pyclustering.cluster.center_initializer import kmeans_plusplus_initializer
        from pyclustering.samples.definitions import FCPS_SAMPLES
        from pyclustering.utils import read_sample

        # Load list of points for cluster analysis.
        sample = read_sample(FCPS_SAMPLES.SAMPLE_TWO_DIAMONDS)

        # Prepare initial centers using K-Means++ method.
        initial_centers = kmeans_plusplus_initializer(sample, 2).initialize()

        # Create instance of K-Means algorithm with prepared centers.
        kmeans_instance = kmeans(sample, initial_centers)

        # Run cluster analysis and obtain results.
        kmeans_instance.process()
        clusters = kmeans_instance.get_clusters()
        final_centers = kmeans_instance.get_centers()

        # Visualize obtained results
        kmeans_visualizer.show_clusters(sample, clusters, final_centers)
    @endcode

    Example #2 - Clustering using specific distance metric, for example, Manhattan distance:
    @code
        # prepare input data and initial centers for cluster analysis using K-Means

        # create metric that will be used for clustering
        manhattan_metric = distance_metric(type_metric.MANHATTAN)

        # create instance of K-Means using specific distance metric:
        kmeans_instance = kmeans(sample, initial_centers, metric=manhattan_metric)

        # run cluster analysis and obtain results
        kmeans_instance.process()
        clusters = kmeans_instance.get_clusters()
    @endcode

    @see center_initializer
    
    """
    
    def __init__(self, data, initial_centers, tolerance=0.001, ccore=True, **kwargs):
        """!
        @brief Constructor of clustering algorithm K-Means.
        @details Center initializer can be used for creating initial centers, for example, K-Means++ method.
        
        @param[in] data (array_like): Input data that is presented as array of points (objects), each point should be represented by array_like data structure.
        @param[in] initial_centers (array_like): Initial coordinates of centers of clusters that are represented by array_like data structure: [center1, center2, ...].
        @param[in] tolerance (double): Stop condition: if maximum value of change of centers of clusters is less than tolerance then algorithm stops processing.
        @param[in] ccore (bool): Defines should be CCORE library (C++ pyclustering library) used instead of Python code or not.
        @param[in] **kwargs: Arbitrary keyword arguments (available arguments: 'observer', 'metric', 'itermax').
        
        <b>Keyword Args:</b><br>
            - observer (kmeans_observer): Observer of the algorithm to collect information about clustering process on each iteration.
            - metric (distance_metric): Metric that is used for distance calculation between two points (by default euclidean square distance).
            - itermax (uint): Maximum number of iterations that is used for clustering process (by default: 200).
        
        @see center_initializer
        
        """
        self.__pointer_data = numpy.array(data)
        self.__clusters = []
        self.__centers = numpy.array(initial_centers)
        self.__tolerance = tolerance
        self.__total_wce = 0.0

        self.__observer = kwargs.get('observer', None)
        self.__metric = kwargs.get('metric', distance_metric(type_metric.EUCLIDEAN_SQUARE))
        self.__itermax = kwargs.get('itermax', 100)

        if self.__metric.get_type() != type_metric.USER_DEFINED:
            self.__metric.enable_numpy_usage()
        else:
            self.__metric.disable_numpy_usage()
        
        self.__ccore = ccore and self.__metric.get_type() != type_metric.USER_DEFINED
        if self.__ccore is True:
            self.__ccore = ccore_library.workable()

        self.__verify_arguments()


    def process(self):
        """!
        @brief Performs cluster analysis in line with rules of K-Means algorithm.

        @return (kmeans) Returns itself (K-Means instance).
        
        @see get_clusters()
        @see get_centers()
        
        """

        if len(self.__pointer_data[0]) != len(self.__centers[0]):
            raise ValueError("Dimension of the input data and dimension of the initial cluster centers must be equal.")

        if self.__ccore is True:
            self.__process_by_ccore()
        else:
            self.__process_by_python()

        return self


    def __process_by_ccore(self):
        """!
        @brief Performs cluster analysis using CCORE (C/C++ part of pyclustering library).

        """
        ccore_metric = metric_wrapper.create_instance(self.__metric)

        results = wrapper.kmeans(self.__pointer_data, self.__centers, self.__tolerance, self.__itermax, (self.__observer is not None), ccore_metric.get_pointer())
        self.__clusters = results[0]
        self.__centers = results[1]

        if self.__observer is not None:
            self.__observer.set_evolution_clusters(results[2])
            self.__observer.set_evolution_centers(results[3])

        self.__total_wce = results[4][0]


    def __process_by_python(self):
        """!
        @brief Performs cluster analysis using python code.

        """

        maximum_change = float('inf')
        iteration = 0

        if self.__observer is not None:
            initial_clusters = self.__update_clusters()
            self.__observer.notify(initial_clusters, self.__centers.tolist())

        while maximum_change > self.__tolerance and iteration < self.__itermax:
            self.__clusters = self.__update_clusters()
            updated_centers = self.__update_centers()  # changes should be calculated before assignment

            if self.__observer is not None:
                self.__observer.notify(self.__clusters, updated_centers.tolist())

            maximum_change = self.__calculate_changes(updated_centers)

            self.__centers = updated_centers    # assign center after change calculation
            iteration += 1

        self.__calculate_total_wce()


    def predict(self, points):
        """!
        @brief Calculates the closest cluster to each point.

        @param[in] points (array_like): Points for which closest clusters are calculated.

        @return (list) List of closest clusters for each point. Each cluster is denoted by index. Return empty
                 collection if 'process()' method was not called.

        """

        nppoints = numpy.array(points)
        if len(self.__clusters) == 0:
            return []

        differences = numpy.zeros((len(nppoints), len(self.__centers)))
        for index_point in range(len(nppoints)):
            if self.__metric.get_type() != type_metric.USER_DEFINED:
                differences[index_point] = self.__metric(nppoints[index_point], self.__centers)
            else:
                differences[index_point] = [ self.__metric(nppoints[index_point], center) for center in self.__centers ]

        return numpy.argmin(differences, axis=1)


    def get_clusters(self):
        """!
        @brief Returns list of allocated clusters, each cluster contains indexes of objects in list of data.
        
        @see process()
        @see get_centers()
        
        """
        
        return self.__clusters


    def get_centers(self):
        """!
        @brief Returns list of centers of allocated clusters.
        
        @see process()
        @see get_clusters()
        
        """

        if isinstance(self.__centers, list):
            return self.__centers
        
        return self.__centers.tolist()


    def get_total_wce(self):
        """!
        @brief Returns sum of metric errors that depends on metric that was used for clustering (by default SSE - Sum of Squared Errors).
        @details Sum of metric errors is calculated using distance between point and its center:
                 \f[error=\sum_{i=0}^{N}distance(x_{i}-center(x_{i}))\f]

        @see process()
        @see get_clusters()

        """

        return self.__total_wce


    def get_cluster_encoding(self):
        """!
        @brief Returns clustering result representation type that indicate how clusters are encoded.
        
        @return (type_encoding) Clustering result representation.
        
        @see get_clusters()
        
        """
        
        return type_encoding.CLUSTER_INDEX_LIST_SEPARATION


    def __update_clusters(self):
        """!
        @brief Calculate distance (in line with specified metric) to each point from the each cluster. Nearest points
                are captured by according clusters and as a result clusters are updated.
        
        @return (list) Updated clusters as list of clusters. Each cluster contains indexes of objects from data.
        
        """
        
        clusters = [[] for _ in range(len(self.__centers))]
        
        dataset_differences = self.__calculate_dataset_difference(len(clusters))
        
        optimum_indexes = numpy.argmin(dataset_differences, axis=0)
        for index_point in range(len(optimum_indexes)):
            index_cluster = optimum_indexes[index_point]
            clusters[index_cluster].append(index_point)
        
        clusters = [cluster for cluster in clusters if len(cluster) > 0]

        return clusters


    def __update_centers(self):
        """!
        @brief Calculate centers of clusters in line with contained objects.
        
        @return (numpy.array) Updated centers.
        
        """
        
        dimension = self.__pointer_data.shape[1]
        centers = numpy.zeros((len(self.__clusters), dimension))
        
        for index in range(len(self.__clusters)):
            cluster_points = self.__pointer_data[self.__clusters[index], :]
            centers[index] = cluster_points.mean(axis=0)

        return numpy.array(centers)


    def __calculate_total_wce(self):
        """!
        @brief Calculate total within cluster errors that is depend on metric that was chosen for K-Means algorithm.

        """

        dataset_differences = self.__calculate_dataset_difference(len(self.__clusters))

        self.__total_wce = 0
        for index_cluster in range(len(self.__clusters)):
            for index_point in self.__clusters[index_cluster]:
                self.__total_wce += dataset_differences[index_cluster][index_point]


    def __calculate_dataset_difference(self, amount_clusters):
        """!
        @brief Calculate distance from each point to each cluster center.

        """
        dataset_differences = numpy.zeros((amount_clusters, len(self.__pointer_data)))
        for index_center in range(amount_clusters):
            if self.__metric.get_type() != type_metric.USER_DEFINED:
                dataset_differences[index_center] = self.__metric(self.__pointer_data, self.__centers[index_center])
            else:
                dataset_differences[index_center] = [ self.__metric(point, self.__centers[index_center])
                                                      for point in self.__pointer_data ]

        return dataset_differences


    def __calculate_changes(self, updated_centers):
        """!
        @brief Calculates changes estimation between previous and current iteration using centers for that purpose.

        @param[in] updated_centers (array_like): New cluster centers.

        @return (float) Maximum changes between centers.

        """
        if len(self.__centers) != len(updated_centers):
            maximum_change = float('inf')

        else:
            changes = self.__metric(self.__centers, updated_centers)
            maximum_change = numpy.max(changes)

        return maximum_change


    def __verify_arguments(self):
        """!
        @brief Verify input parameters for the algorithm and throw exception in case of incorrectness.

        """
        if len(self.__pointer_data) == 0:
            raise ValueError("Input data is empty (size: '%d')." % len(self.__pointer_data))

        if len(self.__centers) == 0:
            raise ValueError("Initial centers are empty (size: '%d')." % len(self.__pointer_data))

        if self.__tolerance < 0:
            raise ValueError("Tolerance (current value: '%d') should be greater or equal to 0." %
                             self.__tolerance)

        if self.__itermax < 0:
            raise ValueError("Maximum iterations (current value: '%d') should be greater or equal to 0." %
                             self.__tolerance)
