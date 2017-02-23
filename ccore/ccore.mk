# Tools
CC = g++ -c
LD = g++
RM = rm -rf
MKDIR = mkdir -p


# Toolchain arguments.
CFLAGS = -O3 -MMD -MP -std=c++1y -fPIC
LFLAGS = -static-libstdc++ -shared


# Project sources
MODULES = cluster container differential interface nnet tsp

SOURCES_DIRECTORY = src
SOURCES_DIRECTORIES = $(addprefix $(SOURCES_DIRECTORY)/, $(MODULES))
SOURCES = $(foreach SUBDIR, $(SOURCES_DIRECTORIES), $(wildcard $(SUBDIR)/*.cpp))

INCLUDES = -I$(SOURCES_DIRECTORY)


# Project objects
OBJECTS = $(SOURCES:.cpp=.o)


# The dependency file names
DEPS = $(OBJECTS:.o=.d)


# Executable library file
EXECUTABLE = ../pyclustering/core/x64/linux/ccore.so


.PHONY: ccore
ccore: $(EXECUTABLE)


.PHONY:
clean:
	$(RM) ccore/*o ccore.so


$(EXECUTABLE): $(OBJECTS)
	$(LD) $(LFLAGS) $(OBJECTS) $(INCLUDES) -o $@


.cpp.o:
	$(CC) $(CFLAGS) $(INCLUDES) $< -o $@


-include $(DEPS)

