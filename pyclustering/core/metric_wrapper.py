"""!

@brief CCORE Wrapper for metrics.

@authors Andrei Novikov (pyclustering@yandex.ru)
@date 2014-2020
@copyright BSD-3-Clause

"""


from pyclustering.core.wrapper import ccore_library

from pyclustering.core.pyclustering_package import package_builder, package_extractor, pyclustering_package

from ctypes import c_double, c_size_t, POINTER, c_void_p, CFUNCTYPE

from pyclustering.utils.metric import type_metric


metric_callback = CFUNCTYPE(c_double, POINTER(pyclustering_package), POINTER(pyclustering_package))


class metric_wrapper:
    def __init__(self, type_metric_code, arguments, func):
        self.__func = lambda p1, p2: func(package_extractor(p1).extract(), package_extractor(p2).extract())

        package_arguments = package_builder(arguments, c_double).create()

        ccore = ccore_library.get()

        ccore.metric_create.restype = POINTER(c_void_p)

        self.__pointer = ccore.metric_create(c_size_t(type_metric_code), package_arguments, metric_callback(self.__func))


    def __del__(self):
        if self.__pointer:
            ccore = ccore_library.get()
            ccore.metric_destroy(self.__pointer)


    def __call__(self, point1, point2):
        point_package1 = package_builder(point1, c_double).create()
        point_package2 = package_builder(point2, c_double).create()

        ccore = ccore_library.get()

        ccore.metric_calculate.restype = c_double
        return ccore.metric_calculate(self.__pointer, point_package1, point_package2)


    def get_pointer(self):
        return self.__pointer


    @staticmethod
    def create_instance(metric):
        mtype = metric.get_type()
        arguments = []

        if mtype == type_metric.MINKOWSKI:
            arguments = [metric.get_arguments().get('degree')]

        elif mtype == type_metric.GOWER:
            arguments = metric.get_arguments().get('max_range')

        return metric_wrapper(mtype, arguments, metric.get_function())