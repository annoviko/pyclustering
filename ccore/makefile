# GCC should support C++14

MAKE = make
MKFLAG = -f


default:
	@echo "List of targets:"
	@echo "ccore       - to build release CCORE library for pyclustering."
	@echo "utcore      - to build/run release CCORE library unit-tests."
	@echo " "
	@echo "clean       - to clean everything."


.PHONY: ccore
ccore:
	$(MAKE) $(MKFLAG) ccore.mk


.PHONY: utcore
utcore:
	$(MAKE) $(MKFLAG) utcore.mk
	
	@echo " "
	@echo "utcore is successfully created, unit-tests are started:"
	@echo " "
	
	cd utcore/ && ./utcore.exe;


.PHONY: clean
clean:
	rm -rf ccore/*.o ccore/*.d ../pyclustering/core/x64/linux/ccore.so
	rm -rf utcore/*.o utcore/*.d utcore/utcore.exe
	rm -rf ccore/ant_colony/*.[od]

