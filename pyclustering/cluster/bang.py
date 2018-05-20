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


# TODO: Store blocks in block directory and control them via directory

class bang_visualizer:
    @staticmethod
    def show_level_blocks(data, level_blocks):
        visualizer = cluster_visualizer()
        visualizer.append_cluster(data)

        figure = visualizer.show(display=False)

        bang_visualizer.__draw_blocks(figure, 0, level_blocks)
        plt.show();


    @staticmethod
    def __draw_blocks(figure, offset, level_blocks):
        ax = figure.get_axes()[offset];
        ax.grid(False)

        for block in level_blocks:
            bang_visualizer.__draw_block(ax, block)


    @staticmethod
    def __draw_block(ax, block):
        max_corner, min_corner = block.get_corners()
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


class bang_block:
    def __init__(self, data, dimension, region, level, max_corner, min_corner, cache_points=False):
        self.__region_number = region
        self.__level = level
        self.__data = data
        self.__dimension = dimension
        self.__max_corner = max_corner
        self.__min_corner = min_corner
        self.__cache_points = cache_points
        self.__cluster = None
        self.__points = None
        self.__density = self.__calculate_density()


    def __str__(self):
        return "(" + str(self.__region_number) + ", " + str(self.__level) + ")"


    def get_region(self):
        return self.__region_number


    def get_level(self):
        return self.__level


    def get_density(self):
        return self.__density


    def get_cluster(self):
        return self.__cluster


    def get_corners(self):
        return self.__max_corner, self.__min_corner


    def get_points(self):
        if self.__points is not None:
            return self.__points

        # TODO: return for upper level - traverse tree is preferable than whole data with calculation
        return [index for index in range(len(self.__data)) if self.contained(self.__data[index])]


    def set_cluster(self, index):
        self.__cluster = index


    def is_neighbor(self, block):
        if block is self:
            return False;

        if block.get_region() == 17 and self.__region_number == 1:
            print("Error case")

        block_max_corner, block_min_corner = block.get_corners()

        similarity_counter = 0
        dimension = len(block_max_corner)

        length_edges = [self.__max_corner[i] - self.__min_corner[i] for i in range(dimension)]
        tolerances = [length_edge * 0.0001 for length_edge in length_edges]

        for i in range(dimension):
            diff = abs(block_max_corner[i] - self.__max_corner[i])
            if diff <= length_edges[i] + tolerances[i]:
                similarity_counter += 1

        print(self.get_region(), block.get_region(), similarity_counter)

        if similarity_counter == dimension:
            return True

        return False


    def split(self, cache_points):
        left_region_number = self.__region_number
        right_region_number = self.__region_number + 2 ** self.__level

        dimension = self.__dimension + 1
        if dimension >= len(self.__data[0]):
            dimension = 0

        first_max_corner = self.__max_corner[:]
        first_min_corner = self.__min_corner[:]
        second_max_corner = self.__max_corner[:]
        second_min_corner = self.__min_corner[:]

        split_border = (self.__max_corner[dimension] + self.__min_corner[dimension]) / 2.0
        first_max_corner[dimension] = split_border
        second_min_corner[dimension] = split_border

        left = bang_block(self.__data, dimension, left_region_number, self.__level + 1, first_max_corner, first_min_corner, cache_points)
        right = bang_block(self.__data, dimension, right_region_number, self.__level + 1, second_max_corner, second_min_corner, cache_points)

        return left, right


    def contained(self, point):
        for i in range(len(point)):
            if point[i] < self.__min_corner[i] or point[i] > self.__max_corner[i]:
                return False

        return True


    def __calculate_density(self):
        volume = self.__max_corner[0] - self.__min_corner[0]
        for i in range(1, len(self.__max_corner)):
            volume *= self.__max_corner[i] - self.__min_corner[i]

        amount = self.__get_amount_points()
        return amount / volume


    def __get_amount_points(self):
        amount = 0
        for index in range(len(self.__data)):
            if self.contained(self.__data[index]):
                amount += 1

                if self.__cache_points:
                    if self.__points is None:
                        self.__points = []

                    self.__points.append(index)

        return amount



class bang:
    def __init__(self, data, levels, density_threshold = 0.0):
        self.__data = data
        self.__levels = levels
        self.__blocks = []
        self.__clusters = []
        self.__noise = []
        self.__cluster_blocks = []
        self.__density_threshold = density_threshold


    def process(self):
        self.__validate_arguments()

        self.__build_blocks()
        self.__allocate_clusters()


    def get_clusters(self):
        return self.__clusters


    def get_noise(self):
        return self.__noise


    def get_level_blocks(self, level=-1):
        return self.__blocks[level]


    def __validate_arguments(self):
        if self.__levels <= 0:
            raise ValueError("Incorrect amount of levels '%d'. Level value should be greater than 0." % (self.__levels))

        if len(self.__data) == 0:
            raise ValueError("Empty input data. Data should contain at least one point.")

        if self.__density_threshold < 0:
            raise ValueError("Incorrect density threshold '%f'. Density threshold should not be negative." % (self.__density_threshold))


    def __build_blocks(self):
        min_corner, max_corner = data_corners(self.__data)
        root_block = bang_block(self.__data, 0, 0, 0, max_corner, min_corner, self.__levels == 1)

        level_blocks = [root_block]
        self.__blocks.append(level_blocks)

        for level in range(1, self.__levels):
            cache_points = (level == self.__levels - 1)
            level_blocks = self.__build_next_level_blocks(level_blocks, cache_points)
            level_blocks = sorted(level_blocks, key=lambda block: block.get_density())
            self.__blocks.append(level_blocks)


    def __build_next_level_blocks(self, level_blocks, cache_points):
        next_level_blocks = []
        for block in level_blocks:
            left, right = block.split(cache_points)

            next_level_blocks.append(left)
            next_level_blocks.append(right)

        return next_level_blocks


    def __allocate_clusters(self):
        level_blocks = self.__blocks[-1]
        unhandled_block_indexes = set([i for i in range(len(level_blocks)) if level_blocks[i].get_density() > self.__density_threshold])
        appropriate_block_indexes = set(unhandled_block_indexes)

        current_block = self.__find_block_center(level_blocks)
        cluster_index = 0

        while current_block is not None:
            if (current_block.get_density() <= self.__density_threshold):
                break

            current_block.set_cluster(cluster_index)

            neighbors = self.__find_block_neighbors(current_block, level_blocks, unhandled_block_indexes)
            for neighbor in neighbors:
                neighbor.set_cluster(cluster_index)
                neighbors += self.__find_block_neighbors(neighbor, level_blocks, unhandled_block_indexes)

            current_block = self.__find_block_center(level_blocks)
            cluster_index += 1

        self.__clusters = [[] for _ in range(cluster_index)]
        for appropriate_index in appropriate_block_indexes:
            block = level_blocks[appropriate_index]
            index = block.get_cluster()
            if index is not None:
                self.__clusters[index] += block.get_points()
            else:
                self.__noise += block.get_points()

        self.__clusters = [ list(set(cluster)) for cluster in self.__clusters ]


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

                # Maximum number of neighbors is four
                if len(neighbors) == 4:
                    break

        for handled_index in handled_block_indexes:
            unhandled_block_indexes.remove(handled_index)

        return neighbors
