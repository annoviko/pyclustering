# GCC should support C++11, for example, GCC 4.7.2
CC = g++
CFLAGS = -fPIC -std=gnu++0x -c
INCLUDE = -I./

all: ccore.so

ccore.so: ccore.o dbscan.o hierarchical.o kmeans.o network.o rock.o support.o sync_network.o
	$(CC) -std=gnu++0x -fPIC -shared ccore.o dbscan.o hierarchical.o kmeans.o network.o rock.o support.o sync_network.o -o ccore.so

ccore.o: ccore.cpp
	$(CC) $(CFLAGS) $(INCLUDE) ccore.cpp

dbscan.o: dbscan.cpp
	$(CC) $(CFLAGS) $(INCLUDE) dbscan.cpp

hierarchical.o: hierarchical.cpp
	$(CC) $(CFLAGS) $(INCLUDE) hierarchical.cpp

kmeans.o: kmeans.cpp
	$(CC) $(CFLAGS) $(INCLUDE) kmeans.cpp

network.o: network.cpp
	$(CC) $(CFLAGS) $(INCLUDE) network.cpp

rock.o: rock.cpp
	$(CC) $(CFLAGS) $(INCLUDE) rock.cpp
	
support.o: support.cpp
	$(CC) $(CFLAGS) $(INCLUDE) support.cpp

sync_network.o: sync_network.cpp
	$(CC) $(CFLAGS) $(INCLUDE) sync_network.cpp
	
clean:
	rm -rf *o ccore.so