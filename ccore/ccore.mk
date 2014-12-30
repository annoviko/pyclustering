# GCC should support C++11, for example, GCC 4.7.2
# CCORE PyClustering project

include makefile.include

CC = g++
CFLAGS = -std=gnu++0x -fPIC -c 
LFLAGS = -std=gnu++0x -shared

OBJECTS = $(SOURCES:.cpp=.o)

EXECUTABLE = ../pyclustering/core/x64/linux/ccore.so

ccore: $(EXECUTABLE)

$(EXECUTABLE): $(OBJECTS)
	$(CC) $(LFLAGS) $(OBJECTS) $(INCLUDES) -o $@

.cpp.o:
	$(CC) $(CFLAGS) $(INCLUDES) $< -o $@

clean:
	rm -rf ccore/*o ccore.so

