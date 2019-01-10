"""!

@brief Data dimension analyser.

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
