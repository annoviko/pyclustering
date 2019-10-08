"""!

@brief Cluster analysis algorithm: BANG.
@details Implementation based on paper @cite inproceedings::bang::1.

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
import warnings

try:
    import matplotlib
    import matplotlib.gridspec as gridspec
    import matplotlib.pyplot as plt
    import matplotlib.patches as patches
    import matplotlib.animation as animation
except Exception as error_instance:
    warnings.warn("Impossible to import matplotlib (please, install 'matplotlib'), pyclustering's visualization "
                  "functionality is not available (details: '%s')." % str(error_instance))

from pyclustering.cluster import cluster_visualizer
from pyclustering.cluster.encoder import type_encoding

from pyclustering.utils import data_corners
from pyclustering.utils.color import color as color_list



class bang_visualizer:
    """!
    @brief Visualizer of BANG algorithm's results.
    @details BANG visualizer provides visualization services that are specific for BANG algorithm.

    """

    __maximum_density_alpha = 0.6


    @staticmethod
    def show_blocks(directory):
        """!
        @brief Show BANG-blocks (leafs only) in data space.
        @details BANG-blocks represents grid that was used for clustering process.

        @param[in] directory (bang_directory): Directory that was created by BANG algorithm during clustering process.

        """

        dimension = len(directory.get_data()[0])

        amount_canvases = 1
        if dimension > 1:
            amount_canvases = int(dimension * (dimension - 1) / 2)

        figure = plt.figure()
        grid_spec = gridspec.GridSpec(1, amount_canvases)

        pairs = list(itertools.combinations(range(dimension), 2))
        if len(pairs) == 0: pairs = [(0, 0)]

        for index in range(amount_canvases):
            ax = figure.add_subplot(grid_spec[index])
            bang_visualizer.__draw_blocks(ax, directory.get_leafs(), pairs[index])
            bang_visualizer.__draw_two_dimension_data(ax, directory.get_data(), pairs[index])

        plt.show()


    @staticmethod
    def show_dendrogram(dendrogram):
        """!
        @brief Display dendrogram of BANG-blocks.

        @param[in] dendrogram (list): List representation of dendrogram of BANG-blocks.

        @see bang.get_dendrogram()

        """
        plt.figure()
        axis = plt.subplot(1, 1, 1)

        current_position = 0
        for index_cluster in range(len(dendrogram)):
            densities = [ block.get_density() for block in dendrogram[index_cluster] ]
            xrange = range(current_position, current_position + len(densities))

            axis.bar(xrange, densities, 1.0, linewidth=0.0, color=color_list.get_color(index_cluster))

            current_position += len(densities)

        axis.set_ylabel("density")
        axis.set_xlabel("block")
        axis.xaxis.set_ticklabels([])

        plt.xlim([-0.5, current_position - 0.5])
        plt.show()


    @staticmethod
    def show_clusters(data, clusters, noise=None):
        """!
        @brief Display BANG clustering results.

        @param[in] data (list): Dataset that was used for clustering.
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
    def __draw_blocks(ax, blocks, pair):
        """!
        @brief Display BANG-blocks on specified figure.

        @param[in] ax (Axis): Axis where bang-blocks should be displayed.
        @param[in] blocks (list): List of blocks that should be displyed.
        @param[in] pair (tuple): Pair of coordinate index that should be displayed.

        """
        ax.grid(False)

        density_scale = blocks[-1].get_density()
        for block in blocks:
            bang_visualizer.__draw_block(ax, pair, block, density_scale)


    @staticmethod
    def __draw_block(ax, pair, block, density_scale):
        """!
        @brief Display BANG-block on the specified ax.

        @param[in] ax (Axis): Axis where block should be displayed.
        @param[in] pair (tuple): Pair of coordinate index that should be displayed.
        @param[in] block (bang_block): BANG-block that should be displayed.
        @param[in] density_scale (double): Max density to display density of the block by appropriate tone.

        """
        max_corner, min_corner = bang_visualizer.__get_rectangle_description(block, pair)

        belong_cluster = block.get_cluster() is not None

        if density_scale != 0.0:
            density_scale = bang_visualizer.__maximum_density_alpha * block.get_density() / density_scale

        face_color = matplotlib.colors.to_rgba('blue', alpha=density_scale)
        edge_color = matplotlib.colors.to_rgba('black', alpha=1.0)

        rect = patches.Rectangle(min_corner, max_corner[0] - min_corner[0], max_corner[1] - min_corner[1],
                                 fill=belong_cluster,
                                 facecolor=face_color,
                                 edgecolor=edge_color,
                                 linewidth=0.5)
        ax.add_patch(rect)


    @staticmethod
    def __get_rectangle_description(block, pair):
        """!
        @brief Create rectangle description for block in specific dimension.

        @param[in] pair (tuple): Pair of coordinate index that should be displayed.
        @param[in] block (bang_block): BANG-block that should be displayed

        @return (tuple) Pair of corners that describes rectangle.

        """
        max_corner, min_corner = block.get_spatial_block().get_corners()

        max_corner = [max_corner[pair[0]], max_corner[pair[1]]]
        min_corner = [min_corner[pair[0]], min_corner[pair[1]]]

        if pair == (0, 0):
            max_corner[1], min_corner[1] = 1.0, -1.0

        return max_corner, min_corner


class bang_animator:
    """!
    @brief Provides service for creating 2-D animation using BANG clustering results.
    @details The animator does not support visualization of clustering process where non 2-dimensional was used.

    Code example of animation of BANG clustering process:
    @code
        from pyclustering.cluster.bang import bang, bang_animator
        from pyclustering.utils import read_sample
        from pyclustering.samples.definitions import FCPS_SAMPLES

        # Read data two dimensional data.
        data = read_sample(FCPS_SAMPLES.SAMPLE_LSUN)

        # Create instance of BANG algorithm.
        bang_instance = bang(data, 9)
        bang_instance.process()

        # Obtain clustering results.
        clusters = bang_instance.get_clusters()
        noise = bang_instance.get_noise()
        directory = bang_instance.get_directory()

        # Create BANG animation using class 'bang_animator':
        animator = bang_animator(directory, clusters)
        animator.animate()
    @endcode


    """
    def __init__(self, directory, clusters):
        """!
        @brief Creates BANG animator instance.

        @param[in] directory (bang_directory): BANG directory that was formed during BANG clustering process.
        @param[in] clusters (list): Allocated clusters during BANG clustering process.

        """
        self.__directory = directory
        self.__clusters = clusters
        self.__noise = []

        self.__current_block = 0
        self.__current_level = 0
        self.__level_blocks = directory.get_level(0)

        self.__figure = plt.figure()
        self.__ax = self.__figure.add_subplot(1, 1, 1)
        self.__special_frame = 0

        self.__validate_arguments()


    def __validate_arguments(self):
        """!
        @brief Check correctness of input arguments and throw exception if incorrect is found.

        """
        if len(self.__directory.get_data()[0]) != 2:
            raise ValueError("Impossible to animate BANG clustering process for non 2D data.")


    def __increment_block(self):
        """!
        @brief Increment BANG block safely by updating block index, level and level block.

        """
        self.__current_block += 1
        if self.__current_block >= len(self.__level_blocks):
            self.__current_block = 0
            self.__current_level += 1

            if self.__current_level < self.__directory.get_height():
                self.__level_blocks = self.__directory.get_level(self.__current_level)


    def __draw_block(self, block, block_alpha=0.0):
        """!
        @brief Display single BANG block on axis.

        @param[in] block (bang_block): BANG block that should be displayed.
        @param[in] block_alpha (double): Transparency level - value of alpha.

        """
        max_corner, min_corner = block.get_spatial_block().get_corners()

        face_color = matplotlib.colors.to_rgba('blue', alpha=block_alpha)
        edge_color = matplotlib.colors.to_rgba('black', alpha=1.0)

        rect = patches.Rectangle(min_corner, max_corner[0] - min_corner[0], max_corner[1] - min_corner[1],
                                 fill=True,
                                 facecolor=face_color,
                                 edgecolor=edge_color,
                                 linewidth=0.5)
        self.__ax.add_patch(rect)


    def __draw_leaf_density(self):
        """!
        @brief Display densities by filling blocks by appropriate colors.

        """
        leafs = self.__directory.get_leafs()
        density_scale = leafs[-1].get_density()

        if density_scale == 0.0: density_scale = 1.0

        for block in leafs:
            alpha = 0.8 * block.get_density() / density_scale
            self.__draw_block(block, alpha)


    def __draw_clusters(self):
        """!
        @brief Display clusters and outliers using different colors.

        """
        data = self.__directory.get_data()
        for index_cluster in range(len(self.__clusters)):
            color = color_list.get_color(index_cluster)
            self.__draw_cluster(data, self.__clusters[index_cluster], color, '.')

        self.__draw_cluster(self.__directory.get_data(), self.__noise, 'gray', 'x')


    def __draw_cluster(self, data, cluster, color, marker):
        """!
        @brief Draw 2-D single cluster on axis using specified color and marker.

        """
        for item in cluster:
            self.__ax.plot(data[item][0], data[item][1], color=color, marker=marker)


    def animate(self, animation_velocity=75, movie_fps=25, movie_filename=None):
        """!
        @brief Animates clustering process that is performed by BANG algorithm.

        @param[in] animation_velocity (uint): Interval between frames in milliseconds (for run-time animation only).
        @param[in] movie_fps (uint): Defines frames per second (for rendering movie only).
        @param[in] movie_filename (string): If it is specified then animation will be stored to file that is specified in this parameter.

        """
        def init_frame():
            self.__figure.clf()
            self.__ax = self.__figure.add_subplot(1, 1, 1)
            self.__figure.suptitle("BANG algorithm", fontsize=18, fontweight='bold')

            for point in self.__directory.get_data():
                self.__ax.plot(point[0], point[1], color='red', marker='.')

            return frame_generation(0)


        def frame_generation(index_iteration):
            if self.__current_level < self.__directory.get_height():
                block = self.__level_blocks[self.__current_block]
                self.__draw_block(block)
                self.__increment_block()

            else:
                if self.__special_frame == 0:
                    self.__draw_leaf_density()

                elif self.__special_frame == 15:
                    self.__draw_clusters()

                elif self.__special_frame == 30:
                    self.__figure.clf()
                    self.__ax = self.__figure.add_subplot(1, 1, 1)
                    self.__figure.suptitle("BANG algorithm", fontsize=18, fontweight='bold')

                    self.__draw_clusters()

                self.__special_frame += 1



        iterations = len(self.__directory) + 60
        # print("Total number of iterations: %d" % iterations)
        cluster_animation = animation.FuncAnimation(self.__figure, frame_generation, iterations,
                                                    interval=animation_velocity,
                                                    init_func=init_frame,
                                                    repeat_delay=5000)

        if movie_filename is not None:
            cluster_animation.save(movie_filename, writer = 'ffmpeg', fps = movie_fps, bitrate = 3500)
        else:
            plt.show()



class bang_directory:
    """!
    @brief BANG directory stores BANG-blocks that represents grid in data space.
    @details The directory build BANG-blocks in binary tree manner. Leafs of the tree stored separately to provide
              a direct access to the leafs that should be analysed. Leafs cache data-points.

    """
    def __init__(self, data, levels, **kwargs):
        """!
        @brief Create BANG directory - basically tree structure with direct access to leafs.

        @param[in] data (list): Input data that is clustered.
        @param[in] levels (uint): Height of the tree of blocks.
        @param[in] **kwargs: Arbitrary keyword arguments (available arguments: 'observe').

        <b>Keyword Args:</b><br>
            - observe (bool): If 'True' then blocks on each level are stored.
            - density_threshold (double): The lowest level of density when contained data in bang-block is
               considered as a noise and there is no need to split it till the last level. Be aware that this
               parameter is used with 'amount_threshold' parameter.
            - amount_threshold (uint): Amount of points in the block when it contained data in bang-block is
               considered as a noise and there is no need to split it till the last level.

        """
        self.__data = data
        self.__levels = levels
        self.__density_threshold = kwargs.get('density_threshold', 0.0)
        self.__amount_density = kwargs.get('amount_threshold', 0)
        self.__leafs = []
        self.__root = None
        self.__level_blocks = []
        self.__size = 0
        self.__observe = kwargs.get('observe', True)

        self.__create_directory()


    def __len__(self):
        """!
        @brief Returns amount of blocks that is stored in the directory

        @return (uint) Amount of blocks in the BANG directory.

        """
        return self.__size


    def get_data(self):
        """!
        @brief Return data that is stored in the directory.

        @return (list) List of points that represents stored data.

        """
        return self.__data


    def get_leafs(self):
        """!
        @brief Return leafs - the smallest blocks.
        @details Some leafs can be bigger than others because splitting is not performed for blocks whose density is
                  less than threshold.

        @return (list) List of blocks that are leafs of BANG directory.

        """
        return self.__leafs


    def get_level(self, level):
        """!
        @brief Returns BANG blocks on the specific level.

        @param[in] level (uint): Level of tree where BANG blocks are located.

        @return (list) List of BANG blocks on the specific level.

        """
        return self.__level_blocks[level]


    def get_height(self):
        """!
        @brief Returns height of BANG tree where blocks are stored.

        @return (uint) Height of BANG tree.

        """
        return len(self.__level_blocks)


    def __create_directory(self):
        """!
        @brief Create BANG directory as a tree with separate storage for leafs.

        """

        min_corner, max_corner = data_corners(self.__data)
        data_block = spatial_block(max_corner, min_corner)

        cache_require = (self.__levels == 1)
        self.__root = bang_block(self.__data, 0, 0, data_block, cache_require)

        if cache_require:
            self.__leafs.append(self.__root)
            self.__store_level_blocks([self.__root])
        else:
            self.__build_directory_levels()


    def __store_level_blocks(self, level_blocks):
        """!
        @brief Store level blocks if observing is enabled.

        @param[in] level_blocks (list): Created blocks on a new level.

        """
        self.__size += len(level_blocks)
        if self.__observe is True:
            self.__level_blocks.append(level_blocks)



    def __build_directory_levels(self):
        """!
        @brief Build levels of direction if amount of level is greater than one.

        """

        previous_level_blocks = [ self.__root ]

        for level in range(1, self.__levels):
            previous_level_blocks = self.__build_level(previous_level_blocks, level)
            self.__store_level_blocks(previous_level_blocks)

        self.__leafs = sorted(self.__leafs, key=lambda block: block.get_density())


    def __build_level(self, previous_level_blocks, level):
        """!
        @brief Build new level of directory.

        @param[in] previous_level_blocks (list): BANG-blocks on the previous level.
        @param[in] level (uint): Level number that should be built.

        @return (list) New block on the specified level.

        """
        current_level_blocks = []

        split_dimension = level % len(self.__data[0])
        cache_require = (level == self.__levels - 1)

        for block in previous_level_blocks:
            self.__split_block(block, split_dimension, cache_require, current_level_blocks)

        if cache_require:
            self.__leafs += current_level_blocks

        return current_level_blocks


    def __split_block(self, block, split_dimension, cache_require, current_level_blocks):
        """!
        @brief Split specific block in specified dimension.
        @details Split is not performed for block whose density is lower than threshold value, such blocks are putted to
                  leafs.

        @param[in] block (bang_block): BANG-block that should be split.
        @param[in] split_dimension (uint): Dimension at which splitting should be performed.
        @param[in] cache_require (bool): Defines when points in cache should be stored during density calculation.
        @param[in|out] current_level_blocks (list): Block storage at the current level where new blocks should be added.

        """
        if block.get_density() <= self.__density_threshold or len(block) <= self.__amount_density:
            self.__leafs.append(block)

        else:
            left, right = block.split(split_dimension, cache_require)
            current_level_blocks.append(left)
            current_level_blocks.append(right)


class spatial_block:
    """!
    @brief Geometrical description of BANG block in data space.
    @details Provides services related to spatial functionality and used by bang_block

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
        self.__volume = self.__calculate_volume()


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


    def get_volume(self):
        """!
        @brief Returns volume of current block.
        @details Volume block has uncommon mining here: for 1D is length of a line, for 2D is square of rectangle,
                  for 3D is volume of 3D figure, and for ND is volume of ND figure.

        @return (double) Volume of current block.

        """
        return self.__volume


    def split(self, dimension):
        """!
        @brief Split current block into two spatial blocks in specified dimension.

        @param[in] dimension (uint): Dimension where current block should be split.

        @return (tuple) Pair of new split blocks from current block.

        """
        first_max_corner = self.__max_corner[:]
        second_min_corner = self.__min_corner[:]

        split_border = (self.__max_corner[dimension] + self.__min_corner[dimension]) / 2.0

        first_max_corner[dimension] = split_border
        second_min_corner[dimension] = split_border

        return spatial_block(first_max_corner, self.__min_corner), spatial_block(self.__max_corner, second_min_corner)


    def is_neighbor(self, block):
        """!
        @brief Performs calculation to identify whether specified block is neighbor of current block.
        @details It also considers diagonal blocks as neighbors.

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


    def __calculate_volume(self):
        """!
        @brief Calculates volume of current spatial block.
        @details If empty dimension is detected (where all points has the same value) then such dimension is ignored
                  during calculation of volume.

        @return (double) Volume of current spatial block.

        """

        volume = 0.0
        for i in range(0, len(self.__max_corner)):
            side_length = self.__max_corner[i] - self.__min_corner[i]

            if side_length != 0.0:
                if volume == 0.0: volume = side_length
                else: volume *= side_length

        return volume


class bang_block:
    """!
    @brief BANG-block that represent spatial region in data space.

    """
    def __init__(self, data, region, level, space_block, cache_points=False):
        """!
        @brief Create BANG-block.

        @param[in] data (list): List of points that are processed.
        @param[in] region (uint): Region number - unique value on a level.
        @param[in] level (uint): Level number where block is created.
        @param[in] space_block (spatial_block): Spatial block description in data space.
        @param[in] cache_points (bool): if True then points are stored in memory (used for leaf blocks).

        """
        self.__data = data
        self.__region_number = region
        self.__level = level
        self.__spatial_block = space_block
        self.__cache_points = cache_points

        self.__cluster = None
        self.__points = None
        self.__amount_points = self.__get_amount_points()
        self.__density = self.__calculate_density(self.__amount_points)


    def __str__(self):
        """!
        @brief Returns string representation of BANG-block using region number and level where block is located.

        """
        return "(" + str(self.__region_number) + ", " + str(self.__level) + ")"


    def __len__(self):
        """!
        @brief Returns block size defined by amount of points that are contained by this block.

        """
        return self.__amount_points


    def get_region(self):
        """!
        @brief Returns region number of BANG-block.
        @details Region number is unique on among region numbers on a directory level. Pair of region number and level
                  is unique for all directory.

        @return (uint) Region number.

        """
        return self.__region_number


    def get_density(self):
        """!
        @brief Returns density of the BANG-block.

        @return (double) BANG-block density.

        """
        return self.__density


    def get_cluster(self):
        """!
        @brief Return index of cluster to which the BANG-block belongs to.
        @details Index of cluster may have None value if the block was not assigned to any cluster.

        @return (uint) Index of cluster or None if the block does not belong to any cluster.

        """
        return self.__cluster


    def get_spatial_block(self):
        """!
        @brief Return spatial block - BANG-block description in data space.

        @return (spatial_block) Spatial block of the BANG-block.

        """
        return self.__spatial_block


    def get_points(self):
        """!
        @brief Return points that covers by the BANG-block.

        @return (list) List of point indexes that are covered by the block.

        """
        if self.__points is None:
            self.__cache_covered_data()

        return self.__points


    def set_cluster(self, index):
        """!
        @brief Assign cluster to the BANG-block by index.

        @param[in] index (uint): Index cluster that is assigned to BANG-block.

        """
        self.__cluster = index


    def is_neighbor(self, block):
        """!
        @brief Performs calculation to check whether specified block is neighbor to the current.

        @param[in] block (bang_block): Other BANG-block that should be checked for neighborhood.

        @return (bool) True if blocks are neighbors, False if blocks are not neighbors.

        """
        return self.get_spatial_block().is_neighbor(block.get_spatial_block())


    def split(self, split_dimension, cache_points):
        """!
        @brief Split BANG-block into two new blocks in specified dimension.

        @param[in] split_dimension (uint): Dimension where block should be split.
        @param[in] cache_points (bool): If True then covered points are cached. Used for leaf blocks.

        @return (tuple) Pair of BANG-block that were formed from the current.

        """
        left_region_number = self.__region_number
        right_region_number = self.__region_number + 2 ** self.__level

        first_spatial_block, second_spatial_block = self.__spatial_block.split(split_dimension)

        left = bang_block(self.__data, left_region_number, self.__level + 1, first_spatial_block, cache_points)
        right = bang_block(self.__data, right_region_number, self.__level + 1, second_spatial_block, cache_points)

        return left, right


    def __calculate_density(self, amount_points):
        """!
        @brief Calculates BANG-block density.

        @param[in] amount_points (uint): Amount of points in block.

        @return (double) BANG-block density.

        """
        volume = self.__spatial_block.get_volume()
        if volume != 0.0:
            return amount_points / volume

        return 0.0


    def __get_amount_points(self):
        """!
        @brief Count covered points by the BANG-block and if cache is enable then covered points are stored.

        @return (uint) Amount of covered points.

        """
        amount = 0
        for index in range(len(self.__data)):
            if self.__data[index] in self.__spatial_block:
                self.__cache_point(index)
                amount += 1

        return amount


    def __cache_covered_data(self):
        """!
        @brief Cache covered data.

        """
        self.__cache_points = True
        self.__points = []

        for index_point in range(len(self.__data)):
            if self.__data[index_point] in self.__spatial_block:
                self.__cache_point(index_point)


    def __cache_point(self, index):
        """!
        @brief Store index points.

        @param[in] index (uint): Index point that should be stored.

        """
        if self.__cache_points:
            if self.__points is None:
                self.__points = []

            self.__points.append(index)



class bang:
    """!
    @brief Class implements BANG grid based clustering algorithm.
    @details BANG clustering algorithms uses a multidimensional grid structure to organize the value space surrounding
              the pattern values. The patterns are grouped into blocks and clustered with respect to the blocks by
              a topological neighbor search algorithm @cite inproceedings::bang::1.

    Code example of BANG usage:
    @code
        from pyclustering.cluster.bang import bang, bang_visualizer
        from pyclustering.utils import read_sample
        from pyclustering.samples.definitions import FCPS_SAMPLES

        # Read data three dimensional data.
        data = read_sample(FCPS_SAMPLES.SAMPLE_CHAINLINK)

        # Prepare algorithm's parameters.
        levels = 11

        # Create instance of BANG algorithm.
        bang_instance = bang(data, levels)
        bang_instance.process()

        # Obtain clustering results.
        clusters = bang_instance.get_clusters()
        noise = bang_instance.get_noise()
        directory = bang_instance.get_directory()
        dendrogram = bang_instance.get_dendrogram()

        # Visualize BANG clustering results.
        bang_visualizer.show_blocks(directory)
        bang_visualizer.show_dendrogram(dendrogram)
        bang_visualizer.show_clusters(data, clusters, noise)
    @endcode

    There is visualization of BANG-clustering of three-dimensional data 'chainlink'. BANG-blocks that were formed during
    processing are shown on following figure. The darkest color means highest density, blocks that does not cover points
    are transparent:
    @image html bang_blocks_chainlink.png "Fig. 1. BANG-blocks that cover input data."

    Here is obtained dendrogram that can be used for further analysis to improve clustering results:
    @image html bang_dendrogram_chainlink.png "Fig. 2. BANG dendrogram where the X-axis contains BANG-blocks, the Y-axis contains density."

    BANG clustering result of 'chainlink' data:
    @image html bang_clustering_chainlink.png "Fig. 3. BANG clustering result. Data: 'chainlink'."

    """

    def __init__(self, data, levels, ccore=False, **kwargs):
        """!
        @brief Create BANG clustering algorithm.

        @param[in] data (list): Input data (list of points) that should be clustered.
        @param[in] levels (uint): Amount of levels in tree that is used for splitting (how many times block should be
                    split). For example, if amount of levels is two then surface will be divided into two blocks and
                    each obtained block will be divided into blocks also.
        @param[in] ccore (bool): Reserved positional argument - not used yet.
        @param[in] **kwargs: Arbitrary keyword arguments (available arguments: 'observe').

        <b>Keyword Args:</b><br>
            - density_threshold (double): If block density is smaller than this value then contained data by this
               block is considered as a noise and its points as outliers. Block density is defined by amount of
               points in block divided by block volume: <i>amount_block_points</i>/<i>block_volume</i>. By default
               it is 0.0 - means than only empty blocks are considered as noise. Be aware that this parameter is used
               with parameter 'amount_threshold' - the maximum threshold is considered during processing.
            - amount_threshold (uint): Amount of points in the block when it contained data in bang-block is
               considered as a noise and there is no need to split it till the last level. Be aware that this parameter
               is used with parameter 'density_threshold' - the maximum threshold is considered during processing.

        """
        self.__data = data
        self.__levels = levels
        self.__directory = None
        self.__clusters = []
        self.__noise = []
        self.__cluster_blocks = []
        self.__dendrogram = []
        self.__density_threshold = kwargs.get('density_threshold', 0.0)
        self.__amount_threshold = kwargs.get('amount_threshold', 0)
        self.__ccore = ccore

        self.__validate_arguments()


    def process(self):
        """!
        @brief Performs clustering process in line with rules of BANG clustering algorithm.

        @return (bang) Returns itself (BANG instance).

        @see get_clusters()
        @see get_noise()
        @see get_directory()
        @see get_dendrogram()

        """
        self.__directory = bang_directory(self.__data, self.__levels,
                                          density_threshold=self.__density_threshold,
                                          amount_threshold=self.__amount_threshold)
        self.__allocate_clusters()

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


    def get_directory(self):
        """!
        @brief Returns grid directory that describes grid of the processed data.

        @remark Grid directory is returned only after data processing (method process()). Otherwise None value is returned.

        @return (bang_directory) BANG directory that describes grid of process data.

        @see process()

        """
        return self.__directory


    def get_dendrogram(self):
        """!
        @brief Returns dendrogram of clusters.
        @details Dendrogram is created in following way: the density indices of all regions are calculated and sorted
                  in decreasing order for each cluster during clustering process.

        @remark Dendrogram is returned only after data processing (method process()). Otherwise empty list is returned.

        """
        return self.__dendrogram


    def get_cluster_encoding(self):
        """!
        @brief Returns clustering result representation type that indicate how clusters are encoded.

        @return (type_encoding) Clustering result representation.

        @see get_clusters()

        """

        return type_encoding.CLUSTER_INDEX_LIST_SEPARATION


    def __validate_arguments(self):
        """!
        @brief Check input arguments of BANG algorithm and if one of them is not correct then appropriate exception
                is thrown.

        """
        if len(self.__data) == 0:
            raise ValueError("Input data is empty (size: '%d')." % len(self.__data))

        if self.__levels < 1:
            raise ValueError("Height of the tree should be greater than 0 (current value: '%d')." % self.__levels)

        if self.__density_threshold < 0.0:
            raise ValueError("Density threshold should be greater or equal to 0 (current value: '%d')." %
                             self.__density_threshold)

        if self.__amount_threshold < 0:
            raise ValueError("Amount of points threshold should be greater than 0 (current value: '%d')" %
                             self.__amount_threshold)


    def __allocate_clusters(self):
        """!
        @brief Performs cluster allocation using leafs of tree in BANG directory (the smallest cells).

        """
        leaf_blocks = self.__directory.get_leafs()
        unhandled_block_indexes = set([i for i in range(len(leaf_blocks)) if leaf_blocks[i].get_density() > self.__density_threshold])

        current_block = self.__find_block_center(leaf_blocks, unhandled_block_indexes)
        cluster_index = 0

        while current_block is not None:
            if current_block.get_density() <= self.__density_threshold or len(current_block) <= self.__amount_threshold:
                break

            self.__expand_cluster_block(current_block, cluster_index, leaf_blocks, unhandled_block_indexes)

            current_block = self.__find_block_center(leaf_blocks, unhandled_block_indexes)
            cluster_index += 1

        self.__store_clustering_results(cluster_index, leaf_blocks)


    def __expand_cluster_block(self, block, cluster_index, leaf_blocks, unhandled_block_indexes):
        """!
        @brief Expand cluster from specific block that is considered as a central block.

        @param[in] block (bang_block): Block that is considered as a central block for cluster.
        @param[in] cluster_index (uint): Index of cluster that is assigned to blocks that forms new cluster.
        @param[in] leaf_blocks (list): Leaf BANG-blocks that are considered during cluster formation.
        @param[in] unhandled_block_indexes (set): Set of candidates (BANG block indexes) to become a cluster member. The
                    parameter helps to reduce traversing among BANG-block providing only restricted set of block that
                    should be considered.

        """

        block.set_cluster(cluster_index)
        self.__update_cluster_dendrogram(cluster_index, [block])

        neighbors = self.__find_block_neighbors(block, leaf_blocks, unhandled_block_indexes)
        self.__update_cluster_dendrogram(cluster_index, neighbors)

        for neighbor in neighbors:
            neighbor.set_cluster(cluster_index)
            neighbor_neighbors = self.__find_block_neighbors(neighbor, leaf_blocks, unhandled_block_indexes)
            self.__update_cluster_dendrogram(cluster_index, neighbor_neighbors)

            neighbors += neighbor_neighbors


    def __store_clustering_results(self, amount_clusters, leaf_blocks):
        """!
        @brief Stores clustering results in a convenient way.

        @param[in] amount_clusters (uint): Amount of cluster that was allocated during processing.
        @param[in] leaf_blocks (list): Leaf BANG-blocks (the smallest cells).

        """
        self.__clusters = [[] for _ in range(amount_clusters)]
        for block in leaf_blocks:
            index = block.get_cluster()

            if index is not None:
                self.__clusters[index] += block.get_points()
            else:
                self.__noise += block.get_points()

        self.__clusters = [ list(set(cluster)) for cluster in self.__clusters ]
        self.__noise = list(set(self.__noise))


    def __find_block_center(self, level_blocks, unhandled_block_indexes):
        """!
        @brief Search block that is cluster center for new cluster.

        @return (bang_block) Central block for new cluster, if cluster is not found then None value is returned.

        """
        for i in reversed(range(len(level_blocks))):
            if level_blocks[i].get_density() <= self.__density_threshold:
                return None

            if level_blocks[i].get_cluster() is None:
                unhandled_block_indexes.remove(i)
                return level_blocks[i]

        return None


    def __find_block_neighbors(self, block, level_blocks, unhandled_block_indexes):
        """!
        @brief Search block neighbors that are parts of new clusters (density is greater than threshold and that are
                not cluster members yet), other neighbors are ignored.

        @param[in] block (bang_block): BANG-block for which neighbors should be found (which can be part of cluster).
        @param[in] level_blocks (list): BANG-blocks on specific level.
        @param[in] unhandled_block_indexes (set): Blocks that have not been processed yet.

        @return (list) Block neighbors that can become part of cluster.

        """
        neighbors = []

        handled_block_indexes = []
        for unhandled_index in unhandled_block_indexes:
            if block.is_neighbor(level_blocks[unhandled_index]):
                handled_block_indexes.append(unhandled_index)
                neighbors.append(level_blocks[unhandled_index])

                # Maximum number of neighbors is eight
                if len(neighbors) == 8:
                    break

        for handled_index in handled_block_indexes:
            unhandled_block_indexes.remove(handled_index)

        return neighbors


    def __update_cluster_dendrogram(self, index_cluster, blocks):
        """!
        @brief Append clustered blocks to dendrogram.

        @param[in] index_cluster (uint): Cluster index that was assigned to blocks.
        @param[in] blocks (list): Blocks that were clustered.

        """
        if len(self.__dendrogram) <= index_cluster:
            self.__dendrogram.append([])

        blocks = sorted(blocks, key=lambda block: block.get_density(), reverse=True)
        self.__dendrogram[index_cluster] += blocks

