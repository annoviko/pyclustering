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
    """!
    @brief Geometrical description of CLIQUE block in data space.
    @details Provides services related to spatial functionality.

    @see bang_block

    """

    def __init__(self, max_corner, min_corner):
        """!
        @brief Creates spatial block in data space.

        @param[in] max_corner (array_like): Maximum corner coordinates of the block.
        @param[in] min_corner (array_like): Minimal corner coordinates of the block.

        """
        self.__max_corner = max_corner
        self.__min_corner = min_corner


    def __str__(self):
        """!
        @brief Returns string block description.

        @return String representation of the block.

        """
        return "(max: %s; min: %s)" % (self.__max_corner, self.__min_corner)


    def __contains__(self, point):
        """!
        @brief Point is considered as contained if it lies in block (belong to it).

        @return (bool) True if point is in block, otherwise False.

        """
        for i in range(len(point)):
            if point[i] < self.__min_corner[i] or point[i] > self.__max_corner[i]:
                return False

        return True


    def get_corners(self):
        """!
        @brief Return spatial description of current block.

        @return (tuple) Pair of maximum and minimum corners (max_corner, min_corner).

        """
        return self.__max_corner, self.__min_corner


    def is_neighbor(self, block):
        """!
        @brief Performs calculation to identify whether specified block is neighbor of current block.

        @param[in] block (spatial_block): Another block that is check whether it is neighbor.

        @return (bool) True is blocks are neighbors, False otherwise.

        """
        if block is not self:
            block_max_corner, _ = block.get_corners()
            dimension = len(block_max_corner)
            neighborhood_score = self.__calculate_neighborhood(block_max_corner)

            if neighborhood_score == dimension:
                return True

        return False


    def __calculate_neighborhood(self, block_max_corner):
        """!
        @brief Calculates neighborhood score that defined whether blocks are neighbors.

        @param[in] block_max_corner (list): Maximum coordinates of other block.

        @return (uint) Neighborhood score.

        """
        dimension = len(block_max_corner)

        length_edges = [self.__max_corner[i] - self.__min_corner[i] for i in range(dimension)]

        neighborhood_score = 0
        for i in range(dimension):
            diff = abs(block_max_corner[i] - self.__max_corner[i])

            if diff <= length_edges[i] + length_edges[i] * 0.0001:
                neighborhood_score += 1

        return neighborhood_score



class clique_block:
    def __init__(self):
        self.__logical_location = []
        self.__spatial_location = None
        self.__points = []

    @property
    def logical_location(self):
        return self.__logical_location

    @logical_location.setter
    def logical_location(self, location):
        self.__logical_location = location

    @property
    def spatial_location(self):
        return self.__spatial_location

    @spatial_location.setter
    def spatial_location(self, location):
        self.__spatial_location = location

    @property
    def points(self):
        return self.__points

    def capture_points(self, data, point_availability):
        for index_point in range(len(data)):
            if (point_availability[index_point] is True) and (data[index_point] in self.__spatial_location):
                self.__points.append(index_point)
                point_availability[index_point] = False


    def is_neighbor(self, block):
        for index_dimension in range(len(self.__logical_location)):
            if not self.__is_dimension_neighbor(self.__logical_location[index_dimension], block.logical_location[index_dimension]):
                return False

        return True


    def get_neighbors(self):
        pass


    def __is_dimension_neighbor(self, location1, location2):
        return location1 + 1 == location2 or location1 - 1 == location2



class coordinate_iterator:
    def __init__(self, dimension, intervals):
        self.__intervals = intervals
        self.__dimension = dimension
        self.__coordiate = [0] * dimension


    def get_coordinate(self):
        return self.__coordiate


    def increment(self):
        for index_dimension in range(self.__dimension):
            if self.__coordiate[index_dimension] + 1 < self.__intervals:
                self.__coordiate[index_dimension] += 1
                return
            else:
                self.__coordiate[index_dimension] = 0

        self.__coordiate = None



class clique:
    def __init__(self, data, amount_intervals, density_threshold):
        self.__data = data
        self.__amount_intervals = amount_intervals
        self.__density_threshold = density_threshold

        self.__clusters = []
        self.__noise = []

        self.__validate_arguments()


    def process(self):
        cells = self.__create_grid()
        self.__allocate_clusters(cells)


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


    def __allocate_clusters(self, cells):
        belong = [False] * len(cells)

        for index_cell in range(len(cells)):
            if (belong[index_cell] is False) and (len(cells[index_cell].points) > self.__density_threshold):
                belong[index_cell] = True
                self.__expand_cluster(cells[index_cell], belong)    # traverse from this cell to expand cluster


    def __expand_cluster(self, cell, belong):
        cluster = cell.points[:]
        neighbors = cell.get_neighbors()

        for cell_neighbor in neighbors:
            if len(cell_neighbor.points) > self.__density_threshold:
                cluster.extend(cell_neighbor.points)
                # mark that cell belongs to cluster


    def __create_grid(self):
        data_sizes, min_corner, max_corner = self.__get_data_size_derscription()
        dimension = len(self.__data[0])

        cell_sizes = [dimension_length / self.__amount_intervals for dimension_length in data_sizes]

        cells = [clique_block() for _ in range(pow(self.__amount_intervals, dimension))]
        iterator = coordinate_iterator(dimension, self.__amount_intervals)

        point_availability = [True] * len(self.__data)
        for index_cell in range(len(cells)):
            logical_location = iterator.get_coordinate()
            cells[index_cell].logical_location = logical_location[:]

            cur_max_corner, cur_min_corner = self.__get_spatial_location(logical_location, min_corner, cell_sizes)
            cells[index_cell].spatial_location = spatial_block(cur_max_corner, cur_min_corner)

            cells[index_cell].capture_points(self.__data, point_availability)

        return cells


    def __get_spatial_location(self, logical_location, min_corner, cell_sizes):
        cur_min_corner = min_corner[:]
        cur_max_corner = min_corner[:]
        for index_dimension in range(len(self.__data[0])):
            cur_min_corner[index_dimension] += cell_sizes[index_dimension] * logical_location[index_dimension]
            cur_max_corner[index_dimension] += cell_sizes[index_dimension]

        return cur_max_corner, cur_min_corner


    def __get_data_size_derscription(self):
        min_corner = self.__data[0][:]
        max_corner = self.__data[0][:]

        dimension = len(self.__data[0])

        for index_point in range(1, len(self.__data)):
            for index_dimension in range(dimension):
                coordinate = self.__data[index_point][index_dimension]
                if coordinate > max_corner[index_dimension]:
                    max_corner[index_dimension] = coordinate

                if coordinate < min_corner[index_dimension]:
                    min_corner[index_dimension] = coordinate

        data_sizes = [0.0] * dimension
        for index_dimension in range(dimension):
            data_sizes[index_dimension] = max_corner[index_dimension] - min_corner[index_dimension]

        return data_sizes, min_corner, max_corner
