"""!

@brief Test templates for Elbow clustering module.

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


from pyclustering.utils import read_sample

from pyclustering.cluster.center_initializer import kmeans_plusplus_initializer
from pyclustering.cluster.elbow import elbow

from pyclustering.tests.assertion import assertion

from pyclustering.samples import answer_reader


class elbow_test_template:
    @staticmethod
    def calculate_elbow(path_to_data, path_to_answer, kmin, kmax, ccore, **kwargs):
        repeat = 15  # Elbow method randomly chooses initial centers therefore we need to repeat test if it fails.
        testing_result = False

        initializer = kwargs.get('initializer', kmeans_plusplus_initializer)

        sample = read_sample(path_to_data)

        answer = None
        if path_to_answer is not None:
            answer = answer_reader(path_to_answer)

        additional_info = []

        for _ in range(repeat):
            elbow_instance = elbow(sample, kmin, kmax, ccore=ccore, initializer=initializer)
            elbow_instance.process()

            actual_elbow = elbow_instance.get_amount()
            actual_wce = elbow_instance.get_wce()

            assertion.gt(actual_elbow, kmin)
            assertion.lt(actual_elbow, kmax)
            assertion.eq(len(actual_wce), kmax - kmin)
            assertion.lt(actual_wce[-1], actual_wce[0] + 0.0000001)

            if (answer is not None) and (actual_elbow != len(answer.get_clusters())):
                additional_info.append(actual_elbow)
                continue

            testing_result = True
            break

        message = None
        if answer is not None:
            message = str(len(answer.get_clusters())) + ": " + str(additional_info)
        assertion.true(testing_result, message=message)
