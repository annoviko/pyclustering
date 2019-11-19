"""!

Unit-tests for utils module.

@authors Andrei Novikov (pyclustering@yandex.ru)
@date 2014-2019
@copyright GNU Public License

pyclustering is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

pyclustering is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.

"""

import unittest

# Generate images without having a window appear.
import matplotlib
matplotlib.use('Agg')

from pyclustering.cluster.kmeans import kmeans
from pyclustering.cluster.center_initializer import kmeans_plusplus_initializer

import pyclustering.utils as utils

from pyclustering.utils import euclidean_distance
from pyclustering.utils import average_neighbor_distance
from pyclustering.utils import read_sample
from pyclustering.utils import data_corners
from pyclustering.utils import norm_vector
from pyclustering.utils import rgb2gray
from pyclustering.utils import extract_number_oscillations
from pyclustering.utils import draw_clusters

from pyclustering.samples.definitions import SIMPLE_SAMPLES, IMAGE_SIMPLE_SAMPLES


class Test(unittest.TestCase):

    def testEuclideanDistance(self):
        point1 = [1, 2];
        point2 = [1, 3];
        point3 = [4, 6];
        
        # Tests for euclidean_distance
        assert euclidean_distance(point1, point2) == 1;
        assert euclidean_distance(point1, point1) == 0;
        assert euclidean_distance(point1, point3) == 5;

    
    def testFloatEuclideanDistance(self):
        assert euclidean_distance(0.5, 1.5) == 1;
        assert self.float_comparasion(euclidean_distance(1.6, 1.4), 0.2);
        assert self.float_comparasion(euclidean_distance(4.23, 2.14), 2.09);
    
    
    def testAverageNeighborFourDistance(self):
        points = [[0.0, 0.0], [0.0, 1.0], [1.0, 1.0], [1.0, 0.0]];
        
        assert average_neighbor_distance(points, 1) == 1.0;
        assert average_neighbor_distance(points, 2) == 1.0;
        assert self.float_comparasion(average_neighbor_distance(points, 3), 1.1381);


    def testAverageNeighborFourDistanceNegativeValues(self):
        points = [[0.0, 0.0], [0.0, -1.0], [-1.0, -1.0], [-1.0, 0.0]];
        
        assert average_neighbor_distance(points, 1) == 1.0;
        assert average_neighbor_distance(points, 2) == 1.0;
        assert self.float_comparasion(average_neighbor_distance(points, 3), 1.1381);
    
    
    def float_comparasion(self, float1, float2, eps = 0.0001):
        return ( (float1 + eps) > float2 and (float1 - eps) < float2 );
    
    
    def templateDataCorners(self, data_path, data_filter, expected_result):
        sample = read_sample(data_path);
        result = data_corners(sample, data_filter);
        
        assert result == expected_result;
    
    def testDataCornersSampleSimple01(self):
        self.templateDataCorners(SIMPLE_SAMPLES.SAMPLE_SIMPLE1, None, ([3.423602, 5.364477], [6.978178, 7.850364]));
    
    def testDataCornersSampleSimple01WithFilter(self):
        self.templateDataCorners(SIMPLE_SAMPLES.SAMPLE_SIMPLE1, [0, 1, 2, 3, 4], ([3.423602, 5.364477], [3.936690, 5.663041]));
    
    def testDataCornersSampleSimple02(self):
        self.templateDataCorners(SIMPLE_SAMPLES.SAMPLE_SIMPLE2, None, ([3.177711, 0.022688], [7.835975, 6.704815]));

    def testDataCornersSampleSimple02WithFilter(self):
        self.templateDataCorners(SIMPLE_SAMPLES.SAMPLE_SIMPLE2, [10, 11, 12, 13, 14], ([7.062946, 6.022702], [7.500097, 6.704815]));

    def testVectorLength(self):
        assert 10 == norm_vector([6, 8]);
        assert self.float_comparasion(4.219, norm_vector([2.2, 3.6]), 0.001);
        assert self.float_comparasion(5.280, norm_vector([-4.8, -2.2]), 0.001);

    def testRgbToGray(self):
        rgb_pixels = [ [127, 127, 127], [255, 255, 255], [0, 0, 0] ];
        result = rgb2gray(rgb_pixels);

        assert 3 == len(result);
        assert 127 == round(result[0]);
        assert 255 == round(result[1]);
        assert 0 == round(result[2]);

    def testExtractNumberOscillationsMonotonicDown(self):
        value = [ [10.0], [9.5], [9.0], [8.5], [8.0], [7.5], [7.0], [6.5], [6.0], [5.5], [5.0] ];
        assert extract_number_oscillations(value, 0, 8.0) == 0;

    def testExtractNumberOscillationsMonotonicUp(self):
        value = [ [1.0], [1.5], [2.0], [2.5], [3.0], [3.5], [4.0], [4.5], [5.0], [5.5], [6.0] ];
        assert extract_number_oscillations(value, 0, 4.0) == 0;

    def testExtractNumberOscillationsMonotonicUpSlightlyDown(self):
        value = [ [1.0], [1.5], [2.0], [2.5], [3.0], [3.5], [4.0], [4.5], [5.0], [4.5], [4.0] ];
        assert extract_number_oscillations(value, 0, 2.0) == 0;

    def testExtractNumberOscillationsMonotonicDownSlightlyUp(self):
        value = [ [10.0], [9.5], [9.0], [8.5], [8.0], [7.5], [7.0], [6.5], [7.0], [7.1], [7.3] ];
        assert extract_number_oscillations(value, 0, 7.5) == 0;

    def testExtractNumberOscillationsOnePeriod(self):
        value = [ [0.0], [1.0], [0.0] ];
        assert extract_number_oscillations(value, 0, 0.5) == 1;

    def testExtractNumberOscillationsOnePeriodWithHalf(self):
        value = [ [0.0], [1.0], [0.0], [1.0] ];
        assert extract_number_oscillations(value, 0, 0.5) == 1;

    def testExtractNumberOscillationsTwoPeriods(self):
        value = [ [0.0], [1.0], [0.0], [1.0], [0.0] ];
        assert extract_number_oscillations(value, 0, 0.5) == 2;

    def testExtractNumberOscillationsThreePeriods(self):
        value = [ [0.0], [1.0], [0.0], [1.0], [0.0], [1.0], [0.0] ];
        assert extract_number_oscillations(value, 0, 0.5) == 3;

    def testExtractNumberOscillationsFourPeriods(self):
        value = [ [0.0], [1.0], [0.0], [1.0], [0.0], [1.0], [0.0], [1.0], [0.0] ];
        assert extract_number_oscillations(value, 0, 0.5) == 4;

    def testExtractNumberOscillationsFourPeriodsOnThreshold(self):
        value = [ [0.0], [1.0], [0.0], [1.0], [0.0], [1.0], [0.0], [1.0], [0.0] ];
        assert extract_number_oscillations(value, 0, 1.0) == 4;

    def testExtractNumberOscillationsFourPeriodsUnderThreshold(self):
        value = [ [0.0], [1.0], [0.0], [1.0], [0.0], [1.0], [0.0], [1.0], [0.0] ];
        assert extract_number_oscillations(value, 0, 1.5) == 0;

    def testExtractNumberOscillationsUpDownUp(self):
        value = [ [1.0], [0.0], [1.0] ];
        assert extract_number_oscillations(value, 0, 0.5) == 0;

    def testExtractNumberOscillationsDownUpDown(self):
        value = [ [0.0], [1.0], [0.0] ];
        assert extract_number_oscillations(value, 0, 0.5) == 1;

    def templateDrawClustersNoFailure(self, data_path, amount_clusters):
        sample = read_sample(data_path);
        
        initial_centers = kmeans_plusplus_initializer(sample, amount_clusters).initialize();
        kmeans_instance = kmeans(sample, initial_centers, amount_clusters);
        
        kmeans_instance.process();
        clusters = kmeans_instance.get_clusters();
        
        ax = draw_clusters(sample, clusters);
        assert None != ax;

    def testDrawClustersOneCluster(self):
        self.templateDrawClustersNoFailure(SIMPLE_SAMPLES.SAMPLE_SIMPLE1, 1);

    def testDrawClustersTwoClusters(self):
        self.templateDrawClustersNoFailure(SIMPLE_SAMPLES.SAMPLE_SIMPLE1, 2);

    def testDrawClustersThreeClusters(self):
        self.templateDrawClustersNoFailure(SIMPLE_SAMPLES.SAMPLE_SIMPLE2, 3);

    def testDrawClustersOneDimension(self):
        self.templateDrawClustersNoFailure(SIMPLE_SAMPLES.SAMPLE_SIMPLE7, 2);

    def testDrawClustersTwoDimensions(self):
        self.templateDrawClustersNoFailure(SIMPLE_SAMPLES.SAMPLE_SIMPLE1, 2);

    def testDrawClustersThreeDimensions(self):
        self.templateDrawClustersNoFailure(SIMPLE_SAMPLES.SAMPLE_SIMPLE11, 2);

    def testDrawSegmentationResultNoFailure(self):
        data = utils.read_image(IMAGE_SIMPLE_SAMPLES.IMAGE_SIMPLE01);
    
        kmeans_instance = kmeans(data, [[255, 0, 0], [0, 0, 255], [180, 136, 0], [255, 255, 255]]);
        kmeans_instance.process();
        
        clusters = kmeans_instance.get_clusters();
        utils.draw_image_mask_segments(IMAGE_SIMPLE_SAMPLES.IMAGE_SIMPLE01, clusters);
        utils.draw_image_color_segments(IMAGE_SIMPLE_SAMPLES.IMAGE_SIMPLE01, clusters);

    def testCalculateMatrixDistance(self):
        data = [ [0], [2], [4] ];
        matrix = utils.calculate_distance_matrix(data);
        assert matrix == [ [0.0, 2.0, 4.0], [2.0, 0.0, 2.0], [4.0, 2.0, 0.0] ];
