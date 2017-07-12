MAKE = make
MKFLAG = -f


default:
	@echo "List of targets:"
	@echo "ccore          - to build release CCORE library for pyclustering."
	@echo "ccore_clean    - to clean build files of CCORE library."
	@echo " "
	@echo "ut             - to build release unit-tests for CCORE library."
	@echo "utrun          - to run unit-tests of CCORE library."
	@echo "utclean        - to clean build files of unit-tests of CCORE library."
	@echo " "
	@echo "valgrind       - to build and run unit-tests for memory leak checking of CCORE library."
	@echo " "
	@echo "clean          - to clean everything."


.PHONY: ccore
ccore:
	$(MAKE) $(MKFLAG) ccore.mk ccore


.PHONY: ccore_clean
ccore_clean:
	$(MAKE) $(MKFLAG) ccore.mk clean


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
	$(MAKE) $(MKFLAG) utcore.mk ARGS="valgrind"
	cd tst/ && valgrind --leak-check=full --leak-check=yes --error-exitcode=1 ./utcore.exe


.PHONY: clean
clean:
	$(MAKE) $(MKFLAG) ccore.mk clean
	$(MAKE) $(MKFLAG) utcore.mk clean

