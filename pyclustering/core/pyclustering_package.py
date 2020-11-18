"""!

@brief Pyclustering package that is used to exchange between python core and 'ccore'.

@authors Andrei Novikov (pyclustering@yandex.ru)
@date 2014-2020
@copyright BSD-3-Clause

"""



from ctypes import *

import collections.abc
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
    
    _fields_ = [("size", c_size_t),
                ("type", c_uint),
                ("data", POINTER(c_void_p))]



class pyclustering_type_data:
    """!
    @brief Contains constants that defines type of package.
    
    """
    
    PYCLUSTERING_TYPE_INT = 0
    PYCLUSTERING_TYPE_UNSIGNED_INT = 1
    PYCLUSTERING_TYPE_FLOAT = 2
    PYCLUSTERING_TYPE_DOUBLE = 3
    PYCLUSTERING_TYPE_LONG = 4
    PYCLUSTERING_TYPE_CHAR = 5
    PYCLUSTERING_TYPE_LIST = 6
    PYCLUSTERING_TYPE_SIZE_T = 7
    PYCLUSTERING_TYPE_WCHAR_T = 8
    PYCLUSTERING_TYPE_UNDEFINED = 9

    __CTYPE_PYCLUSTERING_MAP = { 
        c_int: PYCLUSTERING_TYPE_INT,
        c_uint: PYCLUSTERING_TYPE_UNSIGNED_INT,
        c_float: PYCLUSTERING_TYPE_FLOAT,
        c_double: PYCLUSTERING_TYPE_DOUBLE,
        c_long: PYCLUSTERING_TYPE_LONG,
        c_char: PYCLUSTERING_TYPE_CHAR,
        POINTER(pyclustering_package): PYCLUSTERING_TYPE_LIST,
        c_size_t: PYCLUSTERING_TYPE_SIZE_T,
        c_wchar: PYCLUSTERING_TYPE_WCHAR_T,
        None: PYCLUSTERING_TYPE_UNDEFINED
    }

    __PYCLUSTERING_CTYPE_MAP = {
        PYCLUSTERING_TYPE_INT: c_int,
        PYCLUSTERING_TYPE_UNSIGNED_INT: c_uint,
        PYCLUSTERING_TYPE_FLOAT: c_float,
        PYCLUSTERING_TYPE_DOUBLE: c_double,
        PYCLUSTERING_TYPE_LONG: c_long,
        PYCLUSTERING_TYPE_CHAR: c_char,
        PYCLUSTERING_TYPE_LIST: POINTER(pyclustering_package),
        PYCLUSTERING_TYPE_SIZE_T: c_size_t,
        PYCLUSTERING_TYPE_WCHAR_T: c_wchar,
        PYCLUSTERING_TYPE_UNDEFINED: None
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
    def __init__(self, dataset, c_data_type=None):
        """!
        @brief Initialize package builder object by dataset.
        @details String data is packed as it is without encoding. If string encoding is required then it should be
                  provided already encoded, for example in case of `utf-8`:
        @code
            encoded_string = "String to pack".encode('utf-8')
            pyclustering_package = package_builder(encoded_string)
        @endcode
        
        @param[in] dataset (list): Data that should be packed in 'pyclustering_package'.
        @param[in] c_data_type (ctype.type): C-type data that is used to store data in the package.
        
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
        return isinstance(value, collections.abc.Iterable)


    def __get_type(self, pyclustering_data_type):
        if self.__c_data_type is None:
            return pyclustering_data_type
        
        return self.__c_data_type


    def __create_package(self, dataset):
        dataset_package = pyclustering_package()

        if isinstance(dataset, str):
            return self.__create_package_string(dataset_package, dataset)

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


    def __create_package_string(self, dataset_package, string_value):
        dataset_package.size = len(string_value)
        dataset_package.type = pyclustering_type_data.PYCLUSTERING_TYPE_CHAR
        dataset_package.data = cast(string_value, POINTER(c_void_p))
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
        if type_package == pyclustering_type_data.PYCLUSTERING_TYPE_CHAR:
            pointer_string = cast(pointer_data, c_char_p)
            return pointer_string.value

        elif type_package == pyclustering_type_data.PYCLUSTERING_TYPE_WCHAR_T:
            raise NotImplementedError("Data type 'wchar_t' is not supported.")

        result = []
        append_element = lambda container, item: container.append(item)
        
        for index in range(0, pointer_package[0].size):
            if type_package == pyclustering_type_data.PYCLUSTERING_TYPE_LIST:
                pointer_package = cast(pointer_data[index], (POINTER(pyclustering_package)))
                append_element(result, self.__extract_data(pointer_package))

            else:
                append_element(result, pointer_data[index])
        
        return result


    def __unpack_pointer_data(self, pointer_package):
        current_package = pointer_package[0]
        type_package = current_package.type
        
        if current_package.size == 0:
            return []

        pointer_data = cast(current_package.data, POINTER(pyclustering_type_data.get_ctype(type_package)))
        return self.__unpack_data(pointer_package, pointer_data, type_package)
