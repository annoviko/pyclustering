"""!

@brief Segmentation example of Hodgkin-Huxley oscillatory network for image segmentation.

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


from pyclustering.cluster.dbscan import dbscan;

from pyclustering.nnet.dynamic_visualizer import dynamic_visualizer;
from pyclustering.nnet.hhn import hhn_network;

from pyclustering.samples.definitions import IMAGE_SIMPLE_SAMPLES;

from pyclustering.utils import read_image, rgb2gray, draw_image_mask_segments;


def template_image_segmentation(image_file, steps, time):
    image = read_image(image_file);
    stimulus = rgb2gray(image);

    stimulus = [255.0 - pixel for pixel in stimulus];
    divider = max(stimulus) / 70.0;
    stimulus = [int(pixel / divider) for pixel in stimulus];

    net = hhn_network(len(stimulus), stimulus, None, ccore=True);

    (t, dyn_peripheral, dyn_central) = net.simulate(steps, time);

    #draw_image_mask_segments(image_file, ensembles);

    # just for checking correctness of results - let's use classical algorithm
    dbscan_instance = dbscan(image, 3, 4, True);
    dbscan_instance.process();
    trustable_clusters = dbscan_instance.get_clusters();

    amount_canvases = len(trustable_clusters) + 2;
    visualizer = dynamic_visualizer(amount_canvases, x_title = "Time", y_title = "V", y_labels = False);
    visualizer.append_dynamics(t, dyn_peripheral, 0, trustable_clusters);
    visualizer.append_dynamics(t, dyn_central, amount_canvases - 2, True);
    visualizer.show();


def segmentation_image_simple1():
    template_image_segmentation(IMAGE_SIMPLE_SAMPLES.IMAGE_SIMPLE01, 25000, 1200);


segmentation_image_simple1();