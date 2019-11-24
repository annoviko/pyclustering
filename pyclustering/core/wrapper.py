"""!

@brief Wrapper for CCORE library (part of this project).

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


import sys

from ctypes import *

from pyclustering.core.definitions import *


ccore_library_instance = None
ccore_library_version = "0.9.3"


class ccore_library:
    __library = None
    __workable = False
    __initialized = False

    @staticmethod
    def get():
        if not ccore_library.__library:
            ccore_library.initialize()

        return ccore_library.__library


    @staticmethod
    def workable():
        if not ccore_library.__initialized:
            ccore_library.get()

        return ccore_library.__workable


    @staticmethod
    def initialize():
        ccore_library.__initialized = True
        
        if PATH_PYCLUSTERING_CCORE_LIBRARY is None:
            print("The pyclustering ccore is not supported for platform '" + sys.platform + "' (" + platform.architecture()[0] + ").\n" + 
                  "Falling back on python implementation.\n" +
                  "For more information, contact 'pyclustering@yandex.ru'.")
            
            return None
    
        if os.path.exists(PATH_PYCLUSTERING_CCORE_LIBRARY) is False:
            print("The pyclustering ccore is not found (expected core location: '" + PATH_PYCLUSTERING_CCORE_LIBRARY + "').\n" + 
                  "Probably library has not been successfully installed ('" + sys.platform + "', '" + platform.architecture()[0] + "').\n" + 
                  "Falling back on python implementation.\n" +
                  "For more information, contact 'pyclustering@yandex.ru'.")
            
            return None

        ccore_library.__library = cdll.LoadLibrary(PATH_PYCLUSTERING_CCORE_LIBRARY)
        if ccore_library.__check_library_integrity() is False:
            print("Impossible to mark ccore as workable due to compatibility issues " +
                  "('" + sys.platform + "', '" + platform.architecture()[0] + "').\n" + 
                  "Falling back on python implementation.\n" +
                  "For more information, contact 'pyclustering@yandex.ru'.")
            
            return None

        result, version = ccore_library.__check_library_version()
        if result is False:
            print("Incompatible ccore version of pyclustering library is being used ('" + version +"' instead '" + ccore_library_version + "').\n" +
                  "Probably library has not been successfully installed.\n" +
                  "Please, contact 'pyclustering@yandex.ru'.")

        return ccore_library.__library


    @staticmethod
    def __check_library_integrity():
        try:
            ccore_library.__library.get_interface_description.restype = c_char_p
            result = ccore_library.__library.get_interface_description()
            
            if len(result) > 0:
                ccore_library.__workable = True
        
        except:
            ccore_library.__workable = False
        
        return ccore_library.__workable


    @staticmethod
    def __check_library_version():
        version = "unknown"

        try:
            ccore_library.__library.get_interface_version.restype = c_char_p
            version_cptr = ccore_library.__library.get_interface_version()

            ccore_version = version_cptr.decode("utf-8")
            if ccore_version == ccore_library_version:
                ccore_library.__workable = True
            else:
                ccore_library.__workable = False

        except:
            ccore_library.__workable = False

        return ccore_library.__workable, version
