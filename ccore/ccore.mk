#
# @authors Andrei Novikov (pyclustering@yandex.ru)
# @date 2014-2019
# @copyright GNU Public License
#
# GNU_PUBLIC_LICENSE
#   pyclustering is free software: you can redistribute it and/or modify
#   it under the terms of the GNU General Public License as published by
#   the Free Software Foundation, either version 3 of the License, or
#   (at your option) any later version.
#
#   pyclustering is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.
#
#   You should have received a copy of the GNU General Public License
#   along with this program.  If not, see <http://www.gnu.org/licenses/>.
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
		CFLAG_PLATFORM = 
		LFLAG_PLATFORM = 
	endif
endif


# Warnings
WARNING_FLAGS = -Wall -Wpedantic


# Toolchain arguments
CFLAGS = -O2 -MMD -MP -std=$(CPLUS_STANDARD) $(CFLAG_PIC) $(CFLAG_PLATFORM) $(WARNING_FLAGS)
LFLAGS = -shared $(LFLAG_PLATFORM)


# Shared library file
SHARED_LIB_DIRECTORY = ../pyclustering/core/$(PLATFORM)/$(OSNAME)
SHARED_LIB = $(SHARED_LIB_DIRECTORY)/ccore.so


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


# Project objects
OBJECTS_DIRECTORY = obj/ccore/$(PLATFORM)
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
ccore: mkdirs $(SHARED_LIB)


.PHONY: ccore_static
ccore_static: mkdirs $(STATIC_LIB)


.PHONY: mkdirs
mkdirs: $(OBJECTS_DIRECTORIES)


.PHONY:
clean:
	$(RM) $(OBJECTS_DIRECTORY) $(SHARED_LIB) $(STATIC_LIB)


# Build targets
$(SHARED_LIB): $(OBJECTS)
	$(LD) $(LFLAGS) $^ -o $@


$(STATIC_LIB): $(OBJECTS)
	$(AR) $@ $^


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

