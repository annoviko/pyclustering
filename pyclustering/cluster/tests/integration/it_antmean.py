"""!

@brief Unit-tests for ant means algorithm.

@authors Andrei Novikov, Aleksey Kukushkin (pyclustering@yandex.ru)
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

import unittest

from pyclustering.cluster.antmean import antmean


class AntmeanIntegrationTest(unittest.TestCase):
    """ """

    def templateClustering(self, samples, clusters):
        """ """

        algo = antmean(None)
        res = algo.process(len(clusters), samples)

        """
            Testing clusters
        """
        for i in range(len(res)):
            res[i].sort()
        
        for i in range(len(clusters)):
            clusters[i].sort()

            for j in range(len(res)):

                found_cl = True

                for k in range(len(clusters[i])):
                    if clusters[i][k] != res[j][k]:
                        found_cl = False
                        break
                
                if found_cl:
                    break
            
            assert found_cl

    def testSimpleTwoClusters(self):
        self.templateClustering([[0, 0], [1, 1], [10, 10], [11, 11], [-2, -2], [0.55, -1.26], [13.25, 12.12]],
                                [[0, 1, 4, 5], [2, 3, 6]])


if __name__ == "__main__":
    unittest.main()
