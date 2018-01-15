# Tools
CC = g++ -c
LD = g++
RM = rm -rf
MKDIR = mkdir -p


# C++ standard depending on operating system
ifeq ($(shell uname -o), Cygwin)
	CPLUS_STANDARD = gnu++14
	CFLAG_PIC = 
else
	CPLUS_STANDARD = c++14
	CFLAG_PIC = -fPIC
endif


# Target flag depending on platform
ifeq ($(PLATFORM), x86)
	CFLAG_PLATFORM = -m32
	LFLAG_PLATFORM = -m32
else
	CFLAG_PLATFORM = -m64
	LFLAG_PLATFORM = -m64
endif


# Warnings.
WARNING_FLAGS = -Wall -Wpedantic


# Toolchain arguments.
CFLAGS = -O2 -MMD -MP -std=$(CPLUS_STANDARD) $(CFLAG_PIC) $(CFLAG_PLATFORM) $(WARNING_FLAGS)
LFLAGS = -shared $(LFLAG_PLATFORM)


# Executable library file
EXECUTABLE_DIRECTORY = ../pyclustering/core/$(PLATFORM)/linux
EXECUTABLE = $(EXECUTABLE_DIRECTORY)/ccore.so


# Project sources
MODULES = . cluster container differential interface nnet parallel utils

SOURCES_DIRECTORY = src
SOURCES_DIRECTORIES = $(addprefix $(SOURCES_DIRECTORY)/, $(MODULES))
SOURCES = $(foreach SUBDIR, $(SOURCES_DIRECTORIES), $(wildcard $(SUBDIR)/*.cpp))

INCLUDES = -I$(SOURCES_DIRECTORY)


# Project objects
OBJECTS_DIRECTORY = obj/ccore/$(PLATFORM)
OBJECTS_DIRECTORIES = $(addprefix $(OBJECTS_DIRECTORY)/, $(MODULES)) $(EXECUTABLE_DIRECTORY)
OBJECTS = $(patsubst $(SOURCES_DIRECTORY)/%.cpp, $(OBJECTS_DIRECTORY)/%.o, $(SOURCES))


# Dependencies
DEPENDENCIES = $(OBJECTS:.o=.d)


# Targets
.PHONY: cppcheck
cppcheck:
	cppcheck --error-exitcode=1 --inconclusive --enable=warning,style,performance,information,portability --include=$(SOURCES_DIRECTORY) $(SOURCES_DIRECTORY)


.PHONY: ccore
ccore: mkdirs $(EXECUTABLE)


.PHONY: mkdirs
mkdirs: $(OBJECTS_DIRECTORIES)


.PHONY:
clean:
	$(RM) $(OBJECTS_DIRECTORY) $(EXECUTABLE)


# Build targets
$(EXECUTABLE): $(OBJECTS)
	$(LD) $(LFLAGS) $^ -o $@


$(OBJECTS_DIRECTORIES):
	$(MKDIR) $@


vpath %.cpp $(SOURCES_DIRECTORIES)


define make-objects
$1/%.o: %.cpp
	$(CC) $(CFLAGS) $(INCLUDES) $$< -o $$@
endef


$(foreach OBJDIR, $(OBJECTS_DIRECTORIES), $(eval $(call make-objects, $(OBJDIR))))


# Include dependencies
-include $(DEPENDENCIES)

