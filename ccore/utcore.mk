# GCC should support C++1y
# Unit-test project for CCORE PyClustering

# Include all sources of CCORE pyclustering library
include makefile.include

CC = g++
LD = g++

# Toolchain arguments.
CFLAGS = -O3 -MMD -MP -std=gnu++1y -fPIC -c
LDFLAGS = -O3 -std=gnu++1y -pthread

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

rebuild: clean utcore

$(EXECUTABLE): $(OBJECTS)
	$(LD) $(OBJECTS) $(LDFLAGS) -o $(EXECUTABLE)

.cpp.o:
	$(CC) $(CFLAGS) $(INCLUDES) $< -o $@

# Let make read the dependency files and handle them.
-include $(DEPS)

