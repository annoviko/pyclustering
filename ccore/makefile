MAKE = make
MKFLAG = -f


default:
	@echo "List of targets:"
	@echo "ccore       - to build release CCORE library for pyclustering."
	@echo "ut          - to build release unit-tests for CCORE library."
	@echo "utrun       - to run unit-tests of CCORE library."
	@echo "valgrind    - to build and run unit-tests for memory leak checking of CCORE library."
	@echo " "
	@echo "clean       - to clean everything."


.PHONY: ccore
ccore:
	rm -rf ../pyclustering/core/x64/linux
	mkdir ../pyclustering/core/x64/linux
	$(MAKE) $(MKFLAG) ccore.mk


.PHONY: ut
ut:
	$(MAKE) $(MKFLAG) utcore.mk


.PHONY: utrun
utrun:
	cd tst/ && ./utcore.exe


.PHONE: valgrind
valgrind:
	$(MAKE) $(MKFLAG) utcore.mk ARGS="valgrind"
	cd tst/ && valgrind --leak-check=yes --error-exitcode=1 ./utcore.exe


.PHONY: clean
clean:
	find src/ tst/ -name "*.d" -or -name "*.o" -or -name "*.gcda" -or -name "*.gcno" | xargs rm -f
	rm -f ../pyclustering/core/x64/linux/ccore.so
	rm -f tst/utcore.exe

