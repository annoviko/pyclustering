# Unit-test project for CCORE PyClustering library

include makefile.include

CC = g++
LD = g++

# Toolchain arguments
CFLAGS = -O3 -MMD -MP -std=c++1y -fPIC -fprofile-arcs -ftest-coverage -c
LFLAGS = -O3 -pthread -fprofile-arcs -ftest-coverage


# Project sources
SOURCES += utcore/main.cpp
SOURCES += utcore/samples.cpp
SOURCES += tools/gtest/gtest-all.cpp

OBJECTS = $(SOURCES:.cpp=.o)

INCLUDES += -I./ -Iutcore/ -Itools/


# The dependency file names
DEPS = $(OBJECTS:.o=.d)


# Output name of executable file
EXECUTABLE = utcore/utcore.exe


utcore: $(EXECUTABLE)


clean:
	rm utcore/*.o utcore/utcore


$(EXECUTABLE): $(OBJECTS)
	$(LD) $(OBJECTS) $(LFLAGS) -o $(EXECUTABLE)


.cpp.o:
	$(CC) $(CFLAGS) $(INCLUDES) $< -o $@


-include $(DEPS)

