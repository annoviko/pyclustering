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
    def __init__(self, number_points, linear_sum, square_sum, next_node, prev_node):
        self.number_points = number_points;
        self.linear_sum = linear_sum;
        self.square_sum = square_sum;
        
        self.next = next_node;
        self.prev = prev_node;
        
        self.__centroid = None;
    
    def __repr__(self):
        return 'CF (N: %s, LS: %s, SS: %s)' % (self.number_points, self.linear_sum, self.square_sum);    
    
    
    def merge(self, entry):
        self.number_points += entry.number_points;
        
        dimension = len(self.linear_sum);
        for index_dimension in range(0, dimension):
            self.linear_sum[index_dimension] += entry.linear_sum[index_dimension];
        
        self.square_sum += entry.square_sum;
        
        self.__centroid = None;
    
    
    def get_distance(self, entry, type_measurement):
        if (type_measurement is measurement_type.CENTROID_EUCLIDIAN_DISTANCE):
            return euclidean_distance_sqrt(entry.__get_centroid(), self.__get_centroid());
        
        elif (type_measurement is measurement_type.CENTROID_MANHATTAN_DISTANCE):
            return manhattan_distance(entry.__get_centroid(), self.__get_centroid());
        
        elif (type_measurement is measurement_type.AVERAGE_INTER_CLUSTER_DISTANCE):
            return self.__get_average_inter_cluster_distance(entry);
            
        elif (type_measurement is measurement_type.AVERAGE_INTRA_CLUSTER_DISTANCE):
            return self.__get_average_intra_cluster_distance(entry);
        
        elif (type_measurement is measurement_type.VARIANCE_INCREASE_DISTANCE):
            return self.__get_variance_increase_distance(entry);
        
        else:
            assert 0;
    
        
    def __get_centroid(self):
        if (self.radius is not None):
            return self.radius;
        
        self.__centroid = [0] * len(self.linear_sum);
        for index_dimension in range(0, len(self.linear_sum)):
            self.__centroid[index_dimension] = self.linear_sum[index_dimension] / self.number_points;
        
        return self.radius;
        
        
    def __get_average_inter_cluster_distance(self, entry):
        linear_part_distance = sum(list_math_multiplication(self.__centroid, entry.__centroid));
        
        return ( (self.square_sum - 2.0 * linear_part_distance + entry.square_sum) / (self.number_points * entry.number_points) ) ** 0.5;
    
    
    def __get_average_intra_cluster_distance(self, entry):
        linear_part_first = list_math_addition(self.linear_sum, entry.linear_sum);
        linear_part_second = linear_part_first;
        
        linear_part_distance = sum(list_math_multiplication(linear_part_first, linear_part_second));
        
        general_part_distance = 2.0 * (self.square_sum + entry.square_sum) - 2.0 * linear_part_distance;
        return (general_part_distance / ( (self.number_points + entry.number_points) * (self.number_points + entry.number_points - 1.0) )) ** 0.5;
    
    
    def __get_variance_increase_distance(self, entry):
        linear_part_12 = list_math_addition(self.linear_sum, entry.linear_sum);
        variance_part_first = -2.0 * ( sum(list_math_multiplication(linear_part_12, linear_part_12)) ) / ( 1.0 / (self.number_points + entry.number_points) );
        variance_part_second = sum(list_math_multiplication(linear_part_12, linear_part_12)) / (1.0 / (self.number_points + entry.number_points)**0.5 );
        
        linear_part_11 = sum(list_math_multiplication(self.linear_sum, self.linear_sum));
        variance_part_third = (2.0 / self.number_points) * linear_part_11 - (1.0 / self.number_points ** 2.0) * linear_part_11;
        
        linear_part_22 = sum(list_math_multiplication(entry.linear_sum, entry.linear_sum));
        variance_part_fourth = (2.0 / entry.number_points) * linear_part_22 - (1.0 / entry.number_points ** 2.0) * linear_part_22;
        
        return (variance_part_first + variance_part_second + variance_part_third + variance_part_fourth);
        


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
            
            