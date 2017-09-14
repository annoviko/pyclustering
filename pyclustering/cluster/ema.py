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

from pyclustering.utils import pi;

import matplotlib.pyplot as plt;
from _operator import index


def gaussian(data, mean = None, covariance = None):
    dimension = len(data[0]);
 
    if (mean is None):
        mean = numpy.mean(data);
     
    if (covariance is None):
        covariance = numpy.cov(data, rowvar = False);
     
    inv_variance = numpy.linalg.inv(covariance);
    right_const = 1.0 / ( (pi * 2.0) ** (dimension / 2.0) * numpy.linalg.norm(covariance) ** 0.5 );
     
    result = [];
     
    for point in data:
        mean_delta = point - mean;
        point_gaussian = right_const * numpy.exp( -0.5 * mean_delta.dot(inv_variance).dot(numpy.transpose(mean_delta)) );
        result.append(point_gaussian);
     
    return result;


class ema:
    def __init__(self, data, amount_clusters, means = None, variances = None):
        self.__data = numpy.array(data);
        self.__amount_clusters = amount_clusters;
        
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
        
        previous_likelihood = -10000500;
        current_likelihood = -10000000;
        
        while((self.__stop is False) and (abs(numpy.min(previous_likelihood) - numpy.min(current_likelihood)) > 0.00001) and (current_likelihood < 0.0)):
            self.__expectation_step();
            self.__maximization_step();
            
            previous_likelihood = current_likelihood;
            current_likelihood = self.__log_likelihood();
            self.__stop = self.__get_stop_flag();


    def get_clusters(self):
        if (self.__clusters is not None):
            return self.__clusters;
        
        self.__clusters= [];
        for index_cluster in range(self.__amount_clusters):
            cluster = [];
            for index_point in range(len(self.__data)):
                if (self.__rc[index_cluster][index_point] >= 0.5):
                    cluster.append(index_point);
            
            self.__clusters.append(cluster);
        
        return self.__clusters;


    def get_centers(self):
        return self.__means;


    def get_covariances(self):
        return self.__variances;


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
        for index_cluster in range(self.__amount_clusters):
            mc = numpy.sum(self.__rc[index_cluster]);
            
            self.__pic[index_cluster] = mc / len(self.__data);
            self.__means[index_cluster] = self.__update_mean(index_cluster, mc);
            
            self.__variances[index_cluster] = self.__update_covariance(index_cluster, mc);


    def __get_stop_flag(self):
        for covariance in self.__variances:
            if (min(covariance[0]) == 0):
                return True;
        
        return False;


    def __update_covariance(self, index_cluster, mc):
        covariance = 0.0;
        for index_point in range(len(self.__data)):
            deviation = numpy.array( [ self.__data[index_point] - self.__means[index_cluster] ]);
            covariance += self.__rc[index_cluster][index_point] * deviation.T.dot(deviation);
        
        covariance = covariance / mc;
        return covariance;


    def __update_mean(self, index_cluster, mc):
        mean = 0.0;
        for index_point in range(len(self.__data)):
            mean += self.__rc[index_cluster][index_point] * self.__data[index_point];
        
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