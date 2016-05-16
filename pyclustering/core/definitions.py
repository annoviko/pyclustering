"""!

@brief Structures for exchange between core and python implementation.

@authors Andrei Novikov (pyclustering@yandex.ru)
@date 2014-2016
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

import pyclustering.core as core;
import os;

from ctypes import Structure, c_uint, c_double, c_void_p, POINTER;
from sys import platform as _platform;

# Path to DLL.
PATH_DLL_CCORE_64 = None;

if (_platform == "linux") or (_platform == "linux2"):
    PATH_DLL_CCORE_64 = core.__path__[0] + os.sep + "x64" + os.sep + "linux" + os.sep + "ccore.so";
elif (_platform == "win32"):
    PATH_DLL_CCORE_64 = core.__path__[0] + os.sep + "x64" + os.sep + "win" + os.sep + "ccore.dll";


class pyclustering_type_data:
    PYCLUSTERING_TYPE_INT           = 0;
    PYCLUSTERING_TYPE_UNSIGNED_INT  = 1;
    PYCLUSTERING_TYPE_FLOAT         = 2;
    PYCLUSTERING_TYPE_DOUBLE        = 3;
    PYCLUSTERING_TYPE_LONG          = 4;
    PYCLUSTERING_TYPE_UNSIGNED_LONG = 5;
    PYCLUSTERING_TYPE_LIST          = 6;
    PYCLUSTERING_TYPE_SIZE_T        = 7;


# Structures that are required for exchaging with DLL.
class cluster_representation(Structure):
    "Decription of cluster in memory"
    " - unsigned int number_objects"
    " - unsigned int * cluster_representation"
    
    _fields_ = [("number_objects", c_uint), 
                ("pointer_objects", POINTER(c_uint))];
    
    
class clustering_result(Structure):
    "Description of result of clustering in memory"
    " - unsigned int number_clusters"
    " - cluster_representation * pointer_clusters"
    
    _fields_ = [("number_clusters", c_uint), 
                ("pointer_clusters", POINTER(cluster_representation))];


class data_representation(Structure):
    "Description of input data"
    " - unsigned int number_object"
    " - unsigned int dimension"
    " - double ** pointer_objects"
    
    _fields_ = [("number_objects", c_uint), 
                ("dimension", c_uint), 
                ("pointer_objects", POINTER(POINTER(c_double)))];


class dynamic_result(Structure):
    "Description of output dynamic in memory"
    " - unsigned int size_dynamic"
    " - unsigned int size_network"
    " - double * times"
    " - double ** dynamic"
    
    _fields_ = [("size_dynamic", c_uint), 
                ("size_network", c_uint),
                ("times", POINTER(c_double)),
                ("dynamic", POINTER(POINTER(c_double)))];


class pyclustering_package(Structure):
    "Description of output dynamic in memory"
    " - unsigned int size"
    " - unsigned int type"
    " - void * data"
    
    _fields_ = [("size", c_uint),
                ("type", c_uint),
                ("data", POINTER(c_void_p))];

