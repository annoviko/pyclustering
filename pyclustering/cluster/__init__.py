"""!

@brief pyclustering module for cluster analysis.

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
import math
import warnings

try:
    import matplotlib.pyplot as plt
    import matplotlib.gridspec as gridspec
except Exception:
    warnings.warn("Impossible to import matplotlib (please, install 'matplotlib'), pyclustering's visualization "
                  "functionality is not available.")

from pyclustering.utils.color import color as color_list


class canvas_cluster_descr:
    """!
    @brief Description of cluster for representation on canvas.
    
    """

    def __init__(self, cluster, data, marker, markersize, color):
        """!
        @brief Constructor of cluster representation on the canvas.
        
        @param[in] cluster (list): Single cluster that consists of objects or indexes from data.
        @param[in] data (list): Objects that should be displayed, can be None if clusters consist of objects instead of indexes.
        @param[in] marker (string): Type of marker that is used for drawing objects.
        @param[in] markersize (uint): Size of marker that is used for drawing objects.
        @param[in] color (string): Color of the marker that is used for drawing objects.
        
        """
        ## Cluster that may consist of objects or indexes of objects from data.
        self.cluster = cluster
        
        ## Data where objects are stored. It can be None if clusters consist of objects instead of indexes.
        self.data = data
        
        ## Marker that is used for drawing objects.
        self.marker = marker
        
        ## Size of marker that is used for drawing objects.
        self.markersize = markersize
        
        ## Color that is used for coloring marker.
        self.color = color
        
        ## Attribures of the clusters - additional collections of data points that are regarded to the cluster.
        self.attributes = []



class cluster_visualizer_multidim:
    """!
    @brief Visualizer for cluster in multi-dimensional data.
    @details This cluster visualizer is useful for clusters in data whose dimension is greater than 3. The
              multidimensional visualizer helps to overcome 'cluster_visualizer' shortcoming - ability to display
              clusters in 1D, 2D or 3D dimensional data space.

        Example of clustering results visualization where 'Iris' is used:
        @code
            from pyclustering.utils import read_sample
            from pyclustering.samples.definitions import FAMOUS_SAMPLES
            from pyclustering.cluster import cluster_visualizer_multidim

            # load 4D data sample 'Iris'
            sample_4d = read_sample(FAMOUS_SAMPLES.SAMPLE_IRIS)

            # initialize 3 initial centers using K-Means++ algorithm
            centers = kmeans_plusplus_initializer(sample_4d, 3).initialize()

            # performs cluster analysis using X-Means
            xmeans_instance = xmeans(sample_4d, centers)
            xmeans_instance.process()
            clusters = xmeans_instance.get_clusters()

            # visualize obtained clusters in multi-dimensional space
            visualizer = cluster_visualizer_multidim()
            visualizer.append_clusters(clusters, sample_4d)
            visualizer.show(max_row_size=3)
        @endcode

        Visualized clustering results of 'Iris' data (multi-dimensional data):
        @image html xmeans_clustering_famous_iris.png "Fig. 1. X-Means clustering results (data 'Iris')."

        Sometimes no need to display results in all dimensions. Parameter 'filter' can be used to display only
        interesting coordinate pairs. Here is an example of visualization of pair coordinates (x0, x1) and (x0, x2) for
        previous clustering results:
        @code
            visualizer = cluster_visualizer_multidim()
            visualizer.append_clusters(clusters, sample_4d)
            visualizer.show(pair_filter=[[0, 1], [0, 2]])
        @endcode

        Visualized results of specified coordinate pairs:
        @image html xmeans_clustering_famous_iris_filtered.png "Fig. 2. X-Means clustering results (x0, x1) and (x0, x2) (data 'Iris')."

    """

    def __init__(self):
        """!
        @brief Constructs cluster visualizer for multidimensional data.
        @details The visualizer is suitable more data whose dimension is bigger than 3.

        """
        self.__clusters = []
        self.__figure = None
        self.__grid_spec = None


    def append_cluster(self, cluster, data = None, marker = '.', markersize = None, color = None):
        """!
        @brief Appends cluster for visualization.

        @param[in] cluster (list): cluster that may consist of indexes of objects from the data or object itself.
        @param[in] data (list): If defines that each element of cluster is considered as a index of object from the data.
        @param[in] marker (string): Marker that is used for displaying objects from cluster on the canvas.
        @param[in] markersize (uint): Size of marker.
        @param[in] color (string): Color of marker.

        @return Returns index of cluster descriptor on the canvas.

        """
        if len(cluster) == 0:
            raise ValueError("Empty cluster is provided.")

        markersize = markersize or 5
        if color is None:
            index_color = len(self.__clusters) % len(color_list.TITLES)
            color = color_list.TITLES[index_color]

        cluster_descriptor = canvas_cluster_descr(cluster, data, marker, markersize, color)
        self.__clusters.append(cluster_descriptor)


    def append_clusters(self, clusters, data=None, marker='.', markersize=None):
        """!
        @brief Appends list of cluster for visualization.

        @param[in] clusters (list): List of clusters where each cluster may consist of indexes of objects from the data or object itself.
        @param[in] data (list): If defines that each element of cluster is considered as a index of object from the data.
        @param[in] marker (string): Marker that is used for displaying objects from clusters on the canvas.
        @param[in] markersize (uint): Size of marker.

        """

        for cluster in clusters:
            self.append_cluster(cluster, data, marker, markersize)


    def show(self, pair_filter=None, **kwargs):
        """!
        @brief Shows clusters (visualize) in multi-dimensional space.

        @param[in] pair_filter (list): List of coordinate pairs that should be displayed. This argument is used as a filter.
        @param[in] **kwargs: Arbitrary keyword arguments (available arguments: 'visible_axis' 'visible_labels', 'visible_grid', 'row_size').

        <b>Keyword Args:</b><br>
            - visible_axis (bool): Defines visibility of axes on each canvas, if True - axes are visible.
               By default axis of each canvas are not displayed.
            - visible_labels (bool): Defines visibility of labels on each canvas, if True - labels is displayed.
               By default labels of each canvas are displayed.
            - visible_grid (bool): Defines visibility of grid on each canvas, if True - grid is displayed.
               By default grid of each canvas is displayed.
            - max_row_size (uint): Maximum number of canvases on one row.

        """

        if not len(self.__clusters) > 0:
            raise ValueError("There is no non-empty clusters for visualization.")

        cluster_data = self.__clusters[0].data or self.__clusters[0].cluster
        dimension = len(cluster_data[0])

        acceptable_pairs = pair_filter or []
        pairs = []
        amount_axis = 1
        axis_storage = []

        if dimension > 1:
            pairs = self.__create_pairs(dimension, acceptable_pairs)
            amount_axis = len(pairs)

        self.__figure = plt.figure()
        self.__grid_spec = self.__create_grid_spec(amount_axis, kwargs.get('max_row_size', 4))

        for index in range(amount_axis):
            ax = self.__create_canvas(dimension, pairs, index, **kwargs)
            axis_storage.append(ax)

        for cluster_descr in self.__clusters:
            self.__draw_canvas_cluster(axis_storage, cluster_descr, pairs)

        plt.show()


    def __create_grid_spec(self, amount_axis, max_row_size):
        """!
        @brief Create grid specification for figure to place canvases.

        @param[in] amount_axis (uint): Amount of canvases that should be organized by the created grid specification.
        @param[in] max_row_size (max_row_size): Maximum number of canvases on one row.

        @return (gridspec.GridSpec) Grid specification to place canvases on figure.

        """
        row_size = amount_axis
        if row_size > max_row_size:
            row_size = max_row_size

        col_size = math.ceil(amount_axis / row_size)
        return gridspec.GridSpec(col_size, row_size)


    def __create_pairs(self, dimension, acceptable_pairs):
        """!
        @brief Create coordinate pairs that should be displayed.

        @param[in] dimension (uint): Data-space dimension.
        @param[in] acceptable_pairs (list): List of coordinate pairs that should be displayed.

        @return (list) List of coordinate pairs that should be displayed.

        """
        if len(acceptable_pairs) > 0:
            return acceptable_pairs

        return list(itertools.combinations(range(dimension), 2))


    def __create_canvas(self, dimension, pairs, position, **kwargs):
        """!
        @brief Create new canvas with user defined parameters to display cluster or chunk of cluster on it.

        @param[in] dimension (uint): Data-space dimension.
        @param[in] pairs (list): Pair of coordinates that will be displayed on the canvas. If empty than label will not
                    be displayed on the canvas.
        @param[in] position (uint): Index position of canvas on a grid.
        @param[in] **kwargs: Arbitrary keyword arguments (available arguments: 'visible_axis' 'visible_labels', 'visible_grid').

        <b>Keyword Args:</b><br>
            - visible_axis (bool): Defines visibility of axes on each canvas, if True - axes are visible.
               By default axis are not displayed.
            - visible_labels (bool): Defines visibility of labels on each canvas, if True - labels is displayed.
               By default labels are displayed.
            - visible_grid (bool): Defines visibility of grid on each canvas, if True - grid is displayed.
               By default grid is displayed.

        @return (matplotlib.Axis) Canvas to display cluster of chuck of cluster.

        """
        visible_grid = kwargs.get('visible_grid', True)
        visible_labels = kwargs.get('visible_labels', True)
        visible_axis = kwargs.get('visible_axis', False)

        ax = self.__figure.add_subplot(self.__grid_spec[position])

        if dimension > 1:
            if visible_labels:
                ax.set_xlabel("x%d" % pairs[position][0])
                ax.set_ylabel("x%d" % pairs[position][1])
        else:
            ax.set_ylim(-0.5, 0.5)
            ax.set_yticklabels([])

        if visible_grid:
            ax.grid(True)

        if not visible_axis:
            ax.set_yticklabels([])
            ax.set_xticklabels([])

        return ax


    def __draw_canvas_cluster(self, axis_storage, cluster_descr, pairs):
        """!
        @brief Draw clusters.

        @param[in] axis_storage (list): List of matplotlib axis where cluster dimensional chunks are displayed.
        @param[in] cluster_descr (canvas_cluster_descr): Canvas cluster descriptor that should be displayed.
        @param[in] pairs (list): List of coordinates that should be displayed.

        """

        for index_axis in range(len(axis_storage)):
            for item in cluster_descr.cluster:
                if len(pairs) > 0:
                    self.__draw_cluster_item_multi_dimension(axis_storage[index_axis], pairs[index_axis], item, cluster_descr)
                else:
                    self.__draw_cluster_item_one_dimension(axis_storage[index_axis], item, cluster_descr)


    def __draw_cluster_item_multi_dimension(self, ax, pair, item, cluster_descr):
        """!
        @brief Draw cluster chunk defined by pair coordinates in data space with dimension greater than 1.

        @param[in] ax (axis): Matplotlib axis that is used to display chunk of cluster point.
        @param[in] pair (list): Coordinate of the point that should be displayed.
        @param[in] item (list): Data point or index of data point.
        @param[in] cluster_descr (canvas_cluster_descr): Cluster description whose point is visualized.

        """

        index_dimension1 = pair[0]
        index_dimension2 = pair[1]

        if cluster_descr.data is None:
            ax.plot(item[index_dimension1], item[index_dimension2],
                    color=cluster_descr.color, marker=cluster_descr.marker, markersize=cluster_descr.markersize)
        else:
            ax.plot(cluster_descr.data[item][index_dimension1], cluster_descr.data[item][index_dimension2],
                    color=cluster_descr.color, marker=cluster_descr.marker, markersize=cluster_descr.markersize)


    def __draw_cluster_item_one_dimension(self, ax, item, cluster_descr):
        """!
        @brief Draw cluster point in one dimensional data space..

        @param[in] ax (axis): Matplotlib axis that is used to display chunk of cluster point.
        @param[in] item (list): Data point or index of data point.
        @param[in] cluster_descr (canvas_cluster_descr): Cluster description whose point is visualized.

        """

        if cluster_descr.data is None:
            ax.plot(item[0], 0.0,
                    color=cluster_descr.color, marker=cluster_descr.marker, markersize=cluster_descr.markersize)
        else:
            ax.plot(cluster_descr.data[item][0], 0.0,
                    color=cluster_descr.color, marker=cluster_descr.marker, markersize=cluster_descr.markersize)



class cluster_visualizer:
    """!
    @brief Common visualizer of clusters on 1D, 2D or 3D surface.
    @details Use 'cluster_visualizer_multidim' visualizer in case of data dimension is greater than 3.

    @see cluster_visualizer_multidim
    
    """

    def __init__(self, number_canvases=1, size_row=1, titles=None):
        """!
        @brief Constructor of cluster visualizer.
        
        @param[in] number_canvases (uint): Number of canvases that is used for visualization.
        @param[in] size_row (uint): Amount of canvases that can be placed in one row.
        @param[in] titles (list): List of canvas's titles.
        
        Example:
        @code
            # load 2D data sample
            sample_2d = read_sample(SIMPLE_SAMPLES.SAMPLE_SIMPLE1);
            
            # load 3D data sample
            sample_3d = read_sample(FCPS_SAMPLES.SAMPLE_HEPTA);
            
            # extract clusters from the first sample using DBSCAN algorithm
            dbscan_instance = dbscan(sample_2d, 0.4, 2, False);
            dbscan_instance.process();
            clusters_sample_2d = dbscan_instance.get_clusters();
        
            # extract clusters from the second sample using DBSCAN algorithm
            dbscan_instance = dbscan(sample_3d, 1, 3, True);
            dbscan_instance.process();
            clusters_sample_3d = dbscan_instance.get_clusters();
            
            # create plot with two canvases where each row contains 2 canvases.
            size = 2;
            row_size = 2;
            visualizer = cluster_visualizer(size, row_size);
            
            # place clustering result of sample_2d to the first canvas
            visualizer.append_clusters(clusters_sample_2d, sample_2d, 0, markersize = 5);
            
            # place clustering result of sample_3d to the second canvas
            visualizer.append_clusters(clusters_sample_3d, sample_3d, 1, markersize = 30);
            
            # show plot
            visualizer.show();
        @endcode
        
        """
        
        self.__number_canvases = number_canvases
        self.__size_row = size_row
        self.__canvas_clusters = [ [] for _ in range(number_canvases) ]
        self.__canvas_dimensions = [ None for _ in range(number_canvases) ]
        self.__canvas_titles = [ None for _ in range(number_canvases) ]
        
        if titles is not None:
            self.__canvas_titles = titles
        
        self.__default_2d_marker_size = 5
        self.__default_3d_marker_size = 30
    
    
    def append_cluster(self, cluster, data=None, canvas=0, marker='.', markersize=None, color=None):
        """!
        @brief Appends cluster to canvas for drawing.
        
        @param[in] cluster (list): cluster that may consist of indexes of objects from the data or object itself.
        @param[in] data (list): If defines that each element of cluster is considered as a index of object from the data.
        @param[in] canvas (uint): Number of canvas that should be used for displaying cluster.
        @param[in] marker (string): Marker that is used for displaying objects from cluster on the canvas.
        @param[in] markersize (uint): Size of marker.
        @param[in] color (string): Color of marker.
        
        @return Returns index of cluster descriptor on the canvas.
        
        """
        
        if len(cluster) == 0:
            return
        
        if canvas > self.__number_canvases or canvas < 0:
            raise ValueError("Canvas index '%d' is out of range [0; %d]." % self.__number_canvases or canvas)
        
        if color is None:
            index_color = len(self.__canvas_clusters[canvas]) % len(color_list.TITLES)
            color = color_list.TITLES[index_color]
        
        added_canvas_descriptor = canvas_cluster_descr(cluster, data, marker, markersize, color)
        self.__canvas_clusters[canvas].append(added_canvas_descriptor)

        if data is None:
            dimension = len(cluster[0])
            if self.__canvas_dimensions[canvas] is None:
                self.__canvas_dimensions[canvas] = dimension
            elif self.__canvas_dimensions[canvas] != dimension:
                raise ValueError("Only clusters with the same dimension of objects can be displayed on canvas.")
                
        else:
            dimension = len(data[0])
            if self.__canvas_dimensions[canvas] is None:
                self.__canvas_dimensions[canvas] = dimension
            elif self.__canvas_dimensions[canvas] != dimension:
                raise ValueError("Only clusters with the same dimension of objects can be displayed on canvas.")

        if (dimension < 1) or (dimension > 3):
            raise ValueError("Only objects with size dimension 1 (1D plot), 2 (2D plot) or 3 (3D plot) "
                             "can be displayed. For multi-dimensional data use 'cluster_visualizer_multidim'.")
        
        if markersize is None:
            if (dimension == 1) or (dimension == 2):
                added_canvas_descriptor.markersize = self.__default_2d_marker_size
            elif dimension == 3:
                added_canvas_descriptor.markersize = self.__default_3d_marker_size
        
        return len(self.__canvas_clusters[canvas]) - 1
    
    
    def append_cluster_attribute(self, index_canvas, index_cluster, data, marker = None, markersize = None):
        """!
        @brief Append cluster attribure for cluster on specific canvas.
        @details Attribute it is data that is visualized for specific cluster using its color, marker and markersize if last two is not specified.
        
        @param[in] index_canvas (uint): Index canvas where cluster is located.
        @param[in] index_cluster (uint): Index cluster whose attribute should be added.
        @param[in] data (list): List of points (data) that represents attribute.
        @param[in] marker (string): Marker that is used for displaying objects from cluster on the canvas.
        @param[in] markersize (uint): Size of marker.

        """
        
        cluster_descr = self.__canvas_clusters[index_canvas][index_cluster]
        attribute_marker = marker
        if attribute_marker is None:
            attribute_marker = cluster_descr.marker
        
        attribure_markersize = markersize
        if attribure_markersize is None:
            attribure_markersize = cluster_descr.markersize
        
        attribute_color = cluster_descr.color
        
        added_attribute_cluster_descriptor = canvas_cluster_descr(data, None, attribute_marker, attribure_markersize, attribute_color)
        self.__canvas_clusters[index_canvas][index_cluster].attributes.append(added_attribute_cluster_descriptor)
    
    
    def append_clusters(self, clusters, data=None, canvas=0, marker='.', markersize=None):
        """!
        @brief Appends list of cluster to canvas for drawing.
        
        @param[in] clusters (list): List of clusters where each cluster may consist of indexes of objects from the data or object itself.
        @param[in] data (list): If defines that each element of cluster is considered as a index of object from the data.
        @param[in] canvas (uint): Number of canvas that should be used for displaying clusters.
        @param[in] marker (string): Marker that is used for displaying objects from clusters on the canvas.
        @param[in] markersize (uint): Size of marker.

        """
        
        for cluster in clusters:
            self.append_cluster(cluster, data, canvas, marker, markersize)
    
    
    def set_canvas_title(self, text, canvas = 0):
        """!
        @brief Set title for specified canvas.
        
        @param[in] text (string): Title for canvas.
        @param[in] canvas (uint): Index of canvas where title should be displayed.

        """
        
        if canvas > self.__number_canvases:
            raise NameError('Canvas does ' + canvas + ' not exists.')
        
        self.__canvas_titles[canvas] = text


    def get_cluster_color(self, index_cluster, index_canvas):
        """!
        @brief Returns cluster color on specified canvas.
        
        """
        return self.__canvas_clusters[index_canvas][index_cluster].color


    def show(self, figure=None, invisible_axis=True, visible_grid=True, display=True, shift=None):
        """!
        @brief Shows clusters (visualize).
        
        @param[in] figure (fig): Defines requirement to use specified figure, if None - new figure is created for drawing clusters.
        @param[in] invisible_axis (bool): Defines visibility of axes on each canvas, if True - axes are invisible.
        @param[in] visible_grid (bool): Defines visibility of grid on each canvas, if True - grid is displayed.
        @param[in] display (bool): Defines requirement to display clusters on a stage, if True - clusters are displayed,
                    if False - plt.show() should be called by user."
        @param[in] shift (uint): Force canvas shift value - defines canvas index from which custers should be visualized.
        
        @return (fig) Figure where clusters are shown.
        
        """

        canvas_shift = shift
        if canvas_shift is None:
            if figure is not None:
                canvas_shift = len(figure.get_axes())
            else:
                canvas_shift = 0
            
        if figure is not None:
            cluster_figure = figure
        else:
            cluster_figure = plt.figure()
        
        maximum_cols = self.__size_row
        maximum_rows = math.ceil( (self.__number_canvases + canvas_shift) / maximum_cols)
        
        grid_spec = gridspec.GridSpec(maximum_rows, maximum_cols)

        for index_canvas in range(len(self.__canvas_clusters)):
            canvas_data = self.__canvas_clusters[index_canvas]
            if len(canvas_data) == 0:
                continue
        
            dimension = self.__canvas_dimensions[index_canvas]
            
            #ax = axes[real_index];
            if (dimension == 1) or (dimension == 2):
                ax = cluster_figure.add_subplot(grid_spec[index_canvas + canvas_shift])
            else:
                ax = cluster_figure.add_subplot(grid_spec[index_canvas + canvas_shift], projection='3d')
            
            if len(canvas_data) == 0:
                plt.setp(ax, visible=False)
            
            for cluster_descr in canvas_data:
                self.__draw_canvas_cluster(ax, dimension, cluster_descr)
                
                for attribute_descr in cluster_descr.attributes:
                    self.__draw_canvas_cluster(ax, dimension, attribute_descr)
            
            if invisible_axis is True:
                ax.xaxis.set_ticklabels([])
                ax.yaxis.set_ticklabels([])
                
                if (dimension == 3):
                    ax.zaxis.set_ticklabels([])
            
            if self.__canvas_titles[index_canvas] is not None:
                ax.set_title(self.__canvas_titles[index_canvas])
            
            ax.grid(visible_grid)
        
        if display is True:
            plt.show()
        
        return cluster_figure


    def __draw_canvas_cluster(self, ax, dimension, cluster_descr):
        """!
        @brief Draw canvas cluster descriptor.

        @param[in] ax (Axis): Axis of the canvas where canvas cluster descriptor should be displayed.
        @param[in] dimension (uint): Canvas dimension.
        @param[in] cluster_descr (canvas_cluster_descr): Canvas cluster descriptor that should be displayed.

        @return (fig) Figure where clusters are shown.

        """

        cluster = cluster_descr.cluster
        data = cluster_descr.data
        marker = cluster_descr.marker
        markersize = cluster_descr.markersize
        color = cluster_descr.color
        
        for item in cluster:
            if dimension == 1:
                if data is None:
                    ax.plot(item[0], 0.0, color = color, marker = marker, markersize = markersize)
                else:
                    ax.plot(data[item][0], 0.0, color = color, marker = marker, markersize = markersize)

            elif dimension == 2:
                if data is None:
                    ax.plot(item[0], item[1], color = color, marker = marker, markersize = markersize)
                else:
                    ax.plot(data[item][0], data[item][1], color = color, marker = marker, markersize = markersize)
        
            elif dimension == 3:
                if data is None:
                    ax.scatter(item[0], item[1], item[2], c = color, marker = marker, s = markersize)
                else:
                    ax.scatter(data[item][0], data[item][1], data[item][2], c = color, marker = marker, s = markersize)