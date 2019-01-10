"""!

@brief Colors used by pyclustering library for visualization.

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


class color:
    """!
    @brief Consists titles of colors that are used by pyclustering for visualization.
    
    """

    @staticmethod
    def get_color(sequential_index):
        """!
        @brief Returns color using round robin to avoid out of range exception.

        @param[in] sequential_index (uint): Index that should be converted to valid color index.

        @return (uint) Color from list color.TITLES.

        """
        return color.TITLES[sequential_index % len(color.TITLES)]


    ## List of color titles that are used by pyclustering for visualization.
    TITLES = [  'red', 'blue', 'darkgreen', 'gold', 'violet', 
                'deepskyblue', 'darkgrey', 'lightsalmon', 'deeppink', 'yellow',
                'black', 'mediumspringgreen', 'orange', 'darkviolet', 'darkblue',
                'silver', 'lime', 'pink', 'brown', 'bisque',
                'dimgray', 'firebrick', 'darksalmon', 'chartreuse', 'skyblue',
                'purple', 'fuchsia', 'palegoldenrod', 'coral', 'hotpink',
                'gray', 'tan', 'crimson', 'teal', 'olive']
