# GCC should support C++11, for example, GCC 4.7.2
# CCORE PyClustering project

include makefile.include

CC = g++
LD = g++

# Toolchain arguments.
CFLAGS = -MMD -MP -std=gnu++0x -fPIC -c 
LFLAGS = -static-libstdc++ -std=gnu++0x -shared

# Project sources
OBJECTS = $(SOURCES:.cpp=.o)

# The dependency file names
DEPS = $(OBJECTS:.o=.d)

EXECUTABLE = ../pyclustering/core/x64/linux/ccore.so

ccore: $(EXECUTABLE)

clean:
	rm -rf ccore/*o ccore.so

rebuild: clean ccore

$(EXECUTABLE): $(OBJECTS)
	$(LD) $(LFLAGS) $(OBJECTS) $(INCLUDES) -o $@

.cpp.o:
	$(CC) $(CFLAGS) $(INCLUDES) $< -o $@

# Let make read the dependency files and handle them.
-include $(DEPS)

