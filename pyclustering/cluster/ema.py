"""!

@brief Cluster analysis algorithm: Expectation-Maximization Algorithm (EMA).
@details Implementation based on article:
         - 

@authors Andrei Novikov (pyclustering@yandex.ru)
@date 2014-2017
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

from pyclustering.cluster import cluster_visualizer;
from pyclustering.utils import pi, calculate_ellipse_description;

import matplotlib.pyplot as plt;
from matplotlib import patches;



def gaussian(data, mean, covariance):
    dimension = float(len(data[0]));
 
    if (dimension != 1.0):
        inv_variance = numpy.linalg.pinv(covariance);
    else:
        inv_variance = 1.0 / covariance;
    
    divider = (pi * 2.0) ** (dimension / 2.0) * numpy.sqrt(numpy.linalg.norm(covariance));
    right_const = 1.0 / divider;
     
    result = [];
     
    for point in data:
        mean_delta = point - mean;
        point_gaussian = right_const * numpy.exp( -0.5 * mean_delta.dot(inv_variance).dot(numpy.transpose(mean_delta)) );
        result.append(point_gaussian);
     
    return result;



class ema_observer:
    def __init__(self):
        self.__means_evolution = [];
        self.__covariances_evolution = [];
        self.__clusters_evolution = [];


    def get_iterations(self):
        return len(self.__means);


    def get_means(self):
        return self.__means_evolution;


    def get_covariances(self):
        return self.__covariances_evolution;


    def notify(self, means, covariances, clusters):
        self.__means_evolution.append(means);
        self.__covariances_evolution.append(covariances);
        self.__clusters_evolution.append(clusters);



class ema_visualizer:
    @staticmethod
    def show_clusters(clusters, sample, covariances, means, display = True):
        visualizer = cluster_visualizer();
        visualizer.append_clusters(clusters, sample);
        figure = visualizer.show(display = False);
        
        if (len(sample[0]) == 2):
            ema_visualizer.__draw_ellipses(figure, visualizer, clusters, covariances, means);

        if (display is True): 
            plt.show();

        return figure;


    @staticmethod
    def __draw_ellipses(figure, visualizer, clusters, covariances, means):
        print(len(clusters));
        print([len(cluster) for cluster in clusters]);
        print(clusters);
        
        ax = figure.get_axes()[0];
        
        for index in range(len(clusters)):
            angle, width, height = calculate_ellipse_description(covariances[index]);
            color = visualizer.get_cluster_color(index, 0);
            
            ema_visualizer.__draw_ellipse(ax, means[index][0], means[index][1], angle, width, height, color);


    @staticmethod
    def __draw_ellipse(ax, x, y, angle, width, height, color):
        ellipse = patches.Ellipse((x, y), width, height, alpha=0.2, angle=angle, linewidth=2, fill=True, zorder=2, color=color);
        ax.add_patch(ellipse);


class ema:
    def __init__(self, data, amount_clusters, means = None, variances = None, observer = None, tolerance = 0.00001):
        self.__data = numpy.array(data);
        self.__amount_clusters = amount_clusters;
        self.__tolerance = tolerance;
        self.__observer = observer;
        
        self.__means = means;
        if (means is None):
            self.__means = self.__get_random_means(data, amount_clusters);

        self.__variances = variances;
        if (variances is None):
            self.__variances = self.__get_random_covariances(data, amount_clusters);
        
        self.__rc = [ [0.0] * len(self.__data) for _ in range(amount_clusters) ];
        self.__pic = [1.0] * amount_clusters;
        self.__clusters = [];
        self.__gaussians = [ [] for _ in range(amount_clusters) ];
        self.__stop = False;


    def process(self):
        self.__clusters = None;
        
        previous_likelihood = -200000;
        current_likelihood = -100000;
        
        while( (self.__stop is False) and (abs(previous_likelihood - current_likelihood) > self.__tolerance) ):
            self.__expectation_step();
            self.__maximization_step();
            
            previous_likelihood = current_likelihood;
            current_likelihood = self.__log_likelihood();
            self.__stop = self.__get_stop_condition();
        
        self.__clusters = self.__extract_clusters();


    def get_clusters(self):
        return self.__clusters;


    def get_centers(self):
        return self.__means;


    def get_covariances(self):
        return self.__variances;


    def __notify(self):
        if (self.__observer is not None):
            clusters = self.__extract_clusters();
            self.__notify(self.__means, self.__variances, clusters);


    def __extract_clusters(self):
        clusters = [ [] for _ in range(self.__amount_clusters) ];
        for index_point in range(len(self.__data)):
            candidates = [];
            for index_cluster in range(self.__amount_clusters):
                candidates.append((index_cluster, self.__rc[index_cluster][index_point]));
            
            index_winner = max(candidates, key = lambda candidate : candidate[1])[0];
            clusters[index_winner].append(index_point);
        
        clusters = [ cluster for cluster in clusters if len(cluster) > 0 ];
        return clusters;


    def __log_likelihood(self):
        likelihood = 0.0;
        
        for index_point in range(len(self.__data)):
            particle = 0.0;
            for index_cluster in range(self.__amount_clusters):
                particle += self.__pic[index_cluster] * self.__gaussians[index_cluster][index_point];
            
            likelihood += numpy.log(particle);
        
        return likelihood;


    def __probabilities(self, index_cluster, index_point):
        divider = 0.0;
        for i in range(self.__amount_clusters):
            divider += self.__pic[i] * self.__gaussians[i][index_point];
        
        rc = self.__pic[index_cluster] * self.__gaussians[index_cluster][index_point] / divider;
        return rc;


    def __expectation_step(self):
        for index in range(self.__amount_clusters):
            self.__gaussians[index] = gaussian(self.__data, self.__means[index], self.__variances[index]);
        
        for index_cluster in range(self.__amount_clusters):
            for index_point in range(len(self.__data)):
                self.__rc[index_cluster][index_point] = self.__probabilities(index_cluster, index_point);


    def __maximization_step(self):
        self.__pic = [];
        self.__means = [];
        self.__variances = [];
        
        amount_impossible_clusters = 0;
        
        for index_cluster in range(self.__amount_clusters):
            mc = numpy.sum(self.__rc[index_cluster]);
            
            if (mc == 0.0):
                amount_impossible_clusters += 1;
                continue;
            
            self.__pic.append( mc / len(self.__data) );
            self.__means.append( self.__update_mean(self.__rc[index_cluster], mc) );
            self.__variances.append( self.__update_covariance(self.__means[-1], self.__rc[index_cluster], mc) );
        
        self.__amount_clusters -= amount_impossible_clusters;


    def __get_stop_condition(self):
        for covariance in self.__variances:
            if (numpy.linalg.norm(covariance) == 0.0):
                return True;
        
        return False;


    def __update_covariance(self, means, rc, mc):
        covariance = 0.0;
        for index_point in range(len(self.__data)):
            deviation = numpy.array( [ self.__data[index_point] - means ]);
            covariance += rc[index_point] * deviation.T.dot(deviation);
        
        covariance = covariance / mc;
        return covariance;


    def __update_mean(self, rc, mc):
        mean = 0.0;
        for index_point in range(len(self.__data)):
            mean += rc[index_point] * self.__data[index_point];
        
        mean = mean / mc;
        return mean;


    def __get_random_covariances(self, data, amount):
        covariances = [];
        covariance_appendixes = [];
        data_covariance = numpy.cov(data, rowvar = False);
        for _ in range(amount):
            random_appendix = numpy.min(data_covariance) * 0.5 * numpy.random.random();
            while(random_appendix in covariance_appendixes):
                random_appendix = numpy.min(data_covariance) * 0.5 * numpy.random.random();
            
            covariance_appendixes.append(random_appendix)
            covariances.append(data_covariance - random_appendix);
         
        return covariances;


    def __get_random_means(self, data, amount):
        means = [];
        mean_indexes = [];
        for _ in range(amount):
            random_index = numpy.random.randint(0, len(data));
            while(random_index in mean_indexes):
                random_index = numpy.random.randint(0, len(data));
            
            mean_indexes.append(random_index);
            means.append(numpy.array(data[random_index]));
        
        return means;