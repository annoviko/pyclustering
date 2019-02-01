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


import itertools

from collections import deque


try:
    import matplotlib
    import matplotlib.gridspec as gridspec
    import matplotlib.pyplot as plt
    import matplotlib.patches as patches
    import matplotlib.animation as animation
except Exception as error_instance:
    import warnings
    warnings.warn("Impossible to import matplotlib (please, install 'matplotlib'), pyclustering's visualization "
                  "functionality is not available (details: '%s')." % str(error_instance))


class clique_visualizer:
    __maximum_density_alpha = 0.6

    @staticmethod
    def show_grid(cells, data):
        dimension = cells[0].dimensions

        amount_canvases = 1
        if dimension > 1:
            amount_canvases = int(dimension * (dimension - 1) / 2)

        figure = plt.figure()
        grid_spec = gridspec.GridSpec(1, amount_canvases)

        pairs = list(itertools.combinations(range(dimension), 2))
        if len(pairs) == 0: pairs = [(0, 0)]

        for index in range(amount_canvases):
            ax = figure.add_subplot(grid_spec[index])
            clique_visualizer.__draw_cells(ax, cells, pairs[index])
            clique_visualizer.__draw_two_dimension_data(ax, data, pairs[index])

        plt.show()


    @staticmethod
    def __draw_two_dimension_data(ax, data, pair):
        """!
        @brief Display data in two-dimensional canvas.

        @param[in] ax (Axis): Canvas where data should be displayed.
        @param[in] data (list): Data points that should be displayed.
        @param[in] pair (tuple): Pair of dimension indexes.

        """
        ax.set_xlabel("x%d" % pair[0])
        ax.set_ylabel("x%d" % pair[1])

        for point in data:
            if len(data[0]) > 1:
                ax.plot(point[pair[0]], point[pair[1]], color='red', marker='.')
            else:
                ax.plot(point[pair[0]], 0, color='red', marker='.')
                ax.yaxis.set_ticklabels([])


    @staticmethod
    def __draw_cells(ax, cells, pair):
        ax.grid(False)

        density_scale = max(len(cell.points) for cell in cells)
        for cell in cells:
            clique_visualizer.__draw_cell(ax, pair, cell, density_scale)


    @staticmethod
    def __draw_cell(ax, pair, cell, density_scale):
        max_corner, min_corner = clique_visualizer.__get_rectangle_description(cell, pair)

        belong_cluster = (len(cell.points) > 0)

        if density_scale != 0.0:
            density_scale = clique_visualizer.__maximum_density_alpha * len(cell.points) / density_scale

        face_color = matplotlib.colors.to_rgba('blue', alpha=density_scale)
        edge_color = matplotlib.colors.to_rgba('black', alpha=1.0)

        rect = patches.Rectangle(min_corner, max_corner[0] - min_corner[0], max_corner[1] - min_corner[1],
                                 fill=belong_cluster,
                                 facecolor=face_color,
                                 edgecolor=edge_color,
                                 linewidth=0.5)
        ax.add_patch(rect)
        #ax.annotate(str(cell.logical_location), (min_corner[0], min_corner[1]), fontsize=6, ha='center', va='center')


    @staticmethod
    def __get_rectangle_description(cell, pair):
        max_corner, min_corner = cell.spatial_location.get_corners()

        max_corner = [max_corner[pair[0]], max_corner[pair[1]]]
        min_corner = [min_corner[pair[0]], min_corner[pair[1]]]

        if pair == (0, 0):
            max_corner[1], min_corner[1] = 1.0, -1.0

        return max_corner, min_corner



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
        self.__visited = False

    def __str__(self):
        return str(self.__logical_location)

    def __repr__(self):
        return str(self.__logical_location)

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
    def dimensions(self):
        return len(self.__logical_location)

    @property
    def points(self):
        return self.__points

    @property
    def visited(self):
        return self.__visited

    @visited.setter
    def visited(self, visited):
        self.__visited = visited


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
    def __init__(self, data, amount_intervals, density_threshold, **kwargs):
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
        return self


    def get_clusters(self):
        return self.__clusters


    def get_noise(self):
        return self.__noise


    def get_cells(self):
        return self.__cells


    def __validate_arguments(self):
        if len(self.__data) == 0:
            raise ValueError("Empty input data. Data should contain at least one point.")

        if self.__amount_intervals <= 0:
            raise ValueError("Incorrect amount of intervals '%d'. Amount of intervals value should be greater than 0." % self.__amount_intervals)

        if self.__density_threshold < 0:
            raise ValueError("Incorrect density threshold '%f'. Density threshold should not be negative." % self.__density_threshold)


    def __allocate_clusters(self):
        for cell in self.__cells:
            if cell.visited is False:
                self.__expand_cluster(cell)


    def __expand_cluster(self, cell):
        cell.visited = True

        if len(cell.points) <= self.__density_threshold:
            if len(cell.points) > 0:
                self.__noise.extend(cell.points)

            return

        cluster = cell.points[:]
        neighbors = self.__get_neighbors(cell)

        for neighbor in neighbors:
            if len(neighbor.points) > self.__density_threshold:
                cluster.extend(neighbor.points)
                neighbors += self.__get_neighbors(neighbor)

            elif len(neighbor.points) > 0:
                self.__noise.extend(neighbor.points)

        self.__clusters.append(cluster)


    def __get_neighbors(self, cell):
        neighbors = []
        location_neighbors = cell.get_location_neighbors(self.__amount_intervals)

        for i in range(len(location_neighbors)):
            key = self.__location_to_key(location_neighbors[i])
            candidate_neighbor = self.__cell_map[key]

            if not candidate_neighbor.visited:
                candidate_neighbor.visited = True
                neighbors.append(candidate_neighbor)

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
        return ''.join(str(e) + '.' for e in location)


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
