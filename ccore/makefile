#
# Copyright (C) 2014-2018    Andrei Novikov (pyclustering@yandex.ru)
#
# GNU_PUBLIC_LICENSE
#   pyclustering is free software: you can redistribute it and/or modify
#   it under the terms of the GNU General Public License as published by
#   the Free Software Foundation, either version 3 of the License, or
#   (at your option) any later version.
#
#   pyclustering is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.
#
#   You should have received a copy of the GNU General Public License
#   along with this program.  If not, see <http://www.gnu.org/licenses/>.
#


MAKE = make
MKFLAG = -f


default:
	@echo "List of targets:"
	@echo "ccore_x64        - to build release CCORE library for pyclustering (platform x64)."
	@echo "ccore_x64_clean  - to clean build files of CCORE library (platform x64)."
	@echo "ccore_x86        - to build release CCORE library for pyclustering (platform x86)."
	@echo "ccore_x86_clean  - to clean build files of CCORE library (platform x86)."
	@echo "ccore            - to build all releases of CCORE library for pyclustering."
	@echo "ccore_clean      - to clean all build files of CCORE library."
	@echo " "
	@echo "cppcheck         - to perform static analysis of source code."
	@echo " "
	@echo "ut               - to build release unit-tests for CCORE library."
	@echo "utdbg            - to build debug unit-tests for CCORE library."
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


.PHONY: ccore
ccore:
	$(MAKE) $(MKFLAG) ccore.mk ccore PLATFORM="x64"
	$(MAKE) $(MKFLAG) ccore.mk ccore PLATFORM="x86"


.PHONY: ccore_clean
ccore_clean:
	$(MAKE) $(MKFLAG) ccore.mk clean PLATFORM="x64"
	$(MAKE) $(MKFLAG) ccore.mk clean PLATFORM="x86"


.PHONY: cppcheck
cppcheck:
	$(MAKE) $(MKFLAG) ccore.mk cppcheck


.PHONY: ut
ut:
	$(MAKE) $(MKFLAG) utcore.mk ut


.PHONY: utdbg
utdbg:
	$(MAKE) $(MKFLAG) utcore.mk ut CONFIG="debug"


.PHONY: utrun
utrun:
	cd tst/ && ./utcore.exe


.PHONY: utclean
utclean:
	$(MAKE) $(MKFLAG) utcore.mk clean


.PHONE: valgrind
valgrind:
	$(MAKE) $(MKFLAG) utcore.mk ut CONFIG="valgrind"
	cd tst/ && valgrind --leak-check=full --leak-check=yes --error-exitcode=1 ./utcore.exe


.PHONY: clean
clean:
	$(MAKE) $(MKFLAG) ccore.mk clean PLATFORM="x64"
	$(MAKE) $(MKFLAG) ccore.mk clean PLATFORM="x86"
	$(MAKE) $(MKFLAG) utcore.mk clean

