#!/bin/bash

run_ccore_job() {
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
	echo "CI Job (travis CI): UT CORE (C++ code unit-testing)"
	
	cd ccore/
	make utcore
	
	if [ $? -eq 0 ] ; then
		echo "ccore library creation... success"
	else
		echo "ccore library creation... fail"
		exit 1
	fi
	
	# run unit-tests
	./utcore/utcore
}

run_python_job() {
	echo "CI Job (travis CI): PYCLUSTERING (Python code unit-testing)"

	# run unit-tests
	python pyclustering/ut/__init__.py
}

set -e
set -x

case $PYCLUSTERING_TARGET in
	CCORE) 
		run_ccore_job ;;
		
	UTCORE) 
		run_utcore_job ;;
		
	PYTHON) 
		run_python_job ;;
		
	*)
		echo "CI Job (travis CI): Unknown target $PYCLUSTERING_TARGET"
		exit 1 ;;
esac
