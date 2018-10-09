"""!

@brief Elbow method to determine the optimal number of clusters for k-means clustering.
@details Implementation based on paper @cite ???.

@authors Andrei Novikov (pyclustering@yandex.ru)
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


from pyclustering.cluster.kmeans import kmeans
from pyclustering.cluster.center_initializer import kmeans_plusplus_initializer


class elbow:
    def __init__(self, data, kmin, kmax, **kwargs):
        if kmax - kmin < 3:
            raise ValueError("Amount of K (" + str(kmax - kmin) + ") is too small for analysis. "
                             "It is require to have at least three K to build elbow.")

        self.__initializer = kwargs.get('initializer', kmeans_plusplus_initializer)

        self.__data = data
        self.__kmin = kmin
        self.__kmax = kmax

        self.__sse = []
        self.__elbows = []
        self.__kvalue = -1


    def process(self):
        for amount in range(self.__kmin, self.__kmax):
            centers = self.__initializer(self.__data, amount).initialize()
            instance = kmeans(self.__data, centers)
            self.__sse.append(instance.get_sum_metric_error())

        self.__calculate_elbows()
        self.__find_optimal_kvalue()

        return self


    def get_amount(self):
        return self.__kvalue


    def get_sse(self):
        return self.__sse


    def __calculate_elbows(self):
        for index_elbow in range(1, len(self.__sse) - 1):
            elbow = self.__sse[index_elbow - 1] + self.__sse[index_elbow + 1]
            self.__elbows.append(elbow)


    def __find_optimal_kvalue(self):
        optimal_elbow_value = max(self.__elbows)
        self.__kvalue = self.__elbows.index(optimal_elbow_value) + 1