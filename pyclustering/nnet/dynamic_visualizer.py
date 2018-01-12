"""!

@brief Output dynamic visualizer

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


import matplotlib.pyplot as plt;

from pyclustering.utils import set_ax_param;


class canvas_descr:
    def __init__(self, x_title=None, y_title=None, x_lim=None, y_lim=None, x_labels=True, y_labels=True):
        self.x_title  = x_title;
        self.y_title  = y_title;
        self.x_lim    = x_lim;
        self.y_lim    = y_lim;
        self.x_labels = x_labels;
        self.y_labels = y_labels;


class dynamic_descr:
    def __init__(self, canvas, time, dynamics, separate, color):
        self.canvas     = canvas;
        self.time       = time;
        self.dynamics   = dynamics;
        self.separate   = separate;
        self.color      = color;
        
        self.separate   = self.__get_canonical_separate();


    def get_axis_index(self, index_dynamic):
        return self.separate[index_dynamic];


    def __get_canonical_separate(self):
        if (isinstance(self.separate, list)):
            separate = [0] * len(self.dynamics[0]);
            for canvas_index in range(len(self.separate)):
                dynamic_indexes = self.separate[canvas_index];
                for dynamic_index in dynamic_indexes:
                    separate[dynamic_index] = canvas_index;
            
            return separate;
        
        elif (self.separate is False):
            if (isinstance(self.dynamics[0], list) is True):
                return [ self.canvas ] * len(self.dynamics[0]);
            else:
                return [ self.canvas ];
        
        elif (self.separate is True):
            if (isinstance(self.dynamics[0], list) is True):
                return range(self.canvas, self.canvas + len(self.dynamics[0]));
            else:
                return [ self.canvas ];

        else:
            raise Exception("Incorrect type of argument 'separate' '%s'." % type(self.separate));


class dynamic_visualizer:
    def __init__(self, canvas, x_title=None, y_title=None, x_lim=None, y_lim=None, x_labels=True, y_labels=True):
        self.__size = canvas;
        self.__canvases = [ canvas_descr(x_title, y_title, x_lim, y_lim, x_labels, y_labels) for _ in range(canvas) ];
        self.__dynamic_storage = [];


    def set_canvas_properties(self, canvas, x_title=None, y_title=None, x_lim=None, y_lim=None, x_labels=True, y_labels=True):
        self.__canvases[canvas] = canvas_descr(x_title, y_title, x_lim, y_lim, x_labels, y_labels);


    def append_dynamic(self, t, dynamic, canvas=0, color='blue'):
        description = dynamic_descr(canvas, t, dynamic, False, color);
        self.__dynamic_storage.append(description);
        self.__update_canvas_xlim(description.time, description.separate);


    def append_dynamics(self, t, dynamics, canvas=0, separate=False, color='blue'):
        description = dynamic_descr(canvas, t, dynamics, separate, color);
        self.__dynamic_storage.append(description);
        self.__update_canvas_xlim(description.time, description.separate);


    def show(self):
        (_, axis) = plt.subplots(self.__size, 1);
        
        self.__format_canvases(axis);
        
        for dynamic in self.__dynamic_storage:
            self.__display_dynamic(axis, dynamic);
        
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