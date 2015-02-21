"""!

@brief pyclustering module for cluster analysis.

@authors Andrei Novikov (spb.andr@yandex.ru)
@version 1.0
@date 2014-2015
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

from abc import ABCMeta, abstractmethod;

class cluster_interface(metaclass = ABCMeta):
    @abstractmethod
    def process(self):
        """!
        
        @brief Abstract method that is responsible for performing cluster analysis.
        
        """
        pass;
    
    @abstractmethod
    def get_clusters(self):
        """!
        
        @brief Abstract method that is responsible for returning allocated clusters.
        
        @return (list) Allocated clusters.
        
        @see process()
        @see get_noise()
        
        """
        pass;
    
    @abstractmethod
    def get_noise(self):
        """!
        
        @brief Abstract method that is responsible for returning allocated noise.
        
        @return (list) Allocated noise.
        
        @see process()
        @see get_noise()
        
        """
        pass;