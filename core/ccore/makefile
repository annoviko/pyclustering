# GCC should support C++11, for example, GCC 4.7.2
CC = g++
CFLAGS = -std=gnu++0x -fPIC -c 
LFLAGS = -std=gnu++0x -shared

INCLUDES = -Iccore/

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

OBJECTS = $(SOURCES:.cpp=.o)

EXECUTABLE = x64/linux/ccore.so

ccore: $(EXECUTABLE)

$(EXECUTABLE): $(OBJECTS)
	$(CC) $(LFLAGS) $(OBJECTS) $(INCLUDES) -o $@

.cpp.o:
	$(CC) $(CFLAGS) $(INCLUDES) $< -o $@

clean:
	rm -rf ccore/*o ccore.so
