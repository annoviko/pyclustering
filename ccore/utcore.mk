# Unit-test project for CCORE PyClustering library

include makefile.include

CC = g++
LD = g++

# Toolchain arguments
ifeq ($(ARGS), valgrind)
	CFLAGS = -MMD -MP -std=c++1y -fPIC -g -c
	LFLAGS = -pthread
else
	CFLAGS = -O3 -MMD -MP -std=c++1y -fPIC -fprofile-arcs -ftest-coverage -c
	LFLAGS = -O3 -pthread -fprofile-arcs -ftest-coverage
endif


# Project sources
SOURCES += tst/main.cpp
SOURCES += tst/samples.cpp
SOURCES += tst/utest-cluster.cpp
SOURCES += tools/gtest/gtest-all.cpp

OBJECTS = $(SOURCES:.cpp=.o)

INCLUDES += -I./ -Itst/ -Itools/


# The dependency file names
DEPS = $(OBJECTS:.o=.d)


# Output name of executable file
EXECUTABLE = tst/utcore.exe


utcore: $(EXECUTABLE)


clean:
	rm utcore/*.o tst/utcore.exe


$(EXECUTABLE): $(OBJECTS)
	$(LD) $(OBJECTS) $(LFLAGS) -o $(EXECUTABLE)


.cpp.o:
	$(CC) $(CFLAGS) $(INCLUDES) $< -o $@


-include $(DEPS)

