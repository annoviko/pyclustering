"""!

@brief Output dynamic visualizer

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

import warnings

try:
    import matplotlib.pyplot as plt
except Exception as error_instance:
    warnings.warn("Impossible to import matplotlib (please, install 'matplotlib'), pyclustering's visualization "
                  "functionality is not available (details: '%s')." % str(error_instance))

from pyclustering.utils import set_ax_param


class canvas_descr:
    """!
    @brief Describes plot where dynamic is displayed.
    @details Used by 'dynamic_visualizer' class.

    """

    def __init__(self, x_title=None, y_title=None, x_lim=None, y_lim=None, x_labels=True, y_labels=True):
        """!
        @brief Constructor of canvas.

        @param[in] x_title (string): Title for X axis, if 'None', then nothing is displayed.
        @param[in] y_title (string): Title for Y axis, if 'None', then nothing is displayed.
        @param[in] x_lim (list): Defines borders of X axis like [from, to], for example [0, 3.14], if 'None' then
                    borders are calculated automatically.
        @param[in] y_lim (list): Defines borders of Y axis like [from, to], if 'None' then borders are calculated
                    automatically.
        @param[in] x_labels (bool): If True then labels of X axis are displayed.
        @param[in] y_labels (bool): If True then labels of Y axis are displayed.

        """

        ## Title for X axis.
        self.x_title  = x_title;

        ## Title for Y axis.
        self.y_title  = y_title;

        ## Borders of X axis.
        self.x_lim    = x_lim;

        ## Borders of Y axis.
        self.y_lim    = y_lim;

        ## Defines whether X label should be displayed.
        self.x_labels = x_labels;

        ## Defines whether Y label should be displayed.
        self.y_labels = y_labels;


class dynamic_descr:
    """!
    @brief Output dynamic description that used to display.
    @details Used by 'dynamic_visualizer' class.

    """

    def __init__(self, canvas, time, dynamics, separate, color):
        """!
        @brief Constructor of output dynamic descriptor.

        @param[in] canvas (uint): Index of canvas where dynamic should be displayed, in case of 'separate'
                    representation this argument is considered as a first canvas from that displaying should be done.
        @param[in] time (list): Time points that are considered as a X axis.
        @param[in] dynamics (list): Dynamic or dynamics that should be displayed.
        @param[in] separate (bool|list): If 'True' then each dynamic is displayed on separate canvas, if it is defined
                    by list, for example, [ [1, 2], [3, 4] ], then the first and the second dynamics are displayed on
                    the canvas with index 'canvas' and the third and forth are displayed on the next 'canvas + 1'
                    canvas.
        @param[in] color (string): Color that is used to display output dynamic(s).

        """

        ## Index of canvas where (or from which) dynamic should be displayed.
        self.canvas     = canvas;

        ## Time points.
        self.time       = time;

        ## Dynamic or dynamics.
        self.dynamics   = dynamics;

        ## Defines how dynamic(s) should be displayed.
        self.separate   = self.__get_canonical_separate(separate);

        ## Color of dynamic.
        self.color      = color;


    def get_axis_index(self, index_dynamic):
        """!
        @brief Returns index of canvas where specified dynamic (by index 'index_dynamic') should be displayed.

        @param[in] index_dynamic (uint): Index of dynamic that should be displayed.

        @return (uint) Index of canvas.

        """
        return self.separate[index_dynamic];


    def __get_canonical_separate(self, input_separate):
        """!
        @brief Return unified representation of separation value.
        @details It represents list whose size is equal to amount of dynamics, where index of dynamic will show
                  where it should be displayed.

        @param[in] input_separate (bool|list): Input separate representation that should transformed.

        @return (list) Indexes where each dynamic should be displayed.

        """
        if (isinstance(input_separate, list)):
            separate = [0] * len(self.dynamics[0]);
            for canvas_index in range(len(input_separate)):
                dynamic_indexes = input_separate[canvas_index];
                for dynamic_index in dynamic_indexes:
                    separate[dynamic_index] = canvas_index;
            
            return separate;
        
        elif (input_separate is False):
            if (isinstance(self.dynamics[0], list) is True):
                return [ self.canvas ] * len(self.dynamics[0]);
            else:
                return [ self.canvas ];
        
        elif (input_separate is True):
            if (isinstance(self.dynamics[0], list) is True):
                return range(self.canvas, self.canvas + len(self.dynamics[0]));
            else:
                return [ self.canvas ];

        else:
            raise Exception("Incorrect type of argument 'separate' '%s'." % type(input_separate));


class dynamic_visualizer:
    """!
    @brief Basic output dynamic visualizer.
    @details The aim of the visualizer is to displayed output dynamic of any process, for example, output dynamic of
              oscillatory network.

    """

    def __init__(self, canvas, x_title=None, y_title=None, x_lim=None, y_lim=None, x_labels=True, y_labels=True):
        """!
        @brief Construct dynamic visualizer.
        @details Default properties that are generalized in the constructor, for example, X axis title, can be
                  changed by corresponding method: 'set_canvas_properties'.

        @param[in] canvas (uint): Amount of canvases that is used for visualization.
        @param[in] x_title (string): Title for X axis of canvases, if 'None', then nothing is displayed.
        @param[in] y_title (string): Title for Y axis of canvases, if 'None', then nothing is displayed.
        @param[in] x_lim (list): Defines borders of X axis like [from, to], for example [0, 3.14], if 'None' then
                    borders are calculated automatically.
        @param[in] y_lim (list): Defines borders of Y axis like [from, to], if 'None' then borders are calculated
                    automatically.
        @param[in] x_labels (bool): If True then labels of X axis are displayed.
        @param[in] y_labels (bool): If True then labels of Y axis are displayed.

        """
        self.__size = canvas;
        self.__canvases = [ canvas_descr(x_title, y_title, x_lim, y_lim, x_labels, y_labels) for _ in range(canvas) ];
        self.__dynamic_storage = [];


    def set_canvas_properties(self, canvas, x_title=None, y_title=None, x_lim=None, y_lim=None, x_labels=True, y_labels=True):
        """!
        @brief Set properties for specified canvas.

        @param[in] canvas (uint): Index of canvas whose properties should changed.
        @param[in] x_title (string): Title for X axis, if 'None', then nothing is displayed.
        @param[in] y_title (string): Title for Y axis, if 'None', then nothing is displayed.
        @param[in] x_lim (list): Defines borders of X axis like [from, to], for example [0, 3.14], if 'None' then
                    borders are calculated automatically.
        @param[in] y_lim (list): Defines borders of Y axis like [from, to], if 'None' then borders are calculated
                    automatically.
        @param[in] x_labels (bool): If True then labels of X axis are displayed.
        @param[in] y_labels (bool): If True then labels of Y axis are displayed.

        """
        self.__canvases[canvas] = canvas_descr(x_title, y_title, x_lim, y_lim, x_labels, y_labels);


    def append_dynamic(self, t, dynamic, canvas=0, color='blue'):
        """!
        @brief Append single dynamic to specified canvas (by default to the first with index '0').

        @param[in] t (list): Time points that corresponds to dynamic values and considered on a X axis.
        @param[in] dynamic (list): Value points of dynamic that are considered on an Y axis.
        @param[in] canvas (uint): Canvas where dynamic should be displayed.
        @param[in] color (string): Color that is used for drawing dynamic on the canvas.

        """
        description = dynamic_descr(canvas, t, dynamic, False, color);
        self.__dynamic_storage.append(description);
        self.__update_canvas_xlim(description.time, description.separate);


    def append_dynamics(self, t, dynamics, canvas=0, separate=False, color='blue'):
        """!
        @brief Append several dynamics to canvas or canvases (defined by 'canvas' and 'separate' arguments).

        @param[in] t (list): Time points that corresponds to dynamic values and considered on a X axis.
        @param[in] dynamics (list): Dynamics where each of them is considered on Y axis.
        @param[in] canvas (uint): Index of canvas where dynamic should be displayed, in case of 'separate'
                    representation this argument is considered as a first canvas from that displaying should be done.
        @param[in] separate (bool|list): If 'True' then each dynamic is displayed on separate canvas, if it is defined
                    by list, for example, [ [1, 2], [3, 4] ], then the first and the second dynamics are displayed on
                    the canvas with index 'canvas' and the third and forth are displayed on the next 'canvas + 1'
                    canvas.
        @param[in] color (string): Color that is used to display output dynamic(s).

        """
        description = dynamic_descr(canvas, t, dynamics, separate, color);
        self.__dynamic_storage.append(description);
        self.__update_canvas_xlim(description.time, description.separate);


    def show(self, axis=None, display=True):
        """!
        @brief Draw and show output dynamics.

        @param[in] axis (axis): If is not 'None' then user specified axis is used to display output dynamic.
        @param[in] display (bool): Whether output dynamic should be displayed or not, if not, then user
                    should call 'plt.show()' by himself.

        """
        
        if (not axis):
            (_, axis) = plt.subplots(self.__size, 1);
        
        self.__format_canvases(axis);
        
        for dynamic in self.__dynamic_storage:
            self.__display_dynamic(axis, dynamic);
        
        if (display):
            plt.show();


    def __display_dynamic(self, axis, dyn_descr):
        if (isinstance(dyn_descr.dynamics[0], list) is True):
            self.__display_multiple_dynamic(axis, dyn_descr);
        
        else:
            self.__display_single_dynamic(axis, dyn_descr);


    def __display_multiple_dynamic(self, axis, dyn_descr):
        num_items = len(dyn_descr.dynamics[0]);
        for index in range(0, num_items, 1):
            y = [item[index] for item in dyn_descr.dynamics];
            
            axis_index = dyn_descr.get_axis_index(index);
            ax = self.__get_axis(axis, axis_index);
            
            ax.plot(dyn_descr.time, y, 'b-', linewidth = 0.5);


    def __display_single_dynamic(self, axis, dyn_descr):
        ax = self.__get_axis(axis, dyn_descr.canvas);
        ax.plot(dyn_descr.time, dyn_descr.dynamics, 'b-', linewidth = 0.5);


    def __format_canvases(self, axis):
        for index in range(self.__size):
            canvas = self.__canvases[index];
            
            ax = self.__get_axis(axis, index);
            set_ax_param(ax, canvas.x_title, canvas.y_title, canvas.x_lim, canvas.y_lim, canvas.x_labels, canvas.y_labels, True);
            
            if ( (len(self.__canvases) > 1) and (index != len(self.__canvases) - 1) ):
                ax.get_xaxis().set_visible(False);


    def __update_canvas_xlim(self, t, separate):
        for index in separate:
            self.__update_single_canvas_xlim(index, t);


    def __update_single_canvas_xlim(self, canvas_index, t):
        dynamic_xlim = [0, t[len(t) - 1]];
        if ( (self.__canvases[canvas_index].x_lim is None) or (self.__canvases[canvas_index].x_lim < dynamic_xlim) ):
            self.__canvases[canvas_index].x_lim = dynamic_xlim;


    def __get_axis(self, axis, index):
        if (index >= len(self.__canvases)):
            raise Exception("Impossible to get axis with index '%d' - total number of canvases '%d'."
                            % index, len(self.__canvases));
        
        ax = axis;
        if (self.__size > 1):
            ax = axis[index];
        
        return ax;