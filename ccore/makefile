#
# @authors Andrei Novikov (pyclustering@yandex.ru)
# @date 2014-2019
# @copyright GNU Public License
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

NCORES = 1
UNAME = $(shell uname -s | tr '[:upper:]' '[:lower:]')
ifeq ($(findstring cygwin, $(UNAME)), cygwin)
	NCORES = $(shell grep -c ^processor /proc/cpuinfo)
else
	ifeq ($(UNAME), darwin)
		NCORES = $(shell sysctl -n hw.ncpu)
	else
		NCORES = $(shell grep -c ^processor /proc/cpuinfo)
	endif
endif


MKFLAG = -j$(NCORES) -f


default:
	@echo "List of targets:"
	@echo "ccore_64bit        - to build release shared pyclustering library (64-bit platform)."
	@echo "ccore_64bit_static - to build release static pyclustering library (64-bit platform)."
	@echo "ccore_64bit_clean  - to clean build files of pyclustering library (64-bit platform)."
	@echo "ccore_32bit        - to build release shared pyclustering library (32-bit platform)."
	@echo "ccore_32bit_static - to build release static pyclustering library (32-bit platform)."
	@echo "ccore_32bit_clean  - to clean build files of pyclustering library (32-bit platform)."
	@echo "ccore              - to build release shared pyclustering library using default compiler."
	@echo "ccore_clean        - to clean all build files of pyclustering library."
	@echo " "
	@echo "cppcheck           - to perform static analysis of source code."
	@echo "clang              - to perform compilation and static analysis using clang compiler."
	@echo " "
	@echo "ut                 - to build release unit-tests for pyclustering library."
	@echo "utdbg              - to build debug unit-tests for pyclustering library."
	@echo "utrun              - to run unit-tests of pyclustering library."
	@echo "utclean            - to clean build files of unit-tests of pyclustering library."
	@echo " "
	@echo "valgrind           - to build and run unit-tests for memory leak checking of pyclustering library."
	@echo "valgrind_shock     - to build and run shock scope of unit-tests for memory leak checking of pyclustering library."
	@echo " "
	@echo "clean              - to clean everything."


.PHONY: ccore_64bit
ccore_64bit:
	$(MAKE) $(MKFLAG) ccore.mk ccore PLATFORM="64-bit"


.PHONY: ccore_64bit_static
ccore_64bit_static:
	$(MAKE) $(MKFLAG) ccore.mk ccore_static PLATFORM="64-bit"


.PHONY: ccore_64bit_clean
ccore_64bit_clean:
	$(MAKE) $(MKFLAG) ccore.mk clean PLATFORM="64-bit"


.PHONY: ccore_32bit
ccore_32bit:
	$(MAKE) $(MKFLAG) ccore.mk ccore PLATFORM="32-bit"


.PHONY: ccore_32bit_static
ccore_32bit_static:
	$(MAKE) $(MKFLAG) ccore.mk ccore_static PLATFORM="32-bit"


.PHONY: ccore_32bit_clean
ccore_32bit_clean:
	$(MAKE) $(MKFLAG) ccore.mk clean PLATFORM="32-bit"


.PHONY: ccore
ccore:
	$(MAKE) $(MKFLAG) ccore.mk ccore


.PHONY: ccore_clean
ccore_clean:
	$(MAKE) $(MKFLAG) ccore.mk clean PLATFORM="64-bit"
	$(MAKE) $(MKFLAG) ccore.mk clean PLATFORM="32-bit"


.PHONY: cppcheck
cppcheck:
	$(MAKE) $(MKFLAG) ccore.mk cppcheck


.PHONY: clang
clang:
	$(MAKE) $(MKFLAG) ccore.mk ccore PLATFORM="64-bit" COMPILER="clang"


.PHONY: ut
ut:
	$(MAKE) $(MKFLAG) utcore.mk ut


.PHONY: utdbg
utdbg:
	$(MAKE) $(MKFLAG) utcore.mk ut CONFIG="debug"


.PHONY: utrun
utrun:
	cd tst/ && python3 ut-runner.py


.PHONY: utclean
utclean:
	$(MAKE) $(MKFLAG) utcore.mk clean


.PHONE: valgrind
valgrind:
	$(MAKE) $(MKFLAG) utcore.mk ut CONFIG="valgrind"
	cd tst/ && valgrind --leak-check=full --leak-check=yes --error-exitcode=1 ./utcore.exe


.PHONE: valgrind_shock
valgrind_shock:
	$(MAKE) $(MKFLAG) utcore.mk ut CONFIG="valgrind" BUILD_VERSION="valgrind_shock"
	cd tst/ && valgrind --leak-check=full --leak-check=yes --error-exitcode=1 ./utcore.exe


.PHONY: clean
clean:
	$(MAKE) $(MKFLAG) ccore.mk clean PLATFORM="64-bit"
	$(MAKE) $(MKFLAG) ccore.mk clean PLATFORM="32-bit"
	$(MAKE) $(MKFLAG) utcore.mk clean
