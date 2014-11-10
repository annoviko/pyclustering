# GCC should support C++11, for example, GCC 4.7.2
# Unit-test project for CCORE PyClustering

CC = g++
CFLAGS = -std=gnu++0x -fPIC -c -isystem tools/
LFLAGS = -std=gnu++0x

LIBS += -pthread tools/gtest/lib/linux/libgtest.a

INCLUDES = -I./ -Iutcore/ -Iccore/ -Itools/

SOURCES += ccore/ccore.cpp
SOURCES += ccore/cure.cpp
SOURCES += ccore/dbscan.cpp
SOURCES += ccore/hierarchical.cpp
SOURCES += ccore/hsyncnet.cpp
SOURCES += ccore/kdtree.cpp
SOURCES += ccore/kmeans.cpp
SOURCES += ccore/network.cpp
SOURCES += ccore/rock.cpp
SOURCES += ccore/support.cpp
SOURCES += ccore/sync_network.cpp
SOURCES += ccore/syncnet.cpp
SOURCES += ccore/xmeans.cpp

SOURCES += utcore/main.cpp

OBJECTS = $(SOURCES:.cpp=.o)

EXECUTABLE = utcore/utcore

utccore: $(EXECUTABLE)

$(EXECUTABLE): $(OBJECTS)
	$(CC) $(LFLAGS) $(OBJECTS) $(INCLUDES) -o $(EXECUTABLE)

.cpp.o:
	$(CC) $(CFLAGS) $(LIBS) $(INCLUDES) $< -o $@

clean:
	rm -rf ccore/*o ccore.so

