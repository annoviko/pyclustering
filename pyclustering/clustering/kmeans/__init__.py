'''

Cluster analysis algorithm: K-Means

Based on book description:
 - J.B.MacQueen. Some Methods for Classification and Analysis of Multivariate Observations. 1967.

Copyright (C) 2015    Andrei Novikov (spb.andr@yandex.ru)

pyclustering is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

pyclustering is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.

'''

import pyclustering.core.wrapper as wrapper;

from pyclustering.support import euclidean_distance, euclidean_distance_sqrt, list_math_addition, list_math_division_number;

class kmeans:
    __pointer_data = None;
    __clusters = None;
    __centers = None;
    __tolerance = 0.0;
    
    __ccore = False;
    
    def __init__(self, data, initial_centers, tolerance = 0.25, ccore = False):
        "Constructor of clustering algorithm K-Means."
         
        "(in) data        - input data that is presented as list of points (objects), each point should be represented by list or tuple."
        "(in) centers     - initial coordinates of centers of clusters that are represented by list: [center1, center2, ...]."
        "(in) tolerance   - stop condition: if maximum value of change of centers of clusters is less than tolerance than algorithm will stop processing."
        "(in) ccore       - defines should be CCORE C++ library used instead of Python code or not."
               
        self.__pointer_data = data;
        self.__clusters = [];
        self.__centers = initial_centers[:];     # initial centers shouldn't be chaged
        self.__tolerance = tolerance;
        
        self.__ccore = ccore;


    def process(self):
        "Performs cluster analysis in line with rules of K-Means algorithm. Results of clustering can be obtained using corresponding gets methods."
        
        if (self.__ccore is True):
            self.__clusters = wrapper.kmeans(self.__pointer_data, self.__centers, self.__tolerance);
            self.__centers = self.__update_centers();
        else: 
            changes = float('inf');
             
            stop_condition = self.__tolerance * self.__tolerance;   # Fast solution
            #stop_condition = self.__tolerance;              # Slow solution
             
            # Check for dimension
            if (len(self.__pointer_data[0]) != len(self.__centers[0])):
                raise NameError('Dimension of the input data and dimension of the initial cluster centers must be equal.');
             
            while (changes > stop_condition):
                self.__clusters = self.__update_clusters();
                updated_centers = self.__update_centers();  # changes should be calculated before asignment
             
                #changes = max([euclidean_distance(self.__centers[index], updated_centers[index]) for index in range(len(self.__centers))]);        # Slow solution
                changes = max([euclidean_distance_sqrt(self.__centers[index], updated_centers[index]) for index in range(len(self.__centers))]);    # Fast solution
                 
                self.__centers = updated_centers;


    def get_clusters(self):
        "Returns list of allocated clusters, each cluster contains indexes of objects in list of data."
        
        return self.__clusters;
    
    
    def get_centers(self):
        "Returns list of centers for allocated clusters."

        return self.__centers;


    def __update_clusters(self):
        "Calculate Euclidean distance to each point from the each cluster. Nearest points are captured by according clusters and as a result clusters are updated."

        "Returns updated clusters as list of clusters. Each cluster contains indexes of objects from data."
        
        clusters = [[] for i in range(len(self.__centers))];
        for index_point in range(len(self.__pointer_data)):
            index_optim = -1;
            dist_optim = 0.0;
             
            for index in range(len(self.__centers)):
                # dist = euclidean_distance(data[index_point], centers[index]);         # Slow solution
                dist = euclidean_distance_sqrt(self.__pointer_data[index_point], self.__centers[index]);      # Fast solution
                 
                if ( (dist < dist_optim) or (index is 0)):
                    index_optim = index;
                    dist_optim = dist;
             
            clusters[index_optim].append(index_point);
             
        return clusters;
    
    
    def __update_centers(self):
        "Calculate centers of clusters in line with contained objects."

        "Returns updated centers as list of centers."
         
        centers = [[] for i in range(len(self.__clusters))];
         
        for index in range(len(self.__clusters)):
            point_sum = [0] * len(self.__pointer_data[0]);
             
            for index_point in self.__clusters[index]:
                point_sum = list_math_addition(point_sum, self.__pointer_data[index_point]);
                 
            centers[index] = list_math_division_number(point_sum, len(self.__clusters[index]));
             
        return centers;
