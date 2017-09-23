"""!

@brief General definitions of samples.

@authors Andrei Novikov (pyclustering@yandex.ru)
@date 2014-2017
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

import pyclustering.samples as samples;
import os;


DEFAULT_SAMPLE_PATH = samples.__path__[0] + os.sep + "samples" + os.sep;


class SIMPLE_SAMPLES:
    SAMPLE_SIMPLE1          = DEFAULT_SAMPLE_PATH + "SampleSimple01.txt";
    SAMPLE_SIMPLE2          = DEFAULT_SAMPLE_PATH + "SampleSimple02.txt";
    SAMPLE_SIMPLE3          = DEFAULT_SAMPLE_PATH + "SampleSimple03.txt";
    SAMPLE_SIMPLE4          = DEFAULT_SAMPLE_PATH + "SampleSimple04.txt";
    SAMPLE_SIMPLE5          = DEFAULT_SAMPLE_PATH + "SampleSimple05.txt";
    SAMPLE_SIMPLE6          = DEFAULT_SAMPLE_PATH + "SampleSimple06.txt";
    SAMPLE_SIMPLE7          = DEFAULT_SAMPLE_PATH + "SampleSimple07.txt";
    SAMPLE_SIMPLE8          = DEFAULT_SAMPLE_PATH + "SampleSimple08.txt";
    SAMPLE_SIMPLE9          = DEFAULT_SAMPLE_PATH + "SampleSimple09.txt";
    SAMPLE_SIMPLE10         = DEFAULT_SAMPLE_PATH + "SampleSimple10.txt";
    SAMPLE_SIMPLE11         = DEFAULT_SAMPLE_PATH + "SampleSimple11.txt";
    SAMPLE_SIMPLE12         = DEFAULT_SAMPLE_PATH + "SampleSimple12.txt";
    SAMPLE_ELONGATE         = DEFAULT_SAMPLE_PATH + "SampleElongate.txt";
    SAMPLE_DENSITIES1       = DEFAULT_SAMPLE_PATH + "SampleDensities1.txt";
    SAMPLE_DENSITIES2       = DEFAULT_SAMPLE_PATH + "SampleDensities2.txt";


class FCPS_SAMPLES:
    SAMPLE_ATOM             = DEFAULT_SAMPLE_PATH + "SampleAtom.txt";
    SAMPLE_CHAINLINK        = DEFAULT_SAMPLE_PATH + "SampleChainlink.txt";
    SAMPLE_ENGY_TIME        = DEFAULT_SAMPLE_PATH + "SampleEngyTime.txt";
    SAMPLE_GOLF_BALL        = DEFAULT_SAMPLE_PATH + "SampleGolfBall.txt";
    SAMPLE_HEPTA            = DEFAULT_SAMPLE_PATH + "SampleHepta.txt";
    SAMPLE_LSUN             = DEFAULT_SAMPLE_PATH + "SampleLsun.txt";
    SAMPLE_TARGET           = DEFAULT_SAMPLE_PATH + "SampleTarget.txt";
    SAMPLE_TETRA            = DEFAULT_SAMPLE_PATH + "SampleTetra.txt";
    SAMPLE_TWO_DIAMONDS     = DEFAULT_SAMPLE_PATH + "SampleTwoDiamonds.txt";
    SAMPLE_WING_NUT         = DEFAULT_SAMPLE_PATH + "SampleWingNut.txt";


class COMMON_SAMPLES:
    SAMPLE_OLD_FAITHFUL     = DEFAULT_SAMPLE_PATH + "SampleOldFaithful.txt";


class GRAPH_SIMPLE_SAMPLES:
    GRAPH_BROKEN_CIRCLE1            = samples.__path__[0] + os.sep + "graphs" + os.sep + "GraphBrokenCircle1.grpr";
    GRAPH_BROKEN_CIRCLE2            = samples.__path__[0] + os.sep + "graphs" + os.sep + "GraphBrokenCircle2.grpr";
    GRAPH_FIVE_POINTED_FRAME_STAR   = samples.__path__[0] + os.sep + "graphs" + os.sep + "GraphFivePointedFrameStar.grpr";
    GRAPH_FIVE_POINTED_STAR         = samples.__path__[0] + os.sep + "graphs" + os.sep + "GraphFivePointedStar.grpr";
    GRAPH_ONE_CIRCLE1               = samples.__path__[0] + os.sep + "graphs" + os.sep + "GraphOneCircle1.grpr";
    GRAPH_ONE_CIRCLE2               = samples.__path__[0] + os.sep + "graphs" + os.sep + "GraphOneCircle2.grpr";
    GRAPH_ONE_CIRCLE3               = samples.__path__[0] + os.sep + "graphs" + os.sep + "GraphOneCircle3.grpr";
    GRAPH_ONE_CROSSROAD             = samples.__path__[0] + os.sep + "graphs" + os.sep + "GraphOneCrossroad.grpr";
    GRAPH_ONE_LINE                  = samples.__path__[0] + os.sep + "graphs" + os.sep + "GraphOneLine.grpr";
    GRAPH_TWO_CROSSROADS            = samples.__path__[0] + os.sep + "graphs" + os.sep + "GraphTwoCrossroads.grpr";
    GRAPH_FULL1                     = samples.__path__[0] + os.sep + "graphs" + os.sep + "GraphFull1.grpr"
    GRAPH_FULL2                     = samples.__path__[0] + os.sep + "graphs" + os.sep + "GraphFull2.grpr"
    GRAPH_SIMPLE1                   = samples.__path__[0] + os.sep + "graphs" + os.sep + "GraphSimple1.grpr"
    GRAPH_SIMPLE2                   = samples.__path__[0] + os.sep + "graphs" + os.sep + "GraphSimple2.grpr"
    GRAPH_SIMPLE3                   = samples.__path__[0] + os.sep + "graphs" + os.sep + "GraphSimple3.grpr"


class IMAGE_SIMPLE_SAMPLES:
    IMAGE_SIMPLE01                  = samples.__path__[0] + os.sep + "images" + os.sep + "ImageSimple01.png";
    IMAGE_SIMPLE02                  = samples.__path__[0] + os.sep + "images" + os.sep + "ImageSimple02.png";
    IMAGE_SIMPLE03                  = samples.__path__[0] + os.sep + "images" + os.sep + "ImageSimple03.png";
    IMAGE_SIMPLE04                  = samples.__path__[0] + os.sep + "images" + os.sep + "ImageSimple04.png";
    IMAGE_SIMPLE05                  = samples.__path__[0] + os.sep + "images" + os.sep + "ImageSimple05.png";
    IMAGE_SIMPLE06                  = samples.__path__[0] + os.sep + "images" + os.sep + "ImageSimple06.png";
    IMAGE_SIMPLE07                  = samples.__path__[0] + os.sep + "images" + os.sep + "ImageSimple07.png";
    IMAGE_SIMPLE08                  = samples.__path__[0] + os.sep + "images" + os.sep + "ImageSimple08.png";
    IMAGE_SIMPLE09                  = samples.__path__[0] + os.sep + "images" + os.sep + "ImageSimple09.png";
    IMAGE_SIMPLE10                  = samples.__path__[0] + os.sep + "images" + os.sep + "ImageSimple10.png";
    IMAGE_SIMPLE11                  = samples.__path__[0] + os.sep + "images" + os.sep + "ImageSimple11.png";
    IMAGE_SIMPLE12                  = samples.__path__[0] + os.sep + "images" + os.sep + "ImageSimple12.png";
    IMAGE_SIMPLE13                  = samples.__path__[0] + os.sep + "images" + os.sep + "ImageSimple13.png";
    IMAGE_SIMPLE14                  = samples.__path__[0] + os.sep + "images" + os.sep + "ImageSimple14.png";
    IMAGE_SIMPLE15                  = samples.__path__[0] + os.sep + "images" + os.sep + "ImageSimple15.png";
    IMAGE_SIMPLE16                  = samples.__path__[0] + os.sep + "images" + os.sep + "ImageSimple16.png";
    IMAGE_SIMPLE_BEACH              = samples.__path__[0] + os.sep + "images" + os.sep + "ImageSimpleBeach.png";
    IMAGE_SIMPLE_BUILDING           = samples.__path__[0] + os.sep + "images" + os.sep + "ImageSimpleBuilding.png";
    IMAGE_SIMPLE_FRUITS             = samples.__path__[0] + os.sep + "images" + os.sep + "ImageSimpleFruits.png";
    IMAGE_SIMPLE_FRUITS_SMALL       = samples.__path__[0] + os.sep + "images" + os.sep + "ImageSimpleFruitsSmall.png";
    IMAGE_THIN_BLACK_LINES01        = samples.__path__[0] + os.sep + "images" + os.sep + "ImageThinBlackLines01.png";
    IMAGE_THIN_BLACK_LINES02        = samples.__path__[0] + os.sep + "images" + os.sep + "ImageThinBlackLines02.png";
    IMAGE_THIN_BLACK_LINES03        = samples.__path__[0] + os.sep + "images" + os.sep + "ImageThinBlackLines03.png";
    
    
class IMAGE_MAP_SAMPLES:
    IMAGE_WHITE_SEA                 = samples.__path__[0] + os.sep + "images" + os.sep + "ImageWhiteSea.png";
    IMAGE_WHITE_SEA_SMALL           = samples.__path__[0] + os.sep + "images" + os.sep + "ImageWhiteSeaSmall.png";
    IMAGE_NILE                      = samples.__path__[0] + os.sep + "images" + os.sep + "ImageNile.png";
    IMAGE_NILE_SMALL                = samples.__path__[0] + os.sep + "images" + os.sep + "ImageNileSmall.png";
    IMAGE_BUILDINGS                 = samples.__path__[0] + os.sep + "images" + os.sep + "ImageBuildings.png";
    

class IMAGE_REAL_SAMPLES:
    IMAGE_FIELD_FLOWER              = samples.__path__[0] + os.sep + "images" + os.sep + "ImageFieldFlower.png";
    IMAGE_FIELD_TREE                = samples.__path__[0] + os.sep + "images" + os.sep + "ImageFieldTree.png";
    

class IMAGE_SYMBOL_SAMPLES:
    @staticmethod
    def GET_LIST_IMAGE_SAMPLES(symbol):
        default_path = samples.__path__[0] + os.sep + "images" + os.sep + "symbols" + os.sep;
        number_sample_symbols = 1;
        
        name_file_pattern = "Symbol_%s_Sample%.2d.png";
        list_image_samples = [];
        
        for index_image in range(1, number_sample_symbols + 1, 1):
            file_path = default_path + (name_file_pattern % (symbol, index_image));
            list_image_samples.append(file_path);
            
        return list_image_samples;      

    LIST_IMAGES_SYMBOL_A            = GET_LIST_IMAGE_SAMPLES.__func__('A');
    LIST_IMAGES_SYMBOL_B            = GET_LIST_IMAGE_SAMPLES.__func__('B');
    LIST_IMAGES_SYMBOL_C            = GET_LIST_IMAGE_SAMPLES.__func__('C');
    LIST_IMAGES_SYMBOL_D            = GET_LIST_IMAGE_SAMPLES.__func__('D');
    LIST_IMAGES_SYMBOL_E            = GET_LIST_IMAGE_SAMPLES.__func__('E');
    LIST_IMAGES_SYMBOL_F            = GET_LIST_IMAGE_SAMPLES.__func__('F');
    LIST_IMAGES_SYMBOL_G            = GET_LIST_IMAGE_SAMPLES.__func__('G');
    LIST_IMAGES_SYMBOL_H            = GET_LIST_IMAGE_SAMPLES.__func__('H');
    LIST_IMAGES_SYMBOL_I            = GET_LIST_IMAGE_SAMPLES.__func__('I');
    LIST_IMAGES_SYMBOL_J            = GET_LIST_IMAGE_SAMPLES.__func__('J');
    LIST_IMAGES_SYMBOL_K            = GET_LIST_IMAGE_SAMPLES.__func__('K');
    LIST_IMAGES_SYMBOL_L            = GET_LIST_IMAGE_SAMPLES.__func__('L');
    LIST_IMAGES_SYMBOL_M            = GET_LIST_IMAGE_SAMPLES.__func__('M');
    LIST_IMAGES_SYMBOL_N            = GET_LIST_IMAGE_SAMPLES.__func__('N');
    LIST_IMAGES_SYMBOL_O            = GET_LIST_IMAGE_SAMPLES.__func__('O');
    LIST_IMAGES_SYMBOL_P            = GET_LIST_IMAGE_SAMPLES.__func__('P');
    LIST_IMAGES_SYMBOL_Q            = GET_LIST_IMAGE_SAMPLES.__func__('Q');
    LIST_IMAGES_SYMBOL_R            = GET_LIST_IMAGE_SAMPLES.__func__('R');
    LIST_IMAGES_SYMBOL_S            = GET_LIST_IMAGE_SAMPLES.__func__('S');
    LIST_IMAGES_SYMBOL_T            = GET_LIST_IMAGE_SAMPLES.__func__('T');
    LIST_IMAGES_SYMBOL_U            = GET_LIST_IMAGE_SAMPLES.__func__('U');
    LIST_IMAGES_SYMBOL_V            = GET_LIST_IMAGE_SAMPLES.__func__('V');
    LIST_IMAGES_SYMBOL_W            = GET_LIST_IMAGE_SAMPLES.__func__('W');
    LIST_IMAGES_SYMBOL_X            = GET_LIST_IMAGE_SAMPLES.__func__('X');
    LIST_IMAGES_SYMBOL_Y            = GET_LIST_IMAGE_SAMPLES.__func__('Y');
    LIST_IMAGES_SYMBOL_Z            = GET_LIST_IMAGE_SAMPLES.__func__('Z');
    
    
class IMAGE_DIGIT_SAMPLES:    
    @staticmethod
    def GET_LIST_IMAGE_SAMPLES(digit):
        default_path = samples.__path__[0] + os.sep + "images" + os.sep + "digits" + os.sep;
        number_sample_digits = 25;
        
        name_file_pattern = "Digit_%d_Sample%.2d.png";
        list_image_samples = [];
        
        for index_image in range(1, number_sample_digits + 1, 1):
            file_path = default_path + (name_file_pattern % (digit, index_image));
            list_image_samples.append(file_path);
            
        return list_image_samples;
    
    LIST_IMAGES_DIGIT_0             = GET_LIST_IMAGE_SAMPLES.__func__(0);
    LIST_IMAGES_DIGIT_1             = GET_LIST_IMAGE_SAMPLES.__func__(1);
    LIST_IMAGES_DIGIT_2             = GET_LIST_IMAGE_SAMPLES.__func__(2);
    LIST_IMAGES_DIGIT_3             = GET_LIST_IMAGE_SAMPLES.__func__(3);
    LIST_IMAGES_DIGIT_4             = GET_LIST_IMAGE_SAMPLES.__func__(4);
    LIST_IMAGES_DIGIT_5             = GET_LIST_IMAGE_SAMPLES.__func__(5);
    LIST_IMAGES_DIGIT_6             = GET_LIST_IMAGE_SAMPLES.__func__(6);
    LIST_IMAGES_DIGIT_7             = GET_LIST_IMAGE_SAMPLES.__func__(7);
    LIST_IMAGES_DIGIT_8             = GET_LIST_IMAGE_SAMPLES.__func__(8);
    LIST_IMAGES_DIGIT_9             = GET_LIST_IMAGE_SAMPLES.__func__(9);
    