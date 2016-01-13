# GCC should support C++11, for example, GCC 4.7.2

MAKE = make
MKFLAG = -f

ccore:  core

core:
	$(MAKE) $(MKFLAG) ccore.mk

utcore: ut

ut:
	$(MAKE) $(MKFLAG) utcore.mk


clean:
	rm -rf ccore/*.o ccore/*.d ../pyclustering/core/x64/linux/ccore.so
	rm -rf utcore/*.o utcore/*.d utcore/utcore

