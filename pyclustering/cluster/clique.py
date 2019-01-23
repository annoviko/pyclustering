"""!

@brief Cluster analysis algorithm: CLIQUE
@details Implementation based on paper @cite article::clique::1.

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


class spatial_block:
    def __init__(self):
        pass


class clique:
    def __init__(self, data, amount_intervals, density_threshold):
        self.__data = data
        self.__amount_intervals = amount_intervals
        self.__density_threshold = density_threshold

        self.__clusters = []
        self.__noise = []

        self.__validate_arguments()


    def process(self):
        pass


    def get_clusters(self):
        return self.__clusters


    def get_noise(self):
        return self.__noise


    def __validate_arguments(self):
        if len(self.__data) == 0:
            raise ValueError("Empty input data. Data should contain at least one point.")

        if self.__amount_intervals <= 0:
            raise ValueError("Incorrect amount of intervals '%d'. Amount of intervals value should be greater than 0." % self.__amount_intervals)

        if self.__density_threshold < 0:
            raise ValueError("Incorrect density threshold '%f'. Density threshold should not be negative." % self.__density_threshold)