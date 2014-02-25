CXX=g++
CXXFLAGS=-O3
OUTPUTFILE=dbscan.exe

INCLUDE_PATH=-Iinc/
SOURCE_PATH=src/
BINARY_PATH=../bin/

.DBSCAN: all
all: $(OUTPUTFILE)

$(OUTPUTFILE): $(SOURCE_PATH)dbscan.cpp
	@$(CXX) $^ $(INCLUDE_PATH) -o $@
	@echo $(OUTPUTFILE) has been built successfully
	@mv $(OUTPUTFILE) $(BINARY_PATH)
	@echo $(OUTPUTFILE) has been moved to $(BINARY_PATH)
	
.DBSCAN: clean
clean:	
	@rm -f $(BINARY_PATH)/$(OUTPUTFILE)
	@echo $(OUTPUTFILE) has been removed from $(BINARY_PATH)