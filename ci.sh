#!/bin/bash

run_ccore_job() {
	sudo apt-get install -qq "g++-4.8"
	export CXX="g++-4.8" CC="gcc-4.8"
	
	echo "CI Job (travis CI): CCORE (C++ code library compilation)"
	
	cd ccore/
	make ccore
	
	if [ $? -eq 0 ] ; then
		echo "ccore library creation... success"
	else
		echo "ccore library creation... fail"
		exit 1
	fi
}

run_utcore_job() {
	sudo apt-get install -qq "g++-4.8"
	export CXX="g++-${GCC_VERSION}" CC="gcc-${GCC_VERSION}"
	
	echo "CI Job (travis CI): UT CORE (C++ code unit-testing)"
	
	cd ccore/
	make utcore
	
	if [ $? -eq 0 ] ; then
		echo "ccore library creation... success"
	else
		echo "ccore library creation... fail"
		exit 1
	fi	
}

run_python_job() {
	echo "CI Job (travis CI): PYCLUSTERING (Python code unit-testing)"

	python pyclustering/ut/__init__.py
}

set -e
set -x

case $PYCLUSTERING_TARGET in
	CCORE) 
		run_ccore_job ;;
		
	UTCCORE) 
	
		run_utcore_job ;;
		
	PYTHON) 
		run_python_job ;;
		
	*)
		echo "CI Job (travis CI): Unknown target $PYCLUSTERING_TARGET"
		exit 1 ;;
esac
