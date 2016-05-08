# CCORE PyClustering library project

include makefile.include

CC = g++
LD = g++

# Toolchain arguments.
CFLAGS = -O3 -MMD -MP -std=c++1y -fPIC -c 
LFLAGS = -O3 -static-libstdc++ -shared

# Project sources
OBJECTS = $(SOURCES:.cpp=.o)

# The dependency file names
DEPS = $(OBJECTS:.o=.d)

# Executable library file
EXECUTABLE = ../pyclustering/core/x64/linux/ccore.so


ccore: $(EXECUTABLE)


clean:
	rm -rf ccore/*o ccore.so


$(EXECUTABLE): $(OBJECTS)
	$(LD) $(LFLAGS) $(OBJECTS) $(INCLUDES) -o $@


.cpp.o:
	$(CC) $(CFLAGS) $(INCLUDES) $< -o $@


-include $(DEPS)

