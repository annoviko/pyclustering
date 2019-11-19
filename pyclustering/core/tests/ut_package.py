"""!

@brief Unit-tests for pyclustering package that is used for exchange between ccore library and python code.

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


import unittest

import numpy

from pyclustering.core.pyclustering_package import package_builder, package_extractor

from ctypes import c_ulong, c_size_t, c_double, c_uint, c_float


class Test(unittest.TestCase):
    def templatePackUnpack(self, dataset, c_type_data = None):
        package_pointer = package_builder(dataset, c_type_data).create()
        unpacked_package = package_extractor(package_pointer).extract()

        packing_data = dataset
        if (isinstance(packing_data, numpy.matrix)):
            packing_data = dataset.tolist()

        assert self.compare_containers(packing_data, unpacked_package);


    def compare_containers(self, container1, container2):
        def is_container(container):
            return (isinstance(container, list) or isinstance(container, tuple))
        
        if (len(container1) == 0 and len(container2) == 0):
            return True

        if (len(container1) != len(container2)):
            return False
        
        for index in range(len(container1)):
            if (is_container(container1[index]) and is_container(container2[index])):
                return self.compare_containers(container1[index], container2[index])
            
            elif (is_container(container1[index]) == is_container(container2[index])):
                if (container1[index] != container2[index]):
                    return False
            
            else:
                return False
            
            return True


    def testListInteger(self):
        self.templatePackUnpack([1, 2, 3, 4, 5])

    def testListIntegerSingle(self):
        self.templatePackUnpack([2])

    def testListIntegerNegative(self):
        self.templatePackUnpack([-1, -2, -10, -20])

    def testListIntegerNegativeAndPositive(self):
        self.templatePackUnpack([-1, 26, -10, -20, 13])

    def testListFloat(self):
        self.templatePackUnpack([1.1, 1.2, 1.3, 1.4, 1.5, 1.6])

    def testListFloatNegativeAndPositive(self):
        self.templatePackUnpack([1.1, -1.2, -1.3, -1.4, 1.5, -1.6])

    def testListLong(self):
        self.templatePackUnpack([100000000, 2000000000])

    def testListEmpty(self):
        self.templatePackUnpack([])

    def testListOfListInteger(self):
        self.templatePackUnpack([ [1, 2, 3], [4, 5, 6], [7, 8, 9] ])

    def testListOfListDouble(self):
        self.templatePackUnpack([ [1.1, 5.4], [1.3], [1.4, -9.4] ])

    def testListOfListWithGaps(self):
        self.templatePackUnpack([ [], [1, 2, 3], [], [4], [], [5, 6, 7] ])

    def testListSpecifyUnsignedLong(self):
        self.templatePackUnpack([1, 2, 3, 4, 5], c_ulong)

    def testListSpecifyUnsignedSizeT(self):
        self.templatePackUnpack([1, 2, 3, 4, 5], c_size_t)

    def testListSpecifyDouble(self):
        self.templatePackUnpack([1.1, 1.6, -7.8], c_double)

    def testListOfListSpecifySizeT(self):
        self.templatePackUnpack([ [1, 2, 3], [4, 5] ], c_size_t)

    def testListOfListSpecifyUnsignedIntWithGaps(self):
        self.templatePackUnpack([ [1, 2, 3], [], [4, 5], [], [] ], c_uint)

    def testListOfListEmpty(self):
        self.templatePackUnpack([ [], [], [] ])

    def testListOfListOfListInteger(self):
        self.templatePackUnpack([ [ [1], [2] ], [ [3], [4] ], [ [5, 6], [7, 8] ] ])

    def testTupleInterger(self):
        self.templatePackUnpack([ (1, 2, 3), (4, 5), (6, 7, 8, 9) ], c_uint)

    def testTupleFloat(self):
        self.templatePackUnpack([ (1.0, 2.0, 3.8), (4.6, 5.0), (6.8, 7.4, 8.5, 9.6) ], c_float)

    def testTupleEmpty(self):
        self.templatePackUnpack([ (), (), () ])

    def testNumpyMatrixOneColumn(self):
        self.templatePackUnpack(numpy.matrix([[1.0], [2.0], [3.0]]), c_double)

    def testNumpyMatrixTwoColumns(self):
        self.templatePackUnpack(numpy.matrix([[1.0, 1.0], [2.0, 2.0]]), c_double)

    def testNumpyMatrixThreeColumns(self):
        self.templatePackUnpack(numpy.matrix([[1.1, 2.2, 3.3], [2.2, 3.3, 4.4], [3.3, 4.4, 5.5]]), c_double)
