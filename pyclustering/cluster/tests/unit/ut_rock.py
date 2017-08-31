"""!

@brief Unit-tests for ROCK algorithm.

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


import unittest;

from pyclustering.cluster.tests.rock_templates import RockTestTemplates;

from pyclustering.samples.definitions import SIMPLE_SAMPLES;


class RockUnitTest(unittest.TestCase):  
    def testClusterAllocationSampleSimple1(self):
        RockTestTemplates.templateLengthProcessData(SIMPLE_SAMPLES.SAMPLE_SIMPLE1, 1, 2, 0.5, [5, 5]);
        RockTestTemplates.templateLengthProcessData(SIMPLE_SAMPLES.SAMPLE_SIMPLE1, 5, 1, 0.5, [10]);
        
    def testClusterAllocationSampleSimple2(self):
        RockTestTemplates.templateLengthProcessData(SIMPLE_SAMPLES.SAMPLE_SIMPLE2, 1, 3, 0.5, [10, 5, 8]);
        RockTestTemplates.templateLengthProcessData(SIMPLE_SAMPLES.SAMPLE_SIMPLE2, 5, 1, 0.5, [23]);
        
    def testClusterAllocationSampleSimple3(self):
        RockTestTemplates.templateLengthProcessData(SIMPLE_SAMPLES.SAMPLE_SIMPLE3, 1, 4, 0.5, [10, 10, 10, 30]);
        
    def testClusterAllocationSampleSimple3WrongRadius(self):
        RockTestTemplates.templateLengthProcessData(SIMPLE_SAMPLES.SAMPLE_SIMPLE3, 1.7, 4, 0.5, [10, 10, 10, 30]);
        
    def testClusterAllocationSampleSimple4(self):
        RockTestTemplates.templateLengthProcessData(SIMPLE_SAMPLES.SAMPLE_SIMPLE4, 1, 5, 0.5, [15, 15, 15, 15, 15]);    

    def testClusterAllocationSampleSimple4WrongRadius(self):
        RockTestTemplates.templateLengthProcessData(SIMPLE_SAMPLES.SAMPLE_SIMPLE4, 1.5, 5, 0.5, [15, 15, 15, 15, 15]);  

    def testClusterAllocationSampleSimple5(self):
        RockTestTemplates.templateLengthProcessData(SIMPLE_SAMPLES.SAMPLE_SIMPLE5, 1, 4, 0.5, [15, 15, 15, 15]);    
 

    def testClusterAllocationIncorrectNumberClusters(self):
        RockTestTemplates.templateLengthProcessData(SIMPLE_SAMPLES.SAMPLE_SIMPLE4, 1, 4, 0.5, [15, 15, 15, 15, 15]);


if __name__ == "__main__":
    unittest.main();