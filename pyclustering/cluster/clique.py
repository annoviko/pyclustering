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

from pyclustering.cluster import cluster_visualizer
from pyclustering.cluster.encoder import type_encoding

from pyclustering.core.wrapper import ccore_library

import pyclustering.core.clique_wrapper as wrapper


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
    """!
    @brief Visualizer of CLIQUE algorithm's results.
    @details CLIQUE visualizer provides visualization services that are specific for CLIQUE algorithm, for example,
              to display grid and its density.

    """

    __maximum_density_alpha = 0.6

    @staticmethod
    def show_grid(cells, data):
        """!
        @brief Show CLIQUE blocks as a grid in data space.
        @details Each block contains points and according to this density is displayed. CLIQUE grid helps to visualize
                  grid that was used for clustering process.

        @param[in] cells (list): List of cells that is produced by CLIQUE algorithm.
        @param[in] data (array_like): Input data that was used for clustering process.

        """
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
    def show_clusters(data, clusters, noise=None):
        """!
        @brief Display CLIQUE clustering results.

        @param[in] data (list): Data that was used for clustering.
        @param[in] clusters (array_like): Clusters that were allocated by the algorithm.
        @param[in] noise (array_like): Noise that were allocated by the algorithm.

        """
        visualizer = cluster_visualizer()
        visualizer.append_clusters(clusters, data)
        visualizer.append_cluster(noise or [], data, marker='x')
        visualizer.show()


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
    """!
    @brief CLIQUE block contains information about its logical location in grid, spatial location in data space and
            points that are covered by the block.

    """

    def __init__(self, logical_location=None, spatial_location=None, points=None, visited=False):
        """!
        @brief Initializes CLIQUE block.

        @param[in] logical_location (list): Logical location of the block in CLIQUE grid.
        @param[in] spatial_location (spatial_block): Spatial location in data space.
        @param[in] points (array_like): Points that belong to this block (can be obtained by method 'capture_points',
                    this parameter is used by CLIQUE in case of processing by C++ implementation when clustering
                    result are passed back to Python code.
        @param[in] visited (bool): Marks if block is visited during clustering process.

        """
        self.__logical_location = logical_location or []
        self.__spatial_location = spatial_location
        self.__points = points or []
        self.__visited = visited

    def __str__(self):
        """!
        @brief Returns string representation of the block using its logical location in CLIQUE grid.

        """
        return str(self.__logical_location)

    def __repr__(self):
        """!
        @brief Returns string representation of the block using its logical location in CLIQUE grid.

        """
        return str(self.__logical_location)

    @property
    def logical_location(self):
        """!
        @brief Logical location is represented by coordinates in CLIQUE grid, for example, in case of 2x2 grid blocks
                may have following coordinates: [0, 0], [0, 1], [1, 0], [1, 1].
        @return (list) Logical location of the block in CLIQUE grid.

        """
        return self.__logical_location

    @logical_location.setter
    def logical_location(self, location):
        """!
        @brief Assign logical location to CLIQUE block.

        @param[in] location (list): New logical location of the block in CLIQUE grid.

        """
        self.__logical_location = location

    @property
    def spatial_location(self):
        """!
        @brief Spatial location is represented by real data space coordinates.
        @return (spatial_block) Spatial block that describes location in data space.

        """
        return self.__spatial_location

    @spatial_location.setter
    def spatial_location(self, location):
        """!
        @brief Assign spatial location to CLIQUE block.

        @param[in] location (spatial_block): New spatial location of the block.

        """
        self.__spatial_location = location

    @property
    def dimensions(self):
        """!
        @brief Amount of dimensions where CLIQUE block is located.
        @return (uint) Amount of dimensions where CLIQUE block is located.

        """
        return len(self.__logical_location)

    @property
    def points(self):
        """!
        @brief Points that belong to the CLIQUE block.
        @details Points are represented by indexes that correspond to points in input data space.

        @return (array_like) Points that belong to the CLIQUE block.

        @see capture_points

        """
        return self.__points

    @property
    def visited(self):
        """!
        @brief Defines whether block is visited during cluster analysis.
        @details If cluster analysis has not been performed then value will False.

        @return (bool) True if block has been visited during processing, False otherwise.

        """
        return self.__visited

    @visited.setter
    def visited(self, visited):
        """!
        @brief Marks or unmarks block as a visited.
        @details This setter is used by CLIQUE algorithm.

        @param[in] visited (bool): New visited state for the CLIQUE block.

        """
        self.__visited = visited


    def capture_points(self, data, point_availability):
        """!
        @brief Finds points that belong to this block using availability map to reduce computational complexity by
                checking whether the point belongs to the block.
        @details Algorithm complexity of this method is O(n).

        @param[in] data (array_like): Data where points are represented as coordinates.
        @param[in] point_availability (array_like): Contains boolean values that denote whether point is already belong
                    to another CLIQUE block.

        """
        for index_point in range(len(data)):
            if (point_availability[index_point] is True) and (data[index_point] in self.__spatial_location):
                self.__points.append(index_point)
                point_availability[index_point] = False


    def get_location_neighbors(self, edge):
        """!
        @brief Forms list of logical location of each neighbor for this particular CLIQUE block.

        @param[in] edge (uint): Amount of intervals in each dimension that is used for clustering process.

        @return (list) Logical location of each neighbor for this particular CLIQUE block.

        """
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
    """!
    @brief Coordinate iterator is used to generate logical location description for each CLIQUE block.
    @details This class is used by CLIQUE algorithm for clustering process.

    """

    def __init__(self, dimension, intervals):
        """!
        @brief Initializes coordinate iterator for CLIQUE algorithm.

        @param[in] dimension (uint): Amount of dimensions in input data space.
        @param[in] intervals (uint): Amount of intervals in each dimension.

        """
        self.__intervals = intervals
        self.__dimension = dimension
        self.__coordiate = [0] * dimension


    def get_coordinate(self):
        """!
        @brief Returns current block coordinate.

        """
        return self.__coordiate


    def increment(self):
        """!
        @brief Forms logical location for next block.

        """
        for index_dimension in range(self.__dimension):
            if self.__coordiate[index_dimension] + 1 < self.__intervals:
                self.__coordiate[index_dimension] += 1
                return
            else:
                self.__coordiate[index_dimension] = 0

        self.__coordiate = None



class clique:
    """!
    @brief Class implements CLIQUE grid based clustering algorithm.
    @details CLIQUE automatically finnds subspaces with high-density clusters. It produces identical results
              irrespective of the order in which the input records are presented and it does not presume any canonical
              distribution for input data @cite article::clique::1.

    Here is an example where data in two-dimensional space is clustered using CLIQUE algorithm:
    @code
        from pyclustering.cluster.clique import clique, clique_visualizer
        from pyclustering.utils import read_sample
        from pyclustering.samples.definitions import FCPS_SAMPLES

        # read two-dimensional input data 'Target'
        data = read_sample(FCPS_SAMPLES.SAMPLE_TARGET)

        # create CLIQUE algorithm for processing
        intervals = 10  # defines amount of cells in grid in each dimension
        threshold = 0   # lets consider each point as non-outlier
        clique_instance = clique(data, intervals, threshold)

        # start clustering process and obtain results
        clique_instance.process()
        clusters = clique_instance.get_clusters()  # allocated clusters
        noise = clique_instance.get_noise()     # points that are considered as outliers (in this example should be empty)
        cells = clique_instance.get_cells()     # CLIQUE blocks that forms grid

        print("Amount of clusters:", len(clusters))

        # visualize clustering results
        clique_visualizer.show_grid(cells, data)    # show grid that has been formed by the algorithm
        clique_visualizer.show_clusters(data, clusters, noise)  # show clustering results
    @endcode

    In this example 6 clusters are allocated including four small cluster where each such small cluster consists of
    three points. There are visualized clustering results - grid that has been formed by CLIQUE algorithm with
    density and clusters itself:
    @image html clique_clustering_target.png "Fig. 1. CLIQUE clustering results (grid and clusters itself)."

    Sometimes such small clusters should be considered as outliers taking into account fact that two clusters in the
    central are relatively huge. To treat them as a noise threshold value should be increased:
    @code
        intervals = 10
        threshold = 3   # block that contains 3 or less points is considered as a outlier as well as its points
        clique_instance = clique(data, intervals, threshold)
    @endcode

    Two clusters are allocated, but in this case some points in cluster-"circle" are also considered as outliers,
    because CLIQUE operates with blocks, not with points:
    @image html clique_clustering_with_noise.png "Fig. 2. Noise allocation by CLIQUE."

    """

    def __init__(self, data, amount_intervals, density_threshold, **kwargs):
        """!
        @brief Create CLIQUE clustering algorithm.

        @param[in] data (list): Input data (list of points) that should be clustered.
        @param[in] amount_intervals (uint): Amount of intervals in each dimension that defines amount of CLIQUE block
                    as \f[N_{blocks} = intervals^{dimensions}\f].
        @param[in] density_threshold (uint): Minimum number of points that should contain CLIQUE block to consider its
                    points as non-outliers.
        @param[in] **kwargs: Arbitrary keyword arguments (available arguments: 'ccore').

        <b>Keyword Args:</b><br>
            - ccore (bool): By default is True. If True then C++ implementation is used for cluster analysis, otherwise
               Python implementation is used.

        """
        self.__data = data
        self.__amount_intervals = amount_intervals
        self.__density_threshold = density_threshold

        self.__ccore = kwargs.get('ccore', True)
        if self.__ccore:
            self.__ccore = ccore_library.workable()

        self.__clusters = []
        self.__noise = []

        self.__cells = []
        self.__cells_map = {}

        self.__validate_arguments()


    def process(self):
        """!
        @brief Performs clustering process in line with rules of CLIQUE clustering algorithm.

        @return (clique) Returns itself (CLIQUE instance).

        @see get_clusters()
        @see get_noise()
        @see get_cells()

        """

        if self.__ccore:
            self.__process_by_ccore()
        else:
            self.__process_by_python()

        return self


    def get_clusters(self):
        """!
        @brief Returns allocated clusters.

        @remark Allocated clusters are returned only after data processing (method process()). Otherwise empty list is returned.

        @return (list) List of allocated clusters, each cluster contains indexes of objects in list of data.

        @see process()
        @see get_noise()

        """
        return self.__clusters


    def get_noise(self):
        """!
        @brief Returns allocated noise.

        @remark Allocated noise is returned only after data processing (method process()). Otherwise empty list is returned.

        @return (list) List of indexes that are marked as a noise.

        @see process()
        @see get_clusters()

        """
        return self.__noise


    def get_cells(self):
        """!
        @brief Returns CLIQUE blocks that are formed during clustering process.
        @details CLIQUE blocks can be used for visualization purposes. Each CLIQUE block contain its logical location
                  in grid, spatial location in data space and points that belong to block.

        @return (list) List of CLIQUE blocks.

        """
        return self.__cells


    def get_cluster_encoding(self):
        """!
        @brief Returns clustering result representation type that indicate how clusters are encoded.

        @return (type_encoding) Clustering result representation.

        @see get_clusters()

        """

        return type_encoding.CLUSTER_INDEX_LIST_SEPARATION


    def __process_by_ccore(self):
        """!
        @brief Performs cluster analysis using C++ implementation of CLIQUE algorithm that is used by default if
                user's target platform is supported.

        """
        (self.__clusters, self.__noise, block_logical_locations, block_max_corners, block_min_corners, block_points) = \
            wrapper.clique(self.__data, self.__amount_intervals, self.__density_threshold)

        amount_cells = len(block_logical_locations)
        for i in range(amount_cells):
            self.__cells.append(clique_block(block_logical_locations[i],
                                             spatial_block(block_max_corners[i], block_min_corners[i]),
                                             block_points[i],
                                             True))


    def __process_by_python(self):
        """!
        @brief Performs cluster analysis using Python implementation of CLIQUE algorithm.

        """
        self.__create_grid()
        self.__allocate_clusters()

        self.__cells_map.clear()


    def __validate_arguments(self):
        """!
        @brief Check input arguments of CLIQUE algorithm and if one of them is not correct then appropriate exception
                is thrown.

        """

        if len(self.__data) == 0:
            raise ValueError("Empty input data. Data should contain at least one point.")

        if self.__amount_intervals <= 0:
            raise ValueError("Incorrect amount of intervals '%d'. Amount of intervals value should be greater than 0." % self.__amount_intervals)

        if self.__density_threshold < 0:
            raise ValueError("Incorrect density threshold '%f'. Density threshold should not be negative." % self.__density_threshold)


    def __allocate_clusters(self):
        """!
        @brief Performs cluster analysis using formed CLIQUE blocks.

        """
        for cell in self.__cells:
            if cell.visited is False:
                self.__expand_cluster(cell)


    def __expand_cluster(self, cell):
        """!
        @brief Tries to expand cluster from specified cell.
        @details During expanding points are marked as noise or append to new cluster.

        @param[in] cell (clique_block): CLIQUE block from that cluster should be expanded.

        """
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
        """!
        @brief Returns neighbors for specified CLIQUE block as clique_block objects.

        @return (list) Neighbors as clique_block objects.

        """
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
        """!
        @brief Creates CLIQUE grid that consists of CLIQUE blocks for clustering process.

        """
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
        """!
        @brief Forms key using logical location of a CLIQUE block.

        @return (string) Key for CLIQUE block map.

        """
        return ''.join(str(e) + '.' for e in location)


    def __get_spatial_location(self, logical_location, min_corner, max_corner, cell_sizes):
        """!
        @brief Calculates spatial location for CLIQUE block with logical coordinates defined by logical_location.

        @param[in] logical_location (list): Logical location of CLIQUE block for that spatial location should be calculated.
        @param[in] min_corner (list): Minimum corner of an input data.
        @param[in] max_corner (list): Maximum corner of an input data.
        @param[in] cell_sizes (list): Size of CLIQUE block in each dimension.

        @return (list, list): Maximum and minimum corners for the specified CLIQUE block.

        """
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
        """!
        @brief Calculates input data description that is required to create CLIQUE grid.

        @return (list, list, list): Data size in each dimension, minimum and maximum corners.

        """
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
