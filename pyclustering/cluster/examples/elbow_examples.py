"""!

@brief Examples of usage and demonstration of abilities of Elbow method.

@authors Andrey Novikov (pyclustering@yandex.ru)
@date 2014-2018
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


import matplotlib.pyplot as plt

from pyclustering.cluster.elbow import elbow

from pyclustering.utils import read_sample

from pyclustering.samples.definitions import SIMPLE_SAMPLES


def elbow_analysis(sample_file_path, kmin, kmax, **kwargs):
    sample = read_sample(sample_file_path)

    elbow_instance = elbow(sample, kmin, kmax)
    elbow_instance.process()

    amount_clusters = elbow_instance.get_amount()
    wce = elbow_instance.get_wce()

    print("Sample '%s': Obtained amount of clusters: '%d'." % (sample_file_path, amount_clusters))

    figure = plt.figure(1)
    ax = figure.add_subplot(111)
    ax.plot(range(kmin, kmax), wce)
    ax.grid(True)
    plt.show()


def sample_simple_01():
    elbow_analysis(SIMPLE_SAMPLES.SAMPLE_SIMPLE1, 1, 10)

def sample_simple_02():
    elbow_analysis(SIMPLE_SAMPLES.SAMPLE_SIMPLE2, 1, 10)

def sample_simple_03():
    elbow_analysis(SIMPLE_SAMPLES.SAMPLE_SIMPLE3, 1, 10)

def sample_simple_04():
    elbow_analysis(SIMPLE_SAMPLES.SAMPLE_SIMPLE4, 1, 10)


sample_simple_01()
sample_simple_02()
sample_simple_03()
sample_simple_04()