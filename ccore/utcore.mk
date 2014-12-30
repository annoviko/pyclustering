# GCC should support C++11, for example, GCC 4.7.2
# Unit-test project for CCORE PyClustering

CC = g++
CFLAGS = -std=gnu++0x -fPIC -c -isystem tools/
LFLAGS = -std=gnu++0x -pthread tools/gtest/lib/linux/libgtest.a

include makefile.include

INCLUDES += -I./ -Iutcore/ -Itools/

SOURCES += utcore/main.cpp

OBJECTS = $(SOURCES:.cpp=.o)

EXECUTABLE = utcore/utcore

utcore: $(EXECUTABLE)
	./utcore/utcore

$(EXECUTABLE): $(OBJECTS)
	$(CC) $(OBJECTS) $(LFLAGS) -o $(EXECUTABLE)

.cpp.o:
	$(CC) $(CFLAGS) $(INCLUDES) $< -o $@


