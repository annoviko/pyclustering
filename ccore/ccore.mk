# GCC should support C++1y
# CCORE PyClustering project

include makefile.include

CC = g++
LD = g++

# Toolchain arguments.
CFLAGS = -O3 -MMD -MP -std=c++1y -fPIC -c 
LFLAGS = -O3 -static-libstdc++ -std=c++1y -shared

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

