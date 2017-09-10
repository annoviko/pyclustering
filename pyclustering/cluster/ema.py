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


def gaussion_multivariable(data, mean = None, covariance = None):
    dimension = len(data[0]);

    if (mean is None):
        mean = numpy.mean(data);
    
    if (covariance is None):
        covariance = numpy.cov(data);
    
    inv_variance = numpy.linalg.inv(covariance);
    right_const = 1.0 / ( (pi * 2.0) ** (dimension / 2.0) * numpy.linalg.norm(covariance) ** 0.5 );
    
    result = [];
    
    for point in data:
        mean_delta = point - mean;
        point_gaussian = right_const * numpy.exp(-0.5 * mean_delta.T * inv_variance * mean_delta);
        result.append(point_gaussian);
    
    return result;


def gaussian_singlevariable(data, mean = None, variance = None):
    if (mean is None):
        mean = numpy.mean(data);
    
    if (variance is None):
        variance = numpy.var(data, ddof = 1);

    right_const = 1.0 / ( 2.0 * pi * variance ) ** 0.5;
    result = [];
    
    for point in data:
        mean_delta = point - mean;
        point_gaussian = right_const * numpy.exp(-mean_delta ** 2.0 / (2.0 * variance) );
        result.append(point_gaussian);
    
    return result;


def gaussian(data, mean = None, variance = None):
    try: dimension = len(data[0]);
    except: dimension = 1;
    
    if (dimension == 1):
        return gaussian_singlevariable(data, mean, variance);
    else:
        return gaussion_multivariable(data, mean, variance);


# data = numpy.random.normal(0, 0.1, 100);
# one_gaussian = gaussian(data);
# one_gaussian.sort();
# 
# print(one_gaussian);
# 
# axis = plt.subplot(111);
# plt.plot(one_gaussian, 'b-', linewidth = 2.0);
# plt.show();



class ema:
    def __init__(self, data, amount_clusters, means = None, variances = None):
        self.__data = data;
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


    def process(self):
        previous_likelihood = -1000.0;
        current_likelihood = 0.0;
        
        while(abs(previous_likelihood - current_likelihood) > 0.1):
            self.__expectation_step();
            self.__maximization_step();
            
            previous_likelihood = current_likelihood;
            current_likelihood = self.__log_likelihood();


    def get_clusters(self):
        return self.__clusters;


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
            for index_point in range(self.__data):
                self.__rc[index_cluster][index_point] = self.__probabilities(index_cluster, index_point);


    def __maximization_step(self):
        for index_cluster in range(self.__amount_clusters):
            mc = numpy.sum(self.__rc[index_cluster]);
            
            self.__pic[index_cluster] = mc / len(self.__data);
            self.__means[index_cluster] = self.__update_mean(index_cluster, mc);
            self.__variances[index_cluster] = self.__update_variance(index_cluster, mc);


    def __update_variance(self, index_cluster, mc):
        variance = 0.0;
        for index_point in range(len(self.__data)):
            deviation = self.__data[index_point] - self.__means[index_cluster];
            variance += self.__rc[index_cluster][index_point] * deviation.T * deviation;
        
        variance = variance / mc;
        return variance;


    def __update_mean(self, index_cluster, mc):
        mean = 0.0;
        for index_point in range(len(self.__data)):
            mean += self.__rc[index_cluster][index_point] * self.__data[index_point];
        
        mean = mean / mc;
        return mean;


    def __get_random_covariances(self, data, amount):
        covariances = [];
        data_covariance = numpy.cov(data);
        for _ in range(amount):
            random_appendix = numpy.min(data_covariance) * 0.2 * numpy.random.random();
            covariances.append(data_covariance + random_appendix);
        
        return covariances;


    def __get_random_variances(self, data, amount):
        variances = [];
        data_variance = numpy.var(data, ddof = 1);
        for _ in range(amount):
            random_appendix = data_variance * 0.1 * numpy.random.random();
            variances.append(random_appendix + variances);
        
        return variances;


    def __get_random_means(self, data, amount):
        means = [];
        for _ in range(amount):
            random_index = numpy.random.randint(0, len(data));
            means.append(numpy.array(data[random_index]));
        
        return means;
    


# from pyclustering.samples.definitions import SIMPLE_SAMPLES, FCPS_SAMPLES;
# from pyclustering.utils import read_sample;
# 
# sample = read_sample(SIMPLE_SAMPLES.SAMPLE_SIMPLE1);
# ema_instance = ema(sample, 2);
# ema_instance.process();
# clusters = ema_instance.get_clusters();
# 
# print(clusters);