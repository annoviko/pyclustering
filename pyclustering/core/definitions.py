"""!

@brief Common definition for CCORE.

@authors Andrei Novikov (pyclustering@yandex.ru)
@date 2014-2020
@copyright BSD-3-Clause

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
    PATH_PYCLUSTERING_CCORE_LIBRARY = core.__path__[0] + os.sep + core_architecture + os.sep + "linux" + os.sep + "libpyclustering.so"

elif _platform == "darwin":
    PATH_PYCLUSTERING_CCORE_LIBRARY = core.__path__[0] + os.sep + core_architecture + os.sep + "macos" + os.sep + "libpyclustering.so"

elif _platform == "win32":
    PATH_PYCLUSTERING_CCORE_LIBRARY = core.__path__[0] + os.sep + core_architecture + os.sep + "win" + os.sep + "pyclustering.dll"

elif _platform == "cygwin":
    PATH_PYCLUSTERING_CCORE_LIBRARY = core.__path__[0] + os.sep + core_architecture + os.sep + "win" + os.sep + "libpyclustering.so"
