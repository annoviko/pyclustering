################################################################################
# Automatically-generated file. Do not edit!
################################################################################

# Add inputs and outputs from these tool invocations to the build variables 
CPP_SRCS += \
../ccore/ccore.cpp \
../ccore/cure.cpp \
../ccore/dbscan.cpp \
../ccore/hierarchical.cpp \
../ccore/hsyncnet.cpp \
../ccore/kdtree.cpp \
../ccore/kmeans.cpp \
../ccore/legion.cpp \
../ccore/network.cpp \
../ccore/pcnn.cpp \
../ccore/rock.cpp \
../ccore/som.cpp \
../ccore/support.cpp \
../ccore/sync.cpp \
../ccore/syncnet.cpp \
../ccore/syncpr.cpp \
../ccore/xmeans.cpp 

OBJS += \
./ccore/ccore.o \
./ccore/cure.o \
./ccore/dbscan.o \
./ccore/hierarchical.o \
./ccore/hsyncnet.o \
./ccore/kdtree.o \
./ccore/kmeans.o \
./ccore/legion.o \
./ccore/network.o \
./ccore/pcnn.o \
./ccore/rock.o \
./ccore/som.o \
./ccore/support.o \
./ccore/sync.o \
./ccore/syncnet.o \
./ccore/syncpr.o \
./ccore/xmeans.o 

CPP_DEPS += \
./ccore/ccore.d \
./ccore/cure.d \
./ccore/dbscan.d \
./ccore/hierarchical.d \
./ccore/hsyncnet.d \
./ccore/kdtree.d \
./ccore/kmeans.d \
./ccore/legion.d \
./ccore/network.d \
./ccore/pcnn.d \
./ccore/rock.d \
./ccore/som.d \
./ccore/support.d \
./ccore/sync.d \
./ccore/syncnet.d \
./ccore/syncpr.d \
./ccore/xmeans.d 


# Each subdirectory must supply rules for building sources it contributes
ccore/%.o: ../ccore/%.cpp
	@echo 'Building file: $<'
	@echo 'Invoking: GCC C++ Compiler'
	g++ -std=c++0x -fPIC -I"/home/andrei/workspace/pyclustering/ccore" -I"/home/andrei/workspace/pyclustering/ccore/tools" -O0 -g3 -Wall -c -fmessage-length=0 -MMD -MP -MF"$(@:%.o=%.d)" -MT"$(@:%.o=%.d)" -o "$@" "$<"
	@echo 'Finished building: $<'
	@echo ' '


