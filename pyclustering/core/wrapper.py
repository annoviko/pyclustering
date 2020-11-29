"""!

@brief Wrapper for CCORE library (part of this project).

@authors Andrei Novikov (pyclustering@yandex.ru)
@date 2014-2020
@copyright BSD-3-Clause

"""


import sys
import warnings

from ctypes import *

from pyclustering.core.definitions import *


ccore_library_instance = None
ccore_library_version = "0.11.0"


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
            warnings.warn("The C/C++ pyclustering is not supported for platform '" + sys.platform + "' (" + platform.architecture()[0] + ").\n" +
                          "Falling back on python implementation.\n" +
                          "For more information, contact 'pyclustering@yandex.ru'.", ResourceWarning)
            
            return None
    
        if os.path.exists(PATH_PYCLUSTERING_CCORE_LIBRARY) is False:
            warnings.warn("The C/C++ pyclustering is not found (expected core location: '" + PATH_PYCLUSTERING_CCORE_LIBRARY + "').\n" +
                          "Probably library has not been successfully installed ('" + sys.platform + "', '" + platform.architecture()[0] + "').\n" +
                          "Falling back on python implementation.\n" +
                          "For more information, contact 'pyclustering@yandex.ru'.", ResourceWarning)
            
            return None

        ccore_library.__library = cdll.LoadLibrary(PATH_PYCLUSTERING_CCORE_LIBRARY)
        if ccore_library.__check_library_integrity() is False:
            warnings.warn("Impossible to mark C/C++ pyclustering library as a workable due to compatibility issues " +
                          "('" + sys.platform + "', '" + platform.architecture()[0] + "').\n" +
                          "Falling back on python implementation.\n" +
                          "For more information, contact 'pyclustering@yandex.ru'.", ResourceWarning)
            
            return None

        result, version = ccore_library.__check_library_version()
        if result is False:
            warnings.warn("Incompatible C/C++ pyclustering library is being used ('" + version +"' instead of '" + ccore_library_version + "').\n" +
                          "Probably library has not been successfully installed.\n" +
                          "Please, contact 'pyclustering@yandex.ru'.", ResourceWarning)

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
