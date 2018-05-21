"""!

@brief Cluster analysis algorithm: BANG.
@details Implementation based on paper @cite inproceedings::bang::1.

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


import matplotlib.pyplot as plt
import matplotlib.patches as patches

from pyclustering.utils import data_corners

from pyclustering.cluster import cluster_visualizer


class bang_visualizer:
    @staticmethod
    def show_blocks(data, directory):
        visualizer = cluster_visualizer()
        visualizer.append_cluster(data)

        figure = visualizer.show(display=False)

        bang_visualizer.__draw_blocks(figure, 0, directory.get_leafs())
        plt.show()


    @staticmethod
    def __draw_blocks(figure, offset, level_blocks):
        ax = figure.get_axes()[offset]
        ax.grid(False)

        for block in level_blocks:
            bang_visualizer.__draw_block(ax, block)


    @staticmethod
    def __draw_block(ax, block):
        max_corner, min_corner = block.get_spatial_block().get_corners()
        belong_cluster = block.get_cluster() is not None

        if len(max_corner) == 2:
            rect = patches.Rectangle(min_corner, max_corner[0] - min_corner[0], max_corner[1] - min_corner[1],
                                     fill=belong_cluster,
                                     alpha=0.5)
            ax.add_patch(rect)

            xlabel = (max_corner[0] + min_corner[0]) / 2.0
            ylabel = (max_corner[1] + min_corner[1]) / 2.0
            ax.text(xlabel, ylabel, str(block.get_region()), ha="center", va="center")

        else:
            raise ValueError("Impossible to display blocks on non-2D dimensional data.")



class bang_directory:
    def __init__(self, data, levels, density_threshold=0.0):
        """!
        @brief Create BANG directory - basically tree structure with direct access to leafs.

        @param[in] levels (uint): Height of the blocks tree.
        @param[in] density_threshold (double): The lowest level of density when contained data by bang-block is
                    considered as a noise and there is no need to split it till the last level.

        """
        self.__data = data
        self.__levels = levels
        self.__density_threshold = density_threshold
        self.__leafs = []
        self.__root = None

        self.__create_directory()


    def get_leafs(self):
        return self.__leafs


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
        else:
            self.__build_directory_levels()


    def __build_directory_levels(self):
        """!
        @brief Build levels of direction if amount of level is greater than one.

        """
        previous_level_blocks = [ self.__root ]
        for level in range(1, self.__levels):
            previous_level_blocks = self.__build_level(previous_level_blocks, level)

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
        if block.get_density() <= self.__density_threshold:
            self.__leafs.append(block)

        else:
            left, right = block.split(split_dimension, cache_require)
            current_level_blocks.append(left)
            current_level_blocks.append(right)



class spatial_block:
    """!
    @brief Geometrical description of BANG block in data space.
    @details Provides services related to spatial function and used by bang_block

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

        """
        return "(max: %s; min: %s)" % (self.__max_corner, self.__min_corner)


    def __contains__(self, point):
        """!
        @brief Point is considered as contained if it lies in block (belong to it).

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

        @return (double) Volume of current spatial block.

        """
        volume = self.__max_corner[0] - self.__min_corner[0]
        for i in range(1, len(self.__max_corner)):
            volume *= self.__max_corner[i] - self.__min_corner[i]

        return volume



class bang_block:
    def __init__(self, data, region, level, space_block, cache_points=False):
        self.__data = data
        self.__region_number = region
        self.__level = level
        self.__spatial_block = space_block
        self.__cache_points = cache_points

        self.__cluster = None
        self.__points = None
        self.__density = self.__calculate_density()


    def __str__(self):
        return "(" + str(self.__region_number) + ", " + str(self.__level) + ")"


    def get_region(self):
        return self.__region_number


    def get_density(self):
        return self.__density


    def get_cluster(self):
        return self.__cluster


    def get_spatial_block(self):
        return self.__spatial_block


    def get_points(self):
            return self.__points


    def set_cluster(self, index):
        self.__cluster = index


    def is_neighbor(self, block):
        return self.get_spatial_block().is_neighbor(block.get_spatial_block())


    def split(self, split_dimension, cache_points):
        left_region_number = self.__region_number
        right_region_number = self.__region_number + 2 ** self.__level

        first_spatial_block, second_spatial_block = self.__spatial_block.split(split_dimension)

        left = bang_block(self.__data, left_region_number, self.__level + 1, first_spatial_block, cache_points)
        right = bang_block(self.__data, right_region_number, self.__level + 1, second_spatial_block, cache_points)

        return left, right


    def __calculate_density(self):
        return self.__get_amount_points() / self.__spatial_block.get_volume()


    def __get_amount_points(self):
        amount = 0
        for index in range(len(self.__data)):
            if self.__data[index] in self.__spatial_block:
                self.__cache_point(index)
                amount += 1

        return amount


    def __cache_point(self, index):
        if self.__cache_points:
            if self.__points is None:
                self.__points = []

            self.__points.append(index)



class bang:
    def __init__(self, data, levels, density_threshold = 0.0):
        self.__data = data
        self.__levels = levels
        self.__directory = None
        self.__clusters = []
        self.__noise = []
        self.__cluster_blocks = []
        self.__density_threshold = density_threshold


    def process(self):
        self.__validate_arguments()

        self.__directory = bang_directory(self.__data, self.__levels, self.__density_threshold)
        self.__allocate_clusters()


    def get_clusters(self):
        return self.__clusters


    def get_noise(self):
        return self.__noise


    def get_directory(self):
        return self.__directory


    def __validate_arguments(self):
        if self.__levels <= 0:
            raise ValueError("Incorrect amount of levels '%d'. Level value should be greater than 0." % self.__levels)

        if len(self.__data) == 0:
            raise ValueError("Empty input data. Data should contain at least one point.")

        if self.__density_threshold < 0:
            raise ValueError("Incorrect density threshold '%f'. Density threshold should not be negative." % self.__density_threshold)


    def __allocate_clusters(self):
        leaf_blocks = self.__directory.get_leafs()
        unhandled_block_indexes = set([i for i in range(len(leaf_blocks)) if leaf_blocks[i].get_density() > self.__density_threshold])
        appropriate_block_indexes = set(unhandled_block_indexes)

        current_block = self.__find_block_center(leaf_blocks)
        cluster_index = 0

        while current_block is not None:
            if current_block.get_density() <= self.__density_threshold:
                break

            self.__expand_cluster_block(current_block, cluster_index, leaf_blocks, unhandled_block_indexes)

            current_block = self.__find_block_center(leaf_blocks)
            cluster_index += 1

        self.__store_clustering_results(cluster_index, appropriate_block_indexes, leaf_blocks)


    def __expand_cluster_block(self, block, cluster_index, leaf_blocks, unhandled_block_indexes):
        block.set_cluster(cluster_index)

        neighbors = self.__find_block_neighbors(block, leaf_blocks, unhandled_block_indexes)
        for neighbor in neighbors:
            neighbor.set_cluster(cluster_index)
            neighbors += self.__find_block_neighbors(neighbor, leaf_blocks, unhandled_block_indexes)


    def __store_clustering_results(self, amount_clusters, appropriate_block_indexes, leaf_blocks):
        self.__clusters = [[] for _ in range(amount_clusters)]
        for appropriate_index in appropriate_block_indexes:
            block = leaf_blocks[appropriate_index]
            index = block.get_cluster()

            if index is not None:
                self.__clusters[index] += block.get_points()
            else:
                self.__noise += block.get_points()

        self.__clusters = [ list(set(cluster)) for cluster in self.__clusters ]
        self.__noise = list(set(self.__noise))


    def __find_block_center(self, level_blocks):
        for i in reversed(range(len(level_blocks))):
            if level_blocks[i].get_cluster() is None:
                return level_blocks[i]

        return None


    def __find_block_neighbors(self, block, level_blocks, unhandled_block_indexes):
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
