"""!

@brief Cluster analysis algorithm: Expectation-Maximization Algorithm for Gaussian Mixture Model.
@details Implementation based on paper @cite article::ema::1.

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
import random
import warnings

from pyclustering.cluster import cluster_visualizer
from pyclustering.cluster.center_initializer import kmeans_plusplus_initializer
from pyclustering.cluster.kmeans import kmeans

from pyclustering.utils import pi, calculate_ellipse_description, euclidean_distance_square

from enum import IntEnum

try:
    import matplotlib.pyplot as plt
    import matplotlib.animation as animation
    from matplotlib import patches
except Exception as error_instance:
    warnings.warn("Impossible to import matplotlib (please, install 'matplotlib'), pyclustering's visualization "
                  "functionality is not available (details: '%s')." % str(error_instance))

def gaussian(data, mean, covariance):
    """!
    @brief Calculates gaussian for dataset using specified mean (mathematical expectation) and variance or covariance in case
            multi-dimensional data.
    
    @param[in] data (list): Data that is used for gaussian calculation.
    @param[in] mean (float|numpy.array): Mathematical expectation used for calculation.
    @param[in] covariance (float|numpy.array): Variance or covariance matrix for calculation.
    
    @return (list) Value of gaussian function for each point in dataset.
    
    """
    dimension = float(len(data[0]))
 
    if dimension != 1.0:
        inv_variance = numpy.linalg.pinv(covariance)
    else:
        inv_variance = 1.0 / covariance
    
    divider = (pi * 2.0) ** (dimension / 2.0) * numpy.sqrt(numpy.linalg.norm(covariance))
    if divider != 0.0:
        right_const = 1.0 / divider
    else:
        right_const = float('inf')
    
    result = []
    
    for point in data:
        mean_delta = point - mean
        point_gaussian = right_const * numpy.exp( -0.5 * mean_delta.dot(inv_variance).dot(numpy.transpose(mean_delta)) )
        result.append(point_gaussian)
    
    return result



class ema_init_type(IntEnum):
    """!
    @brief Enumeration of initialization types for Expectation-Maximization algorithm.
    
    """
    
    ## Means are randomly taken from input dataset and variance or covariance is calculated based on
    ## spherical data that belongs to the chosen means.
    RANDOM_INITIALIZATION = 0
    
    ## Two step initialization. The first is calculation of initial centers using K-Means++ method.
    ## The second is K-Means clustering using obtained centers in the first step. Obtained clusters
    ## and its centers are used for calculation of variance (covariance in case of multi-dimensional)
    ## data.
    KMEANS_INITIALIZATION = 1



class ema_initializer():
    """!
    @brief Provides servies for preparing initial means and covariances for Expectation-Maximization algorithm.
    @details Initialization strategy is defined by enumerator 'ema_init_type': random initialization and 
              kmeans with kmeans++ initialization. Here an example of initialization using kmeans strategy:
    
    @code
        from pyclustering.utils import read_sample
        from pyclustering.samples.definitions import FAMOUS_SAMPLES
        from pyclustering.cluster.ema import ema_initializer

        sample = read_sample(FAMOUS_SAMPLES.SAMPLE_OLD_FAITHFUL)
        amount_clusters = 2

        initial_means, initial_covariance = ema_initializer(sample, amount_clusters).initialize()
        print(initial_means)
        print(initial_covariance)
    @endcode
    
    """
    
    __MAX_GENERATION_ATTEMPTS = 10
    
    def __init__(self, sample, amount):
        """!
        @brief Constructs EM initializer.
        
        @param[in] sample (list): Data that will be used by the EM algorithm.
        @param[in] amount (uint): Amount of clusters that should be allocated by the EM algorithm.
        
        """
        self.__sample = sample
        self.__amount = amount


    def initialize(self, init_type = ema_init_type.KMEANS_INITIALIZATION):
        """!
        @brief Calculates initial parameters for EM algorithm: means and covariances using
                specified strategy.
        
        @param[in] init_type (ema_init_type): Strategy for initialization.
        
        @return (float|list, float|numpy.array) Initial means and variance (covariance matrix in case multi-dimensional data).
        
        """
        if init_type == ema_init_type.KMEANS_INITIALIZATION:
            return self.__initialize_kmeans()
        
        elif init_type == ema_init_type.RANDOM_INITIALIZATION:
            return self.__initialize_random()
        
        raise NameError("Unknown type of EM algorithm initialization is specified.")


    def __calculate_initial_clusters(self, centers):
        """!
        @brief Calculate Euclidean distance to each point from the each cluster. 
        @brief Nearest points are captured by according clusters and as a result clusters are updated.
        
        @return (list) updated clusters as list of clusters. Each cluster contains indexes of objects from data.
        
        """
        
        clusters = [[] for _ in range(len(centers))]
        for index_point in range(len(self.__sample)):
            index_optim, dist_optim = -1, 0.0
             
            for index in range(len(centers)):
                dist = euclidean_distance_square(self.__sample[index_point], centers[index])
                 
                if (dist < dist_optim) or (index is 0):
                    index_optim, dist_optim = index, dist
             
            clusters[index_optim].append(index_point)
        
        return clusters


    def __calculate_initial_covariances(self, initial_clusters):
        covariances = []
        for initial_cluster in initial_clusters:
            if len(initial_cluster) > 1:
                cluster_sample = [ self.__sample[index_point] for index_point in initial_cluster ]
                covariances.append(numpy.cov(cluster_sample, rowvar = False))
            else:
                dimension = len(self.__sample[0])
                covariances.append(numpy.zeros((dimension, dimension)) + random.random() / 10.0)
        
        return covariances


    def __initialize_random(self):
        initial_means = []
        
        for _ in range(self.__amount):
            mean = self.__sample[ random.randint(0, len(self.__sample)) - 1 ]
            attempts = 0
            while (mean in initial_means) and (attempts < ema_initializer.__MAX_GENERATION_ATTEMPTS):
                mean = self.__sample[ random.randint(0, len(self.__sample)) - 1 ]
                attempts += 1
            
            if attempts == ema_initializer.__MAX_GENERATION_ATTEMPTS:
                mean = [ value + (random.random() - 0.5) * value * 0.2 for value in mean ]
            
            initial_means.append(mean)
        
        initial_clusters = self.__calculate_initial_clusters(initial_means)
        initial_covariance = self.__calculate_initial_covariances(initial_clusters)
        
        return initial_means, initial_covariance


    def __initialize_kmeans(self):
        initial_centers = kmeans_plusplus_initializer(self.__sample, self.__amount).initialize()
        kmeans_instance = kmeans(self.__sample, initial_centers, ccore = True)
        kmeans_instance.process()
        
        means = kmeans_instance.get_centers()
        
        covariances = []
        initial_clusters = kmeans_instance.get_clusters()
        for initial_cluster in initial_clusters:
            if len(initial_cluster) > 1:
                cluster_sample = [ self.__sample[index_point] for index_point in initial_cluster ]
                covariances.append(numpy.cov(cluster_sample, rowvar = False))
            else:
                dimension = len(self.__sample[0])
                covariances.append(numpy.zeros((dimension, dimension))  + random.random() / 10.0)
        
        return means, covariances



class ema_observer:
    """!
    @brief Observer of EM algorithm for collecting algorithm state on each step.
    @details It can be used to obtain whole picture about clustering process of EM algorithm. Allocated clusters,
              means and covariances are stored in observer on each step. Here an example of usage:
    
    @code
        from pyclustering.cluster.ema import ema, ema_observer
        from pyclustering.utils import read_sample
        from pyclustering.samples.definitions import SIMPLE_SAMPLES

        # Read data from text file.
        sample = read_sample(SIMPLE_SAMPLES.SAMPLE_SIMPLE3)

        # Create EM observer.
        observer = ema_observer()

        # Create EM algorithm to allocated four clusters and pass observer to it.
        ema_instance = ema(sample, 4, observer=observer)

        # Run clustering process.
        ema_instance.process()

        # Print amount of steps that were done by the algorithm.
        print("EMA steps:", observer.get_iterations())

        # Print evolution of means and covariances.
        print("Means evolution:", observer.get_evolution_means())
        print("Covariances evolution:", observer.get_evolution_covariances())

        # Print evolution of clusters.
        print("Clusters evolution:", observer.get_evolution_clusters())

        # Print final clusters.
        print("Allocated clusters:", observer.get_evolution_clusters()[-1])
    @endcode
    
    """
    def __init__(self):
        """!
        @brief Initializes EM observer.
        
        """
        self.__means_evolution = []
        self.__covariances_evolution = []
        self.__clusters_evolution = []


    def __len__(self):
        """!
        @return (uint) Amount of iterations that were done by the EM algorithm.
        
        """
        return len(self.__means_evolution)


    def get_iterations(self):
        """!
        @return (uint) Amount of iterations that were done by the EM algorithm.
        
        """
        return len(self.__means_evolution)


    def get_evolution_means(self):
        """!
        @return (list) Mean of each cluster on each step of clustering.
        
        """
        return self.__means_evolution


    def get_evolution_covariances(self):
        """!
        @return (list) Covariance matrix (or variance in case of one-dimensional data) of each cluster on each step of clustering.
        
        """
        return self.__covariances_evolution


    def get_evolution_clusters(self):
        """!
        @return (list) Allocated clusters on each step of clustering.
        
        """
        return self.__clusters_evolution


    def notify(self, means, covariances, clusters):
        """!
        @brief This method is used by the algorithm to notify observer about changes where the algorithm
                should provide new values: means, covariances and allocated clusters.
        
        @param[in] means (list): Mean of each cluster on currect step.
        @param[in] covariances (list): Covariances of each cluster on current step.
        @param[in] clusters (list): Allocated cluster on current step.
        
        """
        self.__means_evolution.append(means)
        self.__covariances_evolution.append(covariances)
        self.__clusters_evolution.append(clusters)



class ema_visualizer:
    """!
    @brief Visualizer of EM algorithm's results.
    @details Provides services for visualization of particular features of the algorithm, for example,
              in case of two-dimensional dataset it shows covariance ellipses.
    
    """
    
    @staticmethod
    def show_clusters(clusters, sample, covariances, means, figure = None, display = True):
        """!
        @brief Draws clusters and in case of two-dimensional dataset draws their ellipses.
        
        @param[in] clusters (list): Clusters that were allocated by the algorithm.
        @param[in] sample (list): Dataset that were used for clustering.
        @param[in] covariances (list): Covariances of the clusters.
        @param[in] means (list): Means of the clusters.
        @param[in] figure (figure): If 'None' then new is figure is creater, otherwise specified figure is used
                    for visualization.
        @param[in] display (bool): If 'True' then figure will be shown by the method, otherwise it should be
                    shown manually using matplotlib function 'plt.show()'.
        
        @return (figure) Figure where clusters were drawn.
        
        """
        
        visualizer = cluster_visualizer()
        visualizer.append_clusters(clusters, sample)
        
        if figure is None:
            figure = visualizer.show(display = False)
        else:
            visualizer.show(figure = figure, display = False)
        
        if len(sample[0]) == 2:
            ema_visualizer.__draw_ellipses(figure, visualizer, clusters, covariances, means)

        if display is True:
            plt.show()

        return figure


    @staticmethod
    def animate_cluster_allocation(data, observer, animation_velocity = 75, movie_fps = 1, save_movie = None):
        """!
        @brief Animates clustering process that is performed by EM algorithm.
        
        @param[in] data (list): Dataset that is used for clustering.
        @param[in] observer (ema_observer): EM observer that was used for collection information about clustering process.
        @param[in] animation_velocity (uint): Interval between frames in milliseconds (for run-time animation only).
        @param[in] movie_fps (uint): Defines frames per second (for rendering movie only).
        @param[in] save_movie (string): If it is specified then animation will be stored to file that is specified in this parameter.
        
        """
        
        figure = plt.figure()
        
        def init_frame():
            return frame_generation(0)
        
        def frame_generation(index_iteration):
            figure.clf()
            
            figure.suptitle("EM algorithm (iteration: " + str(index_iteration) +")", fontsize = 18, fontweight = 'bold')
            
            clusters = observer.get_evolution_clusters()[index_iteration]
            covariances = observer.get_evolution_covariances()[index_iteration]
            means = observer.get_evolution_means()[index_iteration]
            
            ema_visualizer.show_clusters(clusters, data, covariances, means, figure, False)
            figure.subplots_adjust(top = 0.85)
            
            return [ figure.gca() ]

        iterations = len(observer)
        cluster_animation = animation.FuncAnimation(figure, frame_generation, iterations, interval = animation_velocity, init_func = init_frame, repeat_delay = 5000)

        if save_movie is not None:
            cluster_animation.save(save_movie, writer = 'ffmpeg', fps = movie_fps, bitrate = 1500)
        else:
            plt.show()


    @staticmethod
    def __draw_ellipses(figure, visualizer, clusters, covariances, means):
        ax = figure.get_axes()[0]
        
        for index in range(len(clusters)):
            angle, width, height = calculate_ellipse_description(covariances[index])
            color = visualizer.get_cluster_color(index, 0)

            ema_visualizer.__draw_ellipse(ax, means[index][0], means[index][1], angle, width, height, color)


    @staticmethod
    def __draw_ellipse(ax, x, y, angle, width, height, color):
        if (width > 0.0) and (height > 0.0):
            ax.plot(x, y, color=color, marker='x', markersize=6)
            ellipse = patches.Ellipse((x, y), width, height, alpha=0.2, angle=-angle, linewidth=2, fill=True, zorder=2, color=color)
            ax.add_patch(ellipse)



class ema:
    """!
    @brief Expectation-Maximization clustering algorithm for Gaussian Mixture Model (GMM).
    @details The algorithm provides only clustering services (unsupervised learning).
              Here an example of data clustering process:
    @code
        from pyclustering.cluster.ema import ema, ema_visualizer
        from pyclustering.utils import read_sample
        from pyclustering.samples.definitions import FCPS_SAMPLES

        # Read data from text file.
        sample = read_sample(FCPS_SAMPLES.SAMPLE_LSUN)

        # Create EM algorithm to allocated four clusters.
        ema_instance = ema(sample, 3)

        # Run clustering process.
        ema_instance.process()

        # Get clustering results.
        clusters = ema_instance.get_clusters()
        covariances = ema_instance.get_covariances()
        means = ema_instance.get_centers()

        # Visualize obtained clustering results.
        ema_visualizer.show_clusters(clusters, sample, covariances, means)
    @endcode
    
    Here is clustering results of the Expectation-Maximization clustering algorithm where popular sample 'OldFaithful' was used.
    Initial random means and covariances were used in the example. The first step is presented on the left side of the figure and
    final result (the last step) is on the right side:
    @image html ema_old_faithful_clustering.png
    
    @see ema_visualizer
    @see ema_observer
    
    """
    def __init__(self, data, amount_clusters, means=None, variances=None, observer=None, tolerance=0.00001, iterations=100):
        """!
        @brief Initializes Expectation-Maximization algorithm for cluster analysis.
        
        @param[in] data (list): Dataset that should be analysed and where each point (object) is represented by the list of coordinates.
        @param[in] amount_clusters (uint): Amount of clusters that should be allocated.
        @param[in] means (list): Initial means of clusters (amount of means should be equal to amount of clusters for allocation).
                    If this parameter is 'None' then K-Means algorithm with K-Means++ method will be used for initialization by default.
        @param[in] variances (list): Initial cluster variances (or covariances in case of multi-dimensional data). Amount of
                    covariances should be equal to amount of clusters that should be allocated. If this parameter is 'None' then
                    K-Means algorithm with K-Means++ method will be used for initialization by default.
        @param[in] observer (ema_observer): Observer for gathering information about clustering process.
        @param[in] tolerance (float): Defines stop condition of the algorithm (when difference between current and
                    previous log-likelihood estimation is less then 'tolerance' then clustering is over).
        @param[in] iterations (uint): Additional stop condition parameter that defines maximum number of steps that can be
                    performed by the algorithm during clustering process.
        
        """
        
        self.__data = numpy.array(data)
        self.__amount_clusters = amount_clusters
        self.__tolerance = tolerance
        self.__iterations = iterations
        self.__observer = observer
        
        self.__means = means
        self.__variances = variances

        self.__verify_arguments()

        if (means is None) or (variances is None):
            self.__means, self.__variances = ema_initializer(data, amount_clusters).initialize(ema_init_type.KMEANS_INITIALIZATION)
            
            if len(self.__means) != amount_clusters:
                self.__amount_clusters = len(self.__means)
        
        self.__rc = [ [0.0] * len(self.__data) for _ in range(amount_clusters) ]
        self.__pic = [1.0] * amount_clusters
        self.__clusters = []
        self.__gaussians = [ [] for _ in range(amount_clusters) ]
        self.__stop = False


    def process(self):
        """!
        @brief Run clustering process of the algorithm.

        @return (ema) Returns itself (EMA instance).
        
        """
        
        previous_likelihood = -200000
        current_likelihood = -100000
        
        current_iteration = 0
        while(self.__stop is False) and (abs(previous_likelihood - current_likelihood) > self.__tolerance) and (current_iteration < self.__iterations):
            self.__expectation_step()
            self.__maximization_step()
            
            current_iteration += 1
            
            self.__extract_clusters()
            self.__notify()
            
            previous_likelihood = current_likelihood
            current_likelihood = self.__log_likelihood()
            self.__stop = self.__get_stop_condition()
        
        self.__normalize_probabilities()
        return self


    def get_clusters(self):
        """!
        @return (list) Allocated clusters where each cluster is represented by list of indexes of points from dataset,
                        for example, two cluster may have following representation [[0, 1, 4], [2, 3, 5, 6]].
        
        """
        return self.__clusters


    def get_centers(self):
        """!
        @return (list) Corresponding centers (means) of clusters.
        
        """
        
        return self.__means


    def get_covariances(self):
        """!
        @return (list) Corresponding variances (or covariances in case of multi-dimensional data) of clusters.
        
        """
        
        return self.__variances


    def get_probabilities(self):
        """!
        @brief Returns 2-dimensional list with belong probability of each object from data to cluster correspondingly,
                where that first index is for cluster and the second is for point.
        
        @code
            # Get belong probablities
            probabilities = ema_instance.get_probabilities();
            
            # Show porbability of the fifth element in the first and in the second cluster
            index_point = 5;
            print("Probability in the first cluster:", probabilities[0][index_point]);
            print("Probability in the first cluster:", probabilities[1][index_point]);
        @endcode
        
        @return (list) 2-dimensional list with belong probability of each object from data to cluster.
        
        """
        
        return self.__rc


    def __erase_empty_clusters(self):
        clusters, means, variances, pic, gaussians, rc = [], [], [], [], [], []

        for index_cluster in range(len(self.__clusters)):
            if len(self.__clusters[index_cluster]) > 0:
                clusters.append(self.__clusters[index_cluster])
                means.append(self.__means[index_cluster])
                variances.append(self.__variances[index_cluster])
                pic.append(self.__pic[index_cluster])
                gaussians.append(self.__gaussians[index_cluster])
                rc.append(self.__rc[index_cluster])
        
        if len(self.__clusters) != len(clusters):
            self.__clusters, self.__means, self.__variances, self.__pic = clusters, means, variances, pic
            self.__gaussians, self.__rc = gaussians, rc
            self.__amount_clusters = len(self.__clusters)


    def __notify(self):
        if self.__observer is not None:
            self.__observer.notify(self.__means, self.__variances, self.__clusters)


    def __extract_clusters(self):
        self.__clusters = [[] for _ in range(self.__amount_clusters)]
        for index_point in range(len(self.__data)):
            candidates = []
            for index_cluster in range(self.__amount_clusters):
                candidates.append((index_cluster, self.__rc[index_cluster][index_point]))
            
            index_winner = max(candidates, key=lambda candidate: candidate[1])[0]
            self.__clusters[index_winner].append(index_point)
        
        self.__erase_empty_clusters()


    def __log_likelihood(self):
        likelihood = 0.0
        
        for index_point in range(len(self.__data)):
            particle = 0.0
            for index_cluster in range(self.__amount_clusters):
                particle += self.__pic[index_cluster] * self.__gaussians[index_cluster][index_point]

            if particle > 0.0:
                likelihood += numpy.log(particle)
        
        return likelihood


    def __probabilities(self, index_cluster, index_point):
        divider = 0.0
        for i in range(self.__amount_clusters):
            divider += self.__pic[i] * self.__gaussians[i][index_point]
        
        if (divider != 0.0) and (divider != float('inf')):
            return self.__pic[index_cluster] * self.__gaussians[index_cluster][index_point] / divider
        
        return 1.0


    def __expectation_step(self):
        self.__gaussians = [ [] for _ in range(self.__amount_clusters) ]
        for index in range(self.__amount_clusters):
            self.__gaussians[index] = gaussian(self.__data, self.__means[index], self.__variances[index])
        
        self.__rc = [ [0.0] * len(self.__data) for _ in range(self.__amount_clusters) ]
        for index_cluster in range(self.__amount_clusters):
            for index_point in range(len(self.__data)):
                self.__rc[index_cluster][index_point] = self.__probabilities(index_cluster, index_point)


    def __maximization_step(self):
        self.__pic = []
        self.__means = []
        self.__variances = []
        
        amount_impossible_clusters = 0
        
        for index_cluster in range(self.__amount_clusters):
            mc = numpy.sum(self.__rc[index_cluster])
            
            if mc == 0.0:
                amount_impossible_clusters += 1
                continue
            
            self.__pic.append( mc / len(self.__data) )
            self.__means.append( self.__update_mean(self.__rc[index_cluster], mc) )
            self.__variances.append( self.__update_covariance(self.__means[-1], self.__rc[index_cluster], mc) )
        
        self.__amount_clusters -= amount_impossible_clusters


    def __get_stop_condition(self):
        for covariance in self.__variances:
            if numpy.linalg.norm(covariance) == 0.0:
                return True
        
        return False


    def __update_covariance(self, means, rc, mc):
        covariance = 0.0
        for index_point in range(len(self.__data)):
            deviation = numpy.array([self.__data[index_point] - means])
            covariance += rc[index_point] * deviation.T.dot(deviation)
        
        covariance = covariance / mc
        return covariance


    def __update_mean(self, rc, mc):
        mean = 0.0
        for index_point in range(len(self.__data)):
            mean += rc[index_point] * self.__data[index_point]
        
        mean = mean / mc
        return mean


    def __normalize_probabilities(self):
        for index_point in range(len(self.__data)):
            probability = 0.0
            for index_cluster in range(len(self.__clusters)):
                probability += self.__rc[index_cluster][index_point]
            
            if abs(probability - 1.0) > 0.000001:
                self.__normalize_probability(index_point, probability)


    def __normalize_probability(self, index_point, probability):
        if probability == 0.0:
            return
        
        normalization = 1.0 / probability

        for index_cluster in range(len(self.__clusters)):
            self.__rc[index_cluster][index_point] *= normalization


    def __verify_arguments(self):
        """!
        @brief Verify input parameters for the algorithm and throw exception in case of incorrectness.

        """
        if len(self.__data) == 0:
            raise ValueError("Input data is empty (size: '%d')." % len(self.__data))

        if self.__amount_clusters < 1:
            raise ValueError("Amount of clusters (current value '%d') should be greater or equal to 1." %
                             self.__amount_clusters)
