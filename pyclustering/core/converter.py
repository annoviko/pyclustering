"""!

@brief Common converter from python types to C/C++.

@authors Andrei Novikov (pyclustering@yandex.ru)
@date 2014-2020
@copyright BSD-3-Clause

"""


from ctypes import c_size_t


def convert_data_type(data_type):
    if data_type == 'points': return c_size_t(0);
    elif data_type == 'distance_matrix': return c_size_t(1);
    else: raise TypeError("Unknown data type is specified '%s'." % data_type);