"""!

@brief Unit-test runner for containers.

@authors Andrei Novikov (pyclustering@yandex.ru)
@date 2014-2020
@copyright BSD-3-Clause

"""


from pyclustering.tests.suite_holder import suite_holder

from pyclustering.container.tests.unit import container_unit_tests


class container_tests(suite_holder):
    def __init__(self):
        super().__init__()
        container_unit_tests.fill_suite(self.get_suite())

    @staticmethod
    def fill_suite(container_suite):
        container_unit_tests.fill_suite(container_suite)
