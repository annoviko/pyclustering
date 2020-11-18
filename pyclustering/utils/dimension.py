"""!

@brief Data dimension analyser.

@authors Andrei Novikov (pyclustering@yandex.ru)
@date 2014-2020
@copyright BSD-3-Clause

"""


class dimension_info:
    """!
    @brief Analyse input data to extract general information about data dimension.
    
    """
    
    def __init__(self, data):
        if (data is None):
            raise NameError("Information about dimension of 'None' cannot be obtained");
        
        self.__data                 = data;
        self.__dimensions           = None;
        self.__maximum_dimension    = None;
        self.__minimum_dimension    = None;
        self.__width_dimension      = None;
        self.__center_dimension     = None;


    def get_dimensions(self):
        if (self.__dimensions is None):
            self.__calculate_dimension();
            
        return self.__dimensions;
    
    
    def get_maximum_coordinate(self):
        if (self.__maximum_dimension is None):
            self.__calculate_maxmin_dimension_coordinate();
        
        return self.__maximum_dimension;


    def get_minimum_coordinate(self):
        if (self.__minimum_dimension is None):
            self.__calculate_maxmin_dimension_coordinate();
        
        return self.__minimum_dimension;


    def get_width(self):
        if (self.__width_dimension is None):
            self.__calculate_width();
        
        return self.__width_dimension;


    def get_center(self):
        if (self.__center_dimension is None):
            self.__calculate_center();
        
        return self.__center_dimension;


    def __calculate_dimension(self):
        self.__dimensions = len(self.__data[0]);


    def __calculate_maxmin_dimension_coordinate(self):
        self.__maximum_dimension = [self.__data[0][i] for i in range(self.get_dimensions())];
        self.__minimum_dimension = [self.__data[0][i] for i in range(self.get_dimensions())];
        
        for i in range(len(self.__data)):
            for dim in range(self.get_dimensions()):
                if (self.__maximum_dimension[dim] < self.__data[i][dim]):
                    self.__maximum_dimension[dim] = self.__data[i][dim];
                elif (self.__minimum_dimension[dim] > self.__data[i][dim]):
                    self.__minimum_dimension[dim] = self.__data[i][dim];


    def __calculate_width(self):
        self.__width_dimension = [0] * self.get_dimensions();
        for dim in range(self.get_dimensions()):
            self.__width_dimension[dim] = self.get_maximum_coordinate()[dim] - self.get_minimum_coordinate()[dim];


    def __calculate_center(self):
        self.__center_dimension = [0] * self.get_dimensions();
        for dim in range(self.get_dimensions()):
            self.__center_dimension[dim] = (self.get_maximum_coordinate()[dim] + self.get_minimum_coordinate()[dim]) / 2.0;
