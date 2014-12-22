'''

Data Structure: CF-Tree

Based on book description:
 - M.Zhang, R.Ramakrishnan, M.Livny. BIRCH: An Efficient Data Clustering Method for Very Large Databases. 1996.

Implementation: Andrei Novikov (spb.andr@yandex.ru)

'''

from support import euclidean_distance, euclidean_distance_sqrt;
from support import manhattan_distance;
from support import list_math_addition, list_math_multiplication,list_math_division_number;

class measurement_type:
    CENTROID_EUCLIDIAN_DISTANCE = 0;
    CENTROID_MANHATTAN_DISTANCE = 1;
    AVERAGE_INTER_CLUSTER_DISTANCE = 2;
    AVERAGE_INTRA_CLUSTER_DISTANCE = 3;
    VARIANCE_INCREASE_DISTANCE = 4;

class cfentry:
    "Clustering feature representation."
    
    __centroid = None;
    __radius = None;
    __diameter = None;
    
    __number_points = 0;
    __linear_sum = None;
    __square_sum = None;
    
    @property
    def number_points(self):
        return self.__number_points;
    
    @property
    def linear_sum(self):
        return self.__linear_sum;
    
    @property
    def square_sum(self):
        return self.__square_sum;
    
    
    def __init__(self, number_points, linear_sum, square_sum):
        self.__number_points = number_points;
        self.__linear_sum = linear_sum;
        self.__square_sum = square_sum;
        
        self.__centroid = None;
        self.__radius = None;
        self.__diameter = None;
    
    def __repr__(self):
        return 'CF (N: %s, LS: %s, SS: %s)' % (self.number_points, self.__linear_sum, self.__square_sum);    
    
    
    def merge(self, entry):
        "Merge current clustering feature with another."
        
        "(in) entry    - pointer to clustering feature that should be merged with current."
        
        self.number_points += entry.number_points;
        
        dimension = len(self.linear_sum);
        for index_dimension in range(0, dimension):
            self.linear_sum[index_dimension] += entry.linear_sum[index_dimension];
        
        self.square_sum += entry.square_sum;
        
        self.__centroid = None;
        self.__radius = None;
        self.__diameter = None;
    
    
    def get_distance(self, entry, type_measurement):
        "Return distance between two clusters in line with measurement type."
        
        "(in) entry               - pointer of clustering feature to which distance should be obtained."
        "(in) type_measurement    - distance measurement algorithm between two clusters."
        
        "Return distance between two clusters."
        
        if (type_measurement is measurement_type.CENTROID_EUCLIDIAN_DISTANCE):
            return euclidean_distance_sqrt(entry.get_centroid(), self.get_centroid());
        
        elif (type_measurement is measurement_type.CENTROID_MANHATTAN_DISTANCE):
            return manhattan_distance(entry.get_centroid(), self.get_centroid());
        
        elif (type_measurement is measurement_type.AVERAGE_INTER_CLUSTER_DISTANCE):
            return self.__get_average_inter_cluster_distance(entry);
            
        elif (type_measurement is measurement_type.AVERAGE_INTRA_CLUSTER_DISTANCE):
            return self.__get_average_intra_cluster_distance(entry);
        
        elif (type_measurement is measurement_type.VARIANCE_INCREASE_DISTANCE):
            return self.__get_variance_increase_distance(entry);
        
        else:
            assert 0;
    
        
    def get_centroid(self):
        "Return centroid of cluster that is represented by the entry. It's calculated once when it's requested after the last changes."
        
        if (self.__centroid is not None):
            return self.__centroid;
        
        if (type(self.linear_sum) == list):
            self.__centroid = [0] * len(self.linear_sum);
            for index_dimension in range(0, len(self.linear_sum)):
                self.__centroid[index_dimension] = self.linear_sum[index_dimension] / self.number_points;
        else:
            self.__centroid = self.linear_sum / self.number_points;
        
        return self.__centroid;
    
    
    def get_radius(self):
        "Return radius of cluster that is represented by the entry. It's calculated once when it's requested after the last changes."
        
        if (self.__radius is not None):
            return self.__radius;
        
        centroid = self.get_centroid();
        
        radius_part_1 = self.square_sum;
        
        radius_part_2 = 0.0;
        radius_part_3 = 0.0;
        
        if (type(centroid) == list):
            radius_part_2 = 2.0 * sum(list_math_multiplication(self.linear_sum, centroid));
            radius_part_3 = self.number_points * sum(list_math_multiplication(centroid, centroid));
        else:
            radius_part_2 = 2.0 * self.linear_sum * centroid;
            radius_part_3 = self.number_points * centroid * centroid;
        
        self.__radius = ( (1.0 / self.number_points) * (radius_part_1 - radius_part_2 + radius_part_3) ) ** 0.5;
        return self.__radius;
        
    
    def get_diameter(self):
        "Return diameter of cluster that is represented by the entry. It's calculated once when it's requested after the last changes."
        
        if (self.__diameter is not None):
            return self.__diameter;
        
        diameter_part = 0.0;
        if (type(self.linear_sum) == list):
            diameter_part = self.square_sum * self.number_points - 2.0 * sum(list_math_multiplication(self.linear_sum, self.linear_sum)) + self.square_sum * self.number_points;
            print("diameter_part:", diameter_part);
        else:
            diameter_part = self.square_sum * self.number_points - 2.0 * self.linear_sum * self.linear_sum + self.square_sum * self.number_points;
            
        self.__diameter = ( diameter_part / (self.number_points * (self.number_points - 1)) ) ** 0.5;
        return self.__diameter;
    
        
    def __get_average_inter_cluster_distance(self, entry):
        "Return average inter cluster distance between current and specified clusters."
        
        "(in) entry    - pointer to clustering feature to which distance should be obtained."
        
        "Return average inter cluster distance."
        
        linear_part_distance = sum(list_math_multiplication(self.linear_sum, entry.linear_sum));
        
        return ( (entry.number_points * self.square_sum - 2.0 * linear_part_distance + self.number_points * entry.square_sum) / (self.number_points * entry.number_points) ) ** 0.5;
    
    
    def __get_average_intra_cluster_distance(self, entry):
        "Return average intra cluster distance between current and specified clusters."
        
        "(in) entry    - pointer to clustering feature to which distance should be obtained."
        
        "Return average intra cluster distance."
        
        linear_part_first = list_math_addition(self.linear_sum, entry.linear_sum);
        linear_part_second = linear_part_first;
        
        linear_part_distance = sum(list_math_multiplication(linear_part_first, linear_part_second));
        
        general_part_distance = 2.0 * (self.number_points + entry.number_points) * (self.square_sum + entry.square_sum) - 2.0 * linear_part_distance;
        
        return (general_part_distance / ( (self.number_points + entry.number_points) * (self.number_points + entry.number_points - 1.0) )) ** 0.5;
    
    
    def __get_variance_increase_distance(self, entry):
        "Return variance increase distance between current and specified clusters."
        
        "(in) entry    - pointer to clustering feature to which distance should be obtained."
        
        "Return variance increase distance."
                
        linear_part_12 = list_math_addition(self.linear_sum, entry.linear_sum);
        variance_part_first = (self.square_sum + entry.square_sum) - \
            2.0 * sum(list_math_multiplication(linear_part_12, linear_part_12)) / (self.number_points + entry.number_points) + \
            (self.number_points + entry.number_points) * sum(list_math_multiplication(linear_part_12, linear_part_12)) / (self.number_points + entry.number_points)**2.0;

        
        linear_part_11 = sum(list_math_multiplication(self.linear_sum, self.linear_sum));
        variance_part_second = -( self.square_sum - (2.0 * linear_part_11 / self.number_points) + (linear_part_11 / self.number_points) );
        
        linear_part_22 = sum(list_math_multiplication(entry.linear_sum, entry.linear_sum));
        variance_part_third = -( entry.square_sum - (2.0 / entry.number_points) * linear_part_22 + entry.number_points * (1.0 / entry.number_points ** 2.0) * linear_part_22 );
        
        print(variance_part_first, variance_part_second, variance_part_third);
        
        return (variance_part_first + variance_part_second + variance_part_third);
        


class cftree:
    __root = None;
    
    __branch_factor = 0;
    __threshold = 0.0;
    
    def __init__(self, branch_factor, threshold):
        self.__branch_factor = branch_factor; # maximum number of children
        self.__threshold = threshold;         # maximum diameter of sub-clusters stored at the leaf nodes
    
    def insert(self, node):
        if (self.__root is None):
            self.__root = node;
            
        else:
            # find the closest child node
            pass;
        
    def __find_nearest_leaf(self, node):
        pass;

    
    