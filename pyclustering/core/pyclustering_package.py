"""!

@brief Pyclustering package that is used to exchange between python core and 'ccore'.

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



from ctypes import *

import collections
import numpy



class pyclustering_package(Structure):
    """!
    @brief pyclustering_package description in memory.
    @details Represents following C++ structure:
    
            typedef struct pyclustering_package {
                std::size_t      size;
                unsigned int     type;
                void *           data;
            }
    """
    
    _fields_ = [ ("size", c_size_t),
                 ("type", c_uint),
                 ("data", POINTER(c_void_p)) ]



class pyclustering_type_data:
    """!
    @brief Contains constants that defines type of package.
    
    """
    
    PYCLUSTERING_TYPE_INT               = 0x00
    PYCLUSTERING_TYPE_UNSIGNED_INT      = 0x01
    PYCLUSTERING_TYPE_FLOAT             = 0x02
    PYCLUSTERING_TYPE_DOUBLE            = 0x03
    PYCLUSTERING_TYPE_LONG              = 0x04
    PYCLUSTERING_TYPE_UNSIGNED_LONG     = 0x05
    PYCLUSTERING_TYPE_LIST              = 0x06
    PYCLUSTERING_TYPE_SIZE_T            = 0x07
    PYCLUSTERING_TYPE_UNDEFINED         = 0x08

    __CTYPE_PYCLUSTERING_MAP = { 
        c_int                           : PYCLUSTERING_TYPE_INT,
        c_uint                          : PYCLUSTERING_TYPE_UNSIGNED_INT,
        c_float                         : PYCLUSTERING_TYPE_FLOAT,
        c_double                        : PYCLUSTERING_TYPE_DOUBLE,
        c_long                          : PYCLUSTERING_TYPE_LONG,
        c_ulong                         : PYCLUSTERING_TYPE_UNSIGNED_LONG,
        POINTER(pyclustering_package)   : PYCLUSTERING_TYPE_LIST,
        c_size_t                        : PYCLUSTERING_TYPE_SIZE_T,
        None                            : PYCLUSTERING_TYPE_UNDEFINED
    }

    __PYCLUSTERING_CTYPE_MAP = {
        PYCLUSTERING_TYPE_INT             : c_int,
        PYCLUSTERING_TYPE_UNSIGNED_INT    : c_uint,
        PYCLUSTERING_TYPE_FLOAT           : c_float,
        PYCLUSTERING_TYPE_DOUBLE          : c_double,
        PYCLUSTERING_TYPE_LONG            : c_long,
        PYCLUSTERING_TYPE_UNSIGNED_LONG   : c_ulong,
        PYCLUSTERING_TYPE_LIST            : POINTER(pyclustering_package),
        PYCLUSTERING_TYPE_SIZE_T          : c_size_t,
        PYCLUSTERING_TYPE_UNDEFINED       : None
    }

    @staticmethod
    def get_ctype(pyclustering_package_type):
        """!
        @return (ctype) Return ctype that corresponds to pyclustering type data.
        
        """
        return pyclustering_type_data.__PYCLUSTERING_CTYPE_MAP[pyclustering_package_type]

    @staticmethod
    def get_pyclustering_type(data_ctype):
        """!
        @return (unit) Return pyclustering data type that corresponds to ctype.
        
        """
        return pyclustering_type_data.__CTYPE_PYCLUSTERING_MAP[data_ctype]


class package_builder:
    """!
    @brief Package builder provides service to create 'pyclustering_package' from data that is stored in 'list' container.

    """
    def __init__(self, dataset, c_data_type):
        """!
        @brief Initialize package builder object by dataset.
        
        @param[in] dataset (list): Data that should be packed in 'pyclustering_package'.
        @param[in] c_data_type (ctype.type): If specified than specified data type is used for data storing in package. 
        
        """
        self.__dataset = dataset
        self.__c_data_type = c_data_type


    def create(self):
        """!
        @brief Performs packing procedure of the data to the package.
        
        @return (pointer) ctype-pointer to pyclustering package.
        
        """
        return self.__create_package(self.__dataset)


    def __is_container_type(self, value):
        return isinstance(value, collections.Iterable)


    def __get_type(self, pyclustering_data_type):
        if self.__c_data_type is None:
            return pyclustering_data_type
        
        return self.__c_data_type


    def __create_package(self, dataset):
        dataset_package = pyclustering_package()
        
        if isinstance(dataset, numpy.matrix):
            return self.__create_package_numpy_matrix(dataset_package, dataset)
        
        dataset_package.size = len(dataset)
    
        if len(dataset) == 0:
            dataset_package.type = pyclustering_type_data.PYCLUSTERING_TYPE_UNDEFINED
            dataset_package.data = None
    
            return pointer(dataset_package)
    
        c_data_type = self.__fill_type(dataset_package, dataset)
        self.__fill_data(dataset_package, c_data_type, dataset)
        
        return pointer(dataset_package)


    def __fill_dataset_type(self, dataset_package, dataset):
        if self.__is_container_type(dataset[0]):
            dataset_package.type = pyclustering_type_data.PYCLUSTERING_TYPE_LIST
        
        elif isinstance(dataset[0], int):
            dataset_package.type = pyclustering_type_data.PYCLUSTERING_TYPE_LONG
        
        elif isinstance(dataset[0], float):
            dataset_package.type = pyclustering_type_data.PYCLUSTERING_TYPE_DOUBLE
        
        else:
            raise NameError("Not supported type of pyclustering package.")
        
        return pyclustering_type_data.get_ctype(dataset_package.type)


    def __fill_specify_type(self, dataset_package):
        dataset_package.type = pyclustering_type_data.get_pyclustering_type(self.__c_data_type)
        return self.__c_data_type


    def __fill_type(self, dataset_package, dataset):
        if self.__is_container_type(dataset[0]):
            dataset_package.type = pyclustering_type_data.PYCLUSTERING_TYPE_LIST
            return None
        
        if self.__c_data_type is None:
            return self.__fill_dataset_type(dataset_package, dataset)
        
        return self.__fill_specify_type(dataset_package)


    def __fill_data(self, dataset_package, c_data_type, dataset):
        if dataset_package.type == pyclustering_type_data.PYCLUSTERING_TYPE_LIST:
            package_data = (POINTER(pyclustering_package) * len(dataset))()
            for index in range(len(dataset)):
                package_data[index] = self.__create_package(dataset[index])
            
            dataset_package.data = cast(package_data, POINTER(c_void_p))
        else:
            array_object = (c_data_type * len(dataset))(*dataset)
            dataset_package.data = cast(array_object, POINTER(c_void_p))


    def __create_package_numpy_matrix(self, dataset_package, dataset):
        (rows, cols) = dataset.shape
        
        dataset_package.size = rows
        dataset_package.type = pyclustering_type_data.PYCLUSTERING_TYPE_LIST
        
        package_data = (POINTER(pyclustering_package) * rows)()
        for row_index in range(rows):
            array_package = pyclustering_package()
            array_package.size = cols
            array_package.type = pyclustering_type_data.get_pyclustering_type(self.__c_data_type)
            
            array_object = (self.__c_data_type * cols)()
            for col_index in range(cols):
                array_object[col_index] = self.__c_data_type(dataset[row_index, col_index])
        
            array_package.data = cast(array_object, POINTER(c_void_p))
            package_data[row_index] = pointer(array_package)
            
        dataset_package.data = cast(package_data, POINTER(c_void_p))
        return pointer(dataset_package)



class package_extractor:
    """!
    @brief Package extractor provides servies to unpack pyclustering package.
    
    """
    def __init__(self, package_pointer):
        """!
        @brief Initialize package extractor object by ctype-pointer to 'pyclustering_package'.
        
        @param[in] package_pointer (pointer): ctype-pointer to 'pyclustering_package' that should be used for unpacking.
        
        """
        self.__package_pointer = package_pointer


    def extract(self):
        """!
        @brief Performs unpacking procedure of the pyclustering package to the data.
        
        @return (list) Extracted data from the pyclustering package.
        
        """
        return self.__extract_data(self.__package_pointer)


    def __extract_data(self, ccore_package_pointer):
        if ccore_package_pointer == 0:
            return []
        
        pointer_package = cast(ccore_package_pointer, POINTER(pyclustering_package))
        return self.__unpack_pointer_data(pointer_package)
    
    
    def __unpack_data(self, pointer_package, pointer_data, type_package):
        result = []
        
        for index in range(0, pointer_package[0].size):
            if type_package == pyclustering_type_data.PYCLUSTERING_TYPE_LIST:
                pointer_package = cast(pointer_data[index], (POINTER(pyclustering_package)))
                result.append(self.__extract_data(pointer_package))
            
            else:
                result.append(pointer_data[index])
        
        return result


    def __unpack_pointer_data(self, pointer_package):
        type_package = pointer_package[0].type
        
        if pointer_package[0].size == 0:
            return []
        
        pointer_data = cast(pointer_package[0].data, POINTER(pyclustering_type_data.get_ctype(type_package)))
        return self.__unpack_data(pointer_package, pointer_data, type_package)
