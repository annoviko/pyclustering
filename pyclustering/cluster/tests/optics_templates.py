"""!

@brief Test templates for OPTICS clustering module.

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


from pyclustering.cluster.optics import optics, ordering_analyser

from pyclustering.utils import read_sample, calculate_distance_matrix

from pyclustering.tests.assertion import assertion



class OpticsTestTemplates:
    @staticmethod
    def templateClusteringResults(path, radius, neighbors, amount_clusters, expected_length_clusters, ccore):
        OpticsTestTemplates.templateClusteringResultsSpecificData('points', path, radius, neighbors, amount_clusters, expected_length_clusters, ccore)


    @staticmethod
    def templateClusteringResultsDistanceMatrix(path, radius, neighbors, amount_clusters, expected_length_clusters, ccore):
        OpticsTestTemplates.templateClusteringResultsSpecificData('distance_matrix', path, radius, neighbors, amount_clusters, expected_length_clusters, ccore)


    @staticmethod
    def templateClusteringResultsSpecificData(data_type, path, radius, neighbors, amount_clusters, expected_length_clusters, ccore):
        sample = read_sample(path)

        if data_type == 'distance_matrix':
            input_data = calculate_distance_matrix(sample)
        else:
            input_data = sample

        optics_instance = optics(input_data, radius, neighbors, amount_clusters, ccore, data_type=data_type)
        optics_instance.process()

        clusters = optics_instance.get_clusters()
        noise = optics_instance.get_noise()
        optics_objects = optics_instance.get_optics_objects()

        object_indexes = set( [ obj.index_object for obj in optics_objects ] )
        assertion.eq(len(optics_objects), len(object_indexes))
        for obj in optics_objects:
            if obj.core_distance is not None:
                assertion.ge(obj.core_distance, 0)

            if obj.reachability_distance is not None:
                assertion.ge(obj.reachability_distance, 0)

        assert sum([len(cluster) for cluster in clusters]) + len(noise) == len(sample)
        assert len(clusters) == len(expected_length_clusters)
        assert sum([len(cluster) for cluster in clusters]) == sum(expected_length_clusters)
        assert sorted([len(cluster) for cluster in clusters]) == sorted(expected_length_clusters)

        if amount_clusters is not None:
            analyser = ordering_analyser(optics_instance.get_ordering())
            assert len(analyser) > 0

            amount_clusters, borders = analyser.extract_cluster_amount(optics_instance.get_radius())
            assert amount_clusters == len(expected_length_clusters)
            assert len(borders) == amount_clusters - 1