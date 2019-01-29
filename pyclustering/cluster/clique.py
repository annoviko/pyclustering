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



class clique_block:
    def __init__(self):
        self.__logical_location = []
        self.__spatial_location = None
        self.__points = []
        self.__belong = False

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

    @property
    def belong(self):
        return self.__belong

    @belong.setter
    def belong(self, value):
        self.__belong = value


    def capture_points(self, data, point_availability):
        for index_point in range(len(data)):
            if (point_availability[index_point] is True) and (data[index_point] in self.__spatial_location):
                self.__points.append(index_point)
                point_availability[index_point] = False


    def get_location_neighbors(self, edge):
        neighbors = []

        for index_dimension in range(len(self.__logical_location)):
            if self.__logical_location[index_dimension] + 1 < edge:
                position = self.__logical_location[:]
                position[index_dimension] += 1
                neighbors.append(position)

            if self.__logical_location[index_dimension] - 1 >= 0:
                position = self.__logical_location[:]
                position[index_dimension] -= 1
                neighbors.append(position)

        return neighbors



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

        self.__cells = []
        self.__cells_map = {}

        self.__validate_arguments()


    def process(self):
        self.__create_grid()
        self.__allocate_clusters()

        self.__cells_map.clear()


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


    def __allocate_clusters(self):
        for cell in self.__cells:
            if cell.belong is False:
                cell.belong = True
                if len(cell.points) > self.__density_threshold:
                    self.__expand_cluster(cell)    # traverse from this cell to expand cluster
                elif len(cell.points) > 0:
                    self.__noise.extend(cell.points)


    def __expand_cluster(self, cell):
        cluster = cell.points[:]

        neighbors = []
        traversed = set()
        self.__fill_by_free_neighbors(cell, neighbors, traversed)

        for cell_neighbor in neighbors:
            cell_neighbor.belong = True

            if len(cell_neighbor.points) > self.__density_threshold:
                cluster.extend(cell_neighbor.points)
                self.__fill_by_free_neighbors(cell_neighbor, neighbors, traversed)
            elif len(cell_neighbor.points) > 0:
                self.__noise.extend(cell.points)

        self.__clusters.append(cluster)


    def __fill_by_free_neighbors(self, cell, neighbors, traversed):
        location_neighbors = cell.get_location_neighbors(self.__amount_intervals)

        for location in location_neighbors:
            key = self.__location_to_key(location)

            if key not in traversed:
                traversed.add(key)
                neighbor = self.__cell_map[key]
                if neighbor.belong is False:
                    neighbors.append(self.__cell_map[key])

        return neighbors


    def __create_grid(self):
        data_sizes, min_corner, max_corner = self.__get_data_size_derscription()
        dimension = len(self.__data[0])

        cell_sizes = [dimension_length / self.__amount_intervals for dimension_length in data_sizes]

        self.__cells = [clique_block() for _ in range(pow(self.__amount_intervals, dimension))]
        iterator = coordinate_iterator(dimension, self.__amount_intervals)

        point_availability = [True] * len(self.__data)
        self.__cell_map = {}
        for index_cell in range(len(self.__cells)):
            logical_location = iterator.get_coordinate()
            iterator.increment()

            self.__cells[index_cell].logical_location = logical_location[:]

            cur_max_corner, cur_min_corner = self.__get_spatial_location(logical_location, min_corner, max_corner, cell_sizes)
            self.__cells[index_cell].spatial_location = spatial_block(cur_max_corner, cur_min_corner)

            self.__cells[index_cell].capture_points(self.__data, point_availability)

            self.__cell_map[self.__location_to_key(logical_location)] = self.__cells[index_cell]


    def __location_to_key(self, location):
        return ''.join(str(e) for e in location)


    def __get_spatial_location(self, logical_location, min_corner, max_corner, cell_sizes):
        cur_min_corner = min_corner[:]
        cur_max_corner = min_corner[:]
        dimension = len(self.__data[0])
        for index_dimension in range(dimension):
            cur_min_corner[index_dimension] += cell_sizes[index_dimension] * logical_location[index_dimension]

            if logical_location[index_dimension] == self.__amount_intervals - 1:
                cur_max_corner[index_dimension] = max_corner[index_dimension]
            else:
                cur_max_corner[index_dimension] = cur_min_corner[index_dimension] + cell_sizes[index_dimension]

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



# block1 = clique_block()
# block1.logical_location = [1, 1]
# block2 = clique_block()
# block2.logical_location = [0, 1]
#
# print(block1.get_locaion_neighbors(3))
