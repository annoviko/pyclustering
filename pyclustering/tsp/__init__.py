"""!

@brief pyclustering module for travelling salesman problem algorithms.

@authors Andrei Novikov, Aleksey Kukushkin (pyclustering@yandex.ru)
@date 2014-2016
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


class tsp_result:
    """!
    @brief Describes result of solving travelling salesman problem.
    
    @details It consists of information about sequence of visited objects and the shortest path length.
    
    """  
    
    def __init__(self):
        """!
        @brief Default constructor of TSP result.
        
        """
        
        ## The shortest path for solving travelling salesman problem.
        self.shortest_length = 0;
        
        ## Sequence of objects that have been visited to obtain shortest path.
        self.object_sequence = [];