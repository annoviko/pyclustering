"""!

@brief Wrapper for CCORE library (part of this project).

@authors Andrei Novikov (pyclustering@yandex.ru)
@date 2014-2018
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


import os;
import sys;

from ctypes import *;

from pyclustering.core.definitions import *;


ccore_library_instance = None;


class ccore_library:
    __library           = None;
    __workable          = False;
    __initialized       = False;

    @staticmethod
    def get():
        if (ccore_library.__library):
            return ccore_library.__library;
        
        ccore_library.__initialized = True;
        
        if (PATH_PYCLUSTERING_CCORE_LIBRARY is None):
            # TODO: print platform and python version
            print("The pyclustering core is not supported for platform '" + sys.platform + "'.");
            
            return None;
    
        if (os.path.exists(PATH_PYCLUSTERING_CCORE_LIBRARY) is False):
            # TODO: print platform and python version
            print("The pyclustering core is not found (expected core location: '" + PATH_PYCLUSTERING_CCORE_LIBRARY + "').\n" + 
                  "Probably pyclustering library has not been successfully installed.\n" + 
                  "Please, contact to 'pyclustering@yandex.ru'.");
            
            return None;
        
        ccore_library.__library = cdll.LoadLibrary(PATH_PYCLUSTERING_CCORE_LIBRARY);
        if (not ccore_library.__check_library_integrity()):
            # TODO: print platform and python version
            print("Impossible to mark core as workable due to compitability troubles. Please, contact to 'pyclustering@yandex.ru'");
            
            return None;
        
        return ccore_library.__library;


    @staticmethod
    def workable():
        if (not ccore_library.__initialized):
            ccore_library.get();

        return ccore_library.__workable;


    @staticmethod
    def __check_library_integrity():
        try:
            ccore_library.__library.get_interface_description.restype = c_char_p;
            result = ccore_library.__library.get_interface_description();
            
            if (len(result) > 0):
                ccore_library.__workable = True;
            
            return True;
        
        except:
            ccore_library.__workable = False;
        
        return False;

