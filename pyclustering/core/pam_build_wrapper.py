"""!

@brief CCORE Wrapper for PAM BUILD algorithm.

@authors Andrei Novikov (pyclustering@yandex.ru)
@date 2014-2020
@copyright BSD-3-Clause

"""


from ctypes import c_double, c_size_t, POINTER

from pyclustering.core.converter import convert_data_type
from pyclustering.core.wrapper import ccore_library
from pyclustering.core.pyclustering_package import pyclustering_package, package_builder, package_extractor


def pam_build(sample, amount, pointer_metric, data_type):
    pointer_data = package_builder(sample, c_double).create()
    c_data_type = convert_data_type(data_type)

    ccore = ccore_library.get()
    ccore.pam_build_algorithm.restype = POINTER(pyclustering_package)
    package = ccore.pam_build_algorithm(pointer_data, c_size_t(amount), pointer_metric, c_data_type)

    results = package_extractor(package).extract()
    ccore.free_pyclustering_package(package)

    if isinstance(results, bytes):
        raise RuntimeError(results.decode('utf-8'))

    return results[0]
