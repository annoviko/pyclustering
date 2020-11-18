"""!

@brief Test templates for sampling module.

@authors Andrei Novikov (pyclustering@yandex.ru)
@date 2014-2020
@copyright BSD-3-Clause

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
