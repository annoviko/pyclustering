"""!

@brief Wrapper for CCORE library (part of this project).

@authors Andrei Novikov (pyclustering@yandex.ru)
@date 2014-2017
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


def load_core():
    if (PATH_PYCLUSTERING_CCORE_LIBRARY is None):
        raise NameError("The pyclustering core is not supported for platform '" + sys.platform + "'.");

    if (os.path.exists(PATH_PYCLUSTERING_CCORE_LIBRARY) is False):
        raise NameError("The pyclustering core is not found (expected core location: '" + PATH_PYCLUSTERING_CCORE_LIBRARY + "').\n" + 
                        "Probably pyclustering library has not been successfully installed.\n" + 
                        "Please, contact to 'pyclustering@yandex.ru'.");

    return cdll.LoadLibrary(PATH_PYCLUSTERING_CCORE_LIBRARY);

