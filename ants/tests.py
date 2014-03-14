
import unittest
from support import read_sample
from ants.clustering import clustering

class Test(unittest.TestCase):
    def templateClustering(self, file, num_ants, size_lattice, count_iteration,   ):
        sample = read_sample(file);
        return clustering( num_ants, size_lattice, count_iteration, sample, len(sample) )

    def testClusteringSampleSimple1(self):
        data_on_lattice = self.templateClustering( '../Samples/SampleSimpleForAntsClustering1.txt', 10, 11, 100000 )
        assert len(data_on_lattice) == 42;
