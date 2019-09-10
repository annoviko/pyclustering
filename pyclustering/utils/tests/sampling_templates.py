"""!

@brief Test templates for sampling module.

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

import collections

from scipy import stats

from pyclustering.tests.assertion import assertion



class sampling_test_template:
    @staticmethod
    def random_sampling(data, n, algorithm, repeat, ccore=True):
        for _ in range(repeat):
            sample = algorithm(data, n)
            unique_values = set(sample)

            assertion.eq(n, len(sample))
            assertion.eq(len(unique_values), len(sample))


    @staticmethod
    def uniform_distribution(data, n, algorithm, repeat, supremum_cdf=0.06, ccore=True):
        # Supremum CDF < 0.06 is almost about uniform distribution (for R algorithm).
        # Supremum CDF < 0.4 is for X algorithm
        min_value = min(data)
        max_value = max(data)
        scale = max_value - min_value

        stream = collections.deque()
        for _ in range(repeat):
            stream += algorithm(data, n)

        D, pvalue = stats.kstest(stream, stats.uniform(loc=min_value, scale=scale).cdf)
        assertion.gt(supremum_cdf, D)
