################################################################################
# Automatically-generated file. Do not edit!
################################################################################

# Add inputs and outputs from these tool invocations to the build variables 
CPP_SRCS += \
../utcore/main.cpp \
../utcore/samples.cpp 

OBJS += \
./utcore/main.o \
./utcore/samples.o 

CPP_DEPS += \
./utcore/main.d \
./utcore/samples.d 


# Each subdirectory must supply rules for building sources it contributes
utcore/%.o: ../utcore/%.cpp
	@echo 'Building file: $<'
	@echo 'Invoking: GCC C++ Compiler'
	g++ -std=c++0x -fPIC -I"/home/andrei/workspace/pyclustering/ccore" -I"/home/andrei/workspace/pyclustering/ccore/tools" -O0 -g3 -Wall -c -fmessage-length=0 -MMD -MP -MF"$(@:%.o=%.d)" -MT"$(@:%.o=%.d)" -o "$@" "$<"
	@echo 'Finished building: $<'
	@echo ' '


