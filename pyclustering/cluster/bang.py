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


from pyclustering.utils import data_corners


class bang_block:
    def __init__(self, data, dimension, region, level, max_corner, min_corner):
        self.__region_number = region
        self.__level = level
        self.__data = data
        self.__dimension = dimension
        self.__max_corner = max_corner
        self.__min_corner = min_corner
        self.__density = self.__calculate_density()


    def get_region(self):
        return self.__region_number


    def get_level(self):
        return self.__level


    def get_density(self):
        return self.__density


    def split(self):
        left_region_number = self.__region_number
        right_region_number = self.__region_number + 2 ** self.__level

        dimension = self.__dimension + 1
        if dimension > len(self.__data[0]):
            dimension = 0

        left_min_corner = self.__min_corner[:]
        right_max_corner = self.__max_corner[:]

        left_min_corner[dimension] += (self.__max_corner[dimension] - self.__min_corner[dimension]) / 2.0
        right_max_corner[dimension] = left_min_corner[dimension]

        left = bang_block(self.__data, dimension, left_region_number, self.__level + 1, self.__max_corner, left_min_corner)
        right = bang_block(self.__data, dimension, right_region_number, self.__level + 1, right_max_corner, self.__min_corner)

        return left, right


    def contained(self, point):
        for i in range(len(point)):
            if point[i] <= self.__min_corner[i] or point[i] > self.__max_corner[i]:
                return False


    def __calculate_density(self):
        volume = self.__max_corner[0] - self.__min_corner[0]
        for i in range(1, len(self.__max_corner)):
            volume *= self.__max_corner[i] - self.__min_corner[i]

        amount = self.__get_amount_points()
        return amount / volume


    def __get_amount_points(self):
        amount = 0
        for point in self.__data:
            if self.contained(point):
                amount += 1

        return amount



class bang:
    def __init__(self, data, levels, density_threshold = 0.0):
        self.__data = data
        self.__levels = levels
        self.__blocks = []
        self.__density_threshold = density_threshold


    def process(self):
        self.__build_blocks()
        self.__blocks = sorted(self.__blocks, key=lambda block: block.get_density())


    def get_blocks(self):
        return self.__blocks


    def __build_blocks(self):
        max_corner, min_corner = data_corners(self.__data)
        root_block = bang_block(self.__data, 0, 0, 0, max_corner, min_corner)

        self.__blocks.append(root_block)
        level_blocks = [root_block]

        for level in range(self.__levels):
            level_blocks = self.__build_next_level_blocks(level_blocks)


    def __build_next_level_blocks(self, level_blocks):
        next_level_blocks = []
        for block in level_blocks:
            left, right = block.split()

            next_level_blocks.append(left)
            next_level_blocks.append(right)

        return next_level_blocks