"""!

@brief Module provides various random sampling algorithms.

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


import random


def reservoir_r(data, n):
    """!
    @brief Performs data sampling using Reservoir Algorithm R.
    @details Algorithm complexity O(n). Implementation is based on paper @cite article::utils::sampling::1. Average
              number of uniform random variates: \f$N - n\f$.

    @param[in] data (list): Input data for sampling.
    @param[in] n (uint): Size of sample that should be extracted from 'data'.

    @return (list) Sample with size 'n' from 'data'.

    Generate random samples with 5 elements and with 3 elements using Reservoir Algorithm R:
    @code
        data = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20]
        sample = reservoir_r(data, 5)   # generate sample with 5 elements for 'data'.
        print(sample)

        sample = reservoir_r(data, 3)   # generate sample with 3 elements for 'data'.
        print(sample)
    @endcode

    Output example for the code above:
    @code
        [20, 7, 17, 12, 11]
        [12, 2, 10]
    @endcode

    """
    if n > len(data):
        raise ValueError("Incorrect sampling value 'n' (%d) that should be bigger then data size (%d).")

    random.seed()
    reservoir = data[0:n]

    for i in range(n, len(data)):
        m = random.randrange(0, i + 1)
        if m < n:
            reservoir[m] = data[i]

    return reservoir


def reservoir_x(data, n):
    """!
    @brief Performs data sampling using Reservoir Algorithm X.
    @details Algorithm complexity O(n). Implementation is based on paper @cite article::utils::sampling::1. Average
              number of uniform random variates:
              \f[\approx 2n\ln \left (\frac{N}{n} \right)\f]

    @param[in] data (list): Input data for sampling.
    @param[in] n (uint): Size of sample that should be extracted from 'data'.

    @return (list) Sample with size 'n' from 'data'.

    Generate random sample with 5 elements using Reservoir Algorithm X:
    @code
        data = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20]
        sample = reservoir_x(data, 10)   # generate sample with 5 elements for 'data'.
        print(sample)
    @endcode

    Output example for the code above:
    @code
        [0, 20, 2, 16, 13, 15, 19, 18, 10, 9]
    @endcode

    """
    def calculate_skip_value(t, size, skip):
        return pow(t + 1 - size, skip + 1) / pow(t + 1, skip + 1)

    def generate_skip_value(t, size):
        threshold, skip = random.random(), 0
        while calculate_skip_value(t, size, skip) > threshold:
            skip += 1
        return skip

    if n > len(data):
        raise ValueError("Incorrect sampling value 'n' (%d) that should be bigger then data size (%d).")

    random.seed()
    reservoir = data[0:n]

    i = n
    while i < len(data):
        i += generate_skip_value(i, n)

        if i < len(data):
            m = random.randrange(0, n)
            reservoir[m] = data[i]

        i += 1

    return reservoir
