"""!

@brief Common definition for CCORE.

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

import pyclustering.core as core
import os
import platform

from sys import platform as _platform


# Path to CCORE library - pyclustering core.
PATH_PYCLUSTERING_CCORE_LIBRARY = None


core_architecture = None
if platform.architecture()[0] == "64bit":
    core_architecture = "64-bit"
else:
    core_architecture = "32-bit"


if (_platform == "linux") or (_platform == "linux2"):
    PATH_PYCLUSTERING_CCORE_LIBRARY = core.__path__[0] + os.sep + core_architecture + os.sep + "linux" + os.sep + "ccore.so"

elif _platform == "darwin":
    PATH_PYCLUSTERING_CCORE_LIBRARY = core.__path__[0] + os.sep + core_architecture + os.sep + "macos" + os.sep + "ccore.so"

elif _platform == "win32":
    PATH_PYCLUSTERING_CCORE_LIBRARY = core.__path__[0] + os.sep + core_architecture + os.sep + "win" + os.sep + "ccore.dll"

elif _platform == "cygwin":
    PATH_PYCLUSTERING_CCORE_LIBRARY = core.__path__[0] + os.sep + core_architecture + os.sep + "win" + os.sep + "ccore.so"
