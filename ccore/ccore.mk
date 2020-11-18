#
# @authors Andrei Novikov (pyclustering@yandex.ru)
# @date 2014-2020
# @copyright BSD-3-Clause
#


# Tools
RM = rm -rf
MKDIR = mkdir -p
AR = ar rcs


# C++ standard depending on operating system
UNAME = $(shell uname -s | tr '[:upper:]' '[:lower:]')
ifeq ($(findstring cygwin, $(UNAME)), cygwin)
	OSNAME = win
	CPLUS_STANDARD = gnu++14
	CFLAG_PIC = 
else
	ifeq ($(UNAME), darwin)
		OSNAME = macos
	else
		OSNAME = linux
	endif

	CPLUS_STANDARD = c++14
	CFLAG_PIC = -fPIC
endif


# Compiler (g++ compiler is used by default)
ifeq ($(COMPILER), clang)
	CC = scan-build clang++ -c
	LD = scan-build clang++
else
	CC = g++ -c
	LD = g++
endif


# Target flag depending on platform
ifeq ($(PLATFORM), 32-bit)
	CFLAG_PLATFORM = -m32
	LFLAG_PLATFORM = -m32
else 
	ifeq ($(PLATFORM), 64-bit)
		CFLAG_PLATFORM = -m64
		LFLAG_PLATFORM = -m64
	else
		PLATFORM = 64-bit
		CFLAG_PLATFORM = -m64
		LFLAG_PLATFORM = -m64
	endif
endif


# Definitions
DEFINITION_FLAGS =


# Warnings
WARNING_FLAGS = -Wall -Wpedantic


# Shared library file
SHARED_LIB_DEPLOY_DIRECTORY = ../pyclustering/core/$(PLATFORM)/$(OSNAME)
SHARED_LIB_DIRECTORY = .
SHARED_LIB = $(SHARED_LIB_DIRECTORY)/libpyclustering.so


# Static library file
STATIC_LIB_DIRECTORY = .
STATIC_LIB = libpyclustering.a


# Project sources
MODULES = . cluster container differential interface nnet parallel utils

PROJECT_DIRECTORY = .
INCLUDE_DIRECTORY = $(PROJECT_DIRECTORY)/include/
SOURCES_DIRECTORY = src
SOURCES_DIRECTORIES = $(addprefix $(SOURCES_DIRECTORY)/, $(MODULES))
SOURCES = $(foreach SUBDIR, $(SOURCES_DIRECTORIES), $(wildcard $(SUBDIR)/*.cpp))

INCLUDES = -I$(INCLUDE_DIRECTORY)

LIBRARIES =


# Toolchain arguments
CFLAGS = -O2 -MMD -MP -pthread -std=$(CPLUS_STANDARD) $(CFLAG_PIC) $(CFLAG_PLATFORM) $(WARNING_FLAGS) $(DEFINITION_FLAGS)
LFLAGS = -shared -pthread $(LFLAG_PLATFORM) $(LIBRARIES)


# Project objects
OBJECTS_ROOT = obj
OBJECTS_DIRECTORY = $(OBJECTS_ROOT)/ccore/$(PLATFORM)
OBJECTS_DIRECTORIES = $(addprefix $(OBJECTS_DIRECTORY)/, $(MODULES)) $(SHARED_LIB_DIRECTORY)
OBJECTS = $(patsubst $(SOURCES_DIRECTORY)/%.cpp, $(OBJECTS_DIRECTORY)/%.o, $(SOURCES))


# Dependencies
DEPENDENCIES = $(OBJECTS:.o=.d)


# Targets
.PHONY: cppcheck
cppcheck:
	cppcheck --version
	cppcheck --inline-suppr --error-exitcode=1 --std=c++14 --inconclusive --enable=warning,style,performance,information,portability -I $(INCLUDE_DIRECTORY) $(SOURCES_DIRECTORY)


.PHONY: ccore
ccore: shared_library_definitions mkdirs $(SHARED_LIB) deploy


.PHONY: shared_library_definitions
shared_library_definitions:
	$(eval DEFINITION_FLAGS := -DEXPORT_PYCLUSTERING_INTERFACE)


.PHONY: ccore_static
ccore_static: mkdirs $(STATIC_LIB)


.PHONY: mkdirs
mkdirs: $(OBJECTS_DIRECTORIES)

.PHONY: deploy
deploy: $(SHARED_LIB)
	echo "Copy C++ shared library to Python pyclustering."
	cp $(SHARED_LIB) $(SHARED_LIB_DEPLOY_DIRECTORY)

$(OBJECTS_DIRECTORIES):
	$(MKDIR) $@


.PHONY:
clean:
	$(RM) $(OBJECTS_DIRECTORY) $(SHARED_LIB) $(STATIC_LIB)


# Build targets
$(SHARED_LIB): $(OBJECTS)
	$(LD) $(LFLAGS) $^ -o $@


$(STATIC_LIB): $(OBJECTS)
	$(AR) $@ $^


$(OBJECTS_DIRECTORY)/%.o: $(SOURCES_DIRECTORY)/%.cpp
	$(CC) $(CFLAGS) $(INCLUDES) $(LIBRARIES) $< -o $@


# Include dependencies
-include $(DEPENDENCIES)
