"""!

@brief Test runner for unit and integration tests of oscillatory and neural networks.

@authors Andrei Novikov (pyclustering@yandex.ru)
@date 2014-2020
@copyright BSD-3-Clause

"""


import unittest
from pyclustering.tests.suite_holder import suite_holder

# Generate images without having a window appear.
import matplotlib
matplotlib.use('Agg')

from pyclustering.nnet.tests.integration import nnet_integration_tests
from pyclustering.nnet.tests.unit import nnet_unit_tests


class nnet_tests(suite_holder):
    def __init__(self):
        super().__init__()
        nnet_tests.fill_suite(self.get_suite())

    @staticmethod
    def fill_suite(nnet_suite):
        nnet_integration_tests.fill_suite(nnet_suite)
        nnet_unit_tests.fill_suite(nnet_suite)
