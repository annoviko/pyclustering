MAKE = make
MKFLAG = -f


default:
	@echo "List of targets:"
	@echo "ccore_x64        - to build release CCORE library for pyclustering (platform x64)."
	@echo "ccore_x64_clean  - to clean build files of CCORE library (platform x64)."
	@echo "ccore_x86        - to build release CCORE library for pyclustering (platform x86)."
	@echo "ccore_x86_clean  - to clean build files of CCORE library (platform x86)."
	@echo " "
	@echo "cppcheck         - to perform static analysis of source code."
	@echo " "
	@echo "ut               - to build release unit-tests for CCORE library."
	@echo "utrun            - to run unit-tests of CCORE library."
	@echo "utclean          - to clean build files of unit-tests of CCORE library."
	@echo " "
	@echo "valgrind         - to build and run unit-tests for memory leak checking of CCORE library."
	@echo " "
	@echo "clean            - to clean everything."


.PHONY: ccore_x64
ccore_x64:
	$(MAKE) $(MKFLAG) ccore.mk ccore PLATFORM="x64"


.PHONY: ccore_x64_clean
ccore_x64_clean:
	$(MAKE) $(MKFLAG) ccore.mk clean PLATFORM="x64"


.PHONY: ccore_x86
ccore_x86:
	$(MAKE) $(MKFLAG) ccore.mk ccore PLATFORM="x86"


.PHONY: ccore_x86_clean
ccore_x86_clean:
	$(MAKE) $(MKFLAG) ccore.mk clean PLATFORM="x86"


.PHONY: cppcheck
cppcheck:
	$(MAKE) $(MKFLAG) ccore.mk cppcheck


.PHONY: ut
ut:
	$(MAKE) $(MKFLAG) utcore.mk ut


.PHONY: utrun
utrun:
	cd tst/ && ./utcore.exe


.PHONY: utclean
utclean:
	$(MAKE) $(MKFLAG) utcore.mk clean


.PHONE: valgrind
valgrind:
	$(MAKE) $(MKFLAG) utcore.mk ut ARGS="valgrind"
	cd tst/ && valgrind --leak-check=full --leak-check=yes --error-exitcode=1 ./utcore.exe


.PHONY: clean
clean:
	$(MAKE) $(MKFLAG) ccore.mk clean PLATFORM="x64"
	$(MAKE) $(MKFLAG) ccore.mk clean PLATFORM="x86"
	$(MAKE) $(MKFLAG) utcore.mk clean

