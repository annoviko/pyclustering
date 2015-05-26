"""!

@brief pyclustering module for cluster analysis.

@authors Andrei Novikov (spb.andr@yandex.ru)
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


class cluster_visual_descr:
    cluster = None;
    data = None;
    canvas = None;
    marker = None;
    
    def __init__(self, cluster, data, canvas, marker):
        self.cluster = cluster;
        self.data = data;
        self.canvas = canvas;
        self.marker = marker;
    

class cluster_visualizer:
    __colors = ['b', 'r', 'g', 'y', 'm', 'k', 'c'];
    
    __cluster_descriptors = None;
    __number_canvases = None;
    
    
    def __init__(self, number_canvases = 1):
        self.__number_canvases = number_canvases;
        
    
    def append_cluster(self, cluster, data = None, canvas = 1, marker = '.'):
        if (canvas > self.__number_canvases):
            raise NameError('Canvas does ' + canvas + ' not exists');
            
        self.__cluster_descriptors.append( cluster_visual_descr(cluster, data, canvas, marker) );
    
    
    def addend_clusters(self, clusters, data = None, canvas = 1, marker = '.'):
        for cluster in clusters:
            self.append_cluster(cluster, data, canvas, marker);
    
    
    def show(self, visible_axis = True):
        pass;
    