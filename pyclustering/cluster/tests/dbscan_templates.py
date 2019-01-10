"""!

@brief Test templates for DBSCAN clustering module.

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


from random import random, shuffle

from pyclustering.utils import read_sample, calculate_distance_matrix
from pyclustering.cluster.dbscan import dbscan

from pyclustering.tests.assertion import assertion

from pyclustering.samples import answer_reader


class DbscanTestTemplates:
    @staticmethod
    def templateClusteringResults(path, radius, neighbors, expected_length_clusters, ccore, **kwargs):
        random_order = kwargs.get('random_order', False)

        sample = read_sample(path)
        if random_order:
            shuffle(sample)
         
        dbscan_instance = dbscan(sample, radius, neighbors, ccore)
        dbscan_instance.process()
         
        clusters = dbscan_instance.get_clusters()
        noise = dbscan_instance.get_noise()

        assertion.eq(len(sample), sum([len(cluster) for cluster in clusters]) + len(noise))
        assertion.eq(sum(expected_length_clusters), sum([len(cluster) for cluster in clusters]))
        assertion.eq(expected_length_clusters, sorted([len(cluster) for cluster in clusters]))


    @staticmethod
    def templateClusteringWithAnswers(sample_path, answer_path, radius, neighbors, ccore, **kwargs):
        random_order = kwargs.get('random_order', False)
        repeat = kwargs.get('repeat', 1)

        for _ in range(repeat):
            sample = read_sample(sample_path)

            sample_index_map = [ i for i in range(len(sample)) ]
            if random_order:
                shuffle(sample_index_map)

            sample_shuffled = [ sample[i] for i in sample_index_map ]

            dbscan_instance = dbscan(sample_shuffled, radius, neighbors, ccore)
            dbscan_instance.process()

            clusters = dbscan_instance.get_clusters()
            noise = dbscan_instance.get_noise()

            for cluster in clusters:
                for i in range(len(cluster)):
                    cluster[i] = sample_index_map[cluster[i]]

            for i in range(len(noise)):
                noise[i] = sample_index_map[noise[i]]
            noise = sorted(noise)

            reader = answer_reader(answer_path)
            expected_noise = sorted(reader.get_noise())
            expected_length_clusters = reader.get_cluster_lengths()

            assertion.eq(len(sample), sum([len(cluster) for cluster in clusters]) + len(noise))
            assertion.eq(sum(expected_length_clusters), sum([len(cluster) for cluster in clusters]))
            assertion.eq(expected_length_clusters, sorted([len(cluster) for cluster in clusters]))
            assertion.eq(expected_noise, noise)


    @staticmethod
    def templateClusteringResultsRandomize(path, radius, neighbors, expected_length_clusters, ccore):
        for i in range(10):
            DbscanTestTemplates.templateClusteringResults(path, radius, neighbors, expected_length_clusters, ccore,
                                                          random_order=True)


    @staticmethod
    def templateLengthProcessData(path_to_file, radius, min_number_neighbors, max_number_neighbors, ccore):
        DbscanTestTemplates.templateLengthProcessSpecificData('points', path_to_file, radius,
                                                              min_number_neighbors, max_number_neighbors, ccore)

    @staticmethod
    def templateLengthProcessDistanceMatrix(path_to_file, radius, min_number_neighbors, max_number_neighbors, ccore):
        DbscanTestTemplates.templateLengthProcessSpecificData('points', path_to_file, radius,
                                                              min_number_neighbors, max_number_neighbors, ccore)

    @staticmethod
    def templateLengthProcessSpecificData(data_type, path_to_file, radius, min_number_neighbors, max_number_neighbors, ccore):
        for _ in range(min_number_neighbors, max_number_neighbors, 1):
            sample = read_sample(path_to_file)

            if data_type == 'distance_matrix':
                input_data = calculate_distance_matrix(sample)
            elif data_type == 'points':
                input_data = sample
            else:
                raise ValueError("Incorrect data type '%s' is specified" % data_type)

            dbscan_instance = dbscan(input_data, radius, min_number_neighbors, ccore, data_type=data_type)
            dbscan_instance.process()

            clusters = dbscan_instance.get_clusters()
            noise = dbscan_instance.get_noise()

            length = len(noise)
            length += sum([len(cluster) for cluster in clusters])

            assertion.eq(len(sample), length)


    @staticmethod
    def templateClusterAllocationOneDimensionData(ccore_flag):
        DbscanTestTemplates.templateClusterAllocationOneDimensionDataSpecificData('points', ccore_flag)


    @staticmethod
    def templateClusterAllocationOneDimensionDistanceMatrix(ccore_flag):
        DbscanTestTemplates.templateClusterAllocationOneDimensionDataSpecificData('distance_matrix', ccore_flag)


    @staticmethod
    def templateClusterAllocationOneDimensionDataSpecificData(data_type, ccore_flag):
        for _ in range(50):
            sample = [[random()] for _ in range(10)] + [[random() + 3] for _ in range(10)] + [[random() + 6] for _ in range(10)] + [[random() + 9] for _ in range(10)]

            if data_type == 'distance_matrix':
                input_data = calculate_distance_matrix(sample)
            elif data_type == 'points':
                input_data = sample
            else:
                raise ValueError("Incorrect data type '%s' is specified" % data_type)

            dbscan_instance = dbscan(input_data, 1.0, 2, ccore_flag, data_type=data_type)
            dbscan_instance.process()

            clusters = dbscan_instance.get_clusters()

            assertion.eq(4, len(clusters))
            for cluster in clusters:
                assertion.eq(10, len(cluster))


    @staticmethod
    def templateClusteringDistanceMatrix(path_to_file, radius, neighbors, expected_length_clusters, ccore):
        sample = read_sample(path_to_file)
        distance_matrix = calculate_distance_matrix(sample)

        dbscan_instance = dbscan(distance_matrix, radius, neighbors, ccore, data_type='distance_matrix')
        dbscan_instance.process()

        clusters = dbscan_instance.get_clusters()
        noise = dbscan_instance.get_noise()

        assertion.eq(len(sample), sum([len(cluster) for cluster in clusters]) + len(noise))
        assertion.eq(sum(expected_length_clusters), sum([len(cluster) for cluster in clusters]))
        assertion.eq(expected_length_clusters, sorted([len(cluster) for cluster in clusters]))