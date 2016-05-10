#!/bin/bash


run_ccore_job() {
	echo "[CI Job] CCORE (C++ code building):"
	echo "- Build CCORE library."
	
	cd ccore/
	make ccore
	
	if [ $? -eq 0 ] ; then
		echo "Building CCORE library: SUCCESS."
	else
		echo "Building CCORE library: FAILURE."
		exit 1
	fi
}


run_utcore_job() {
	echo "[CI Job] UT CORE (C++ code unit-testing):"
	echo "- Build C++ unit-test project for CCORE library."
	echo "- Run CCORE library unit-tests."
	
	#install coveralls for cpp to measure core coverage
	pip install --user cpp-coveralls
	
	# build unit-test project
	cd ccore/
	make ut

	if [ $? -eq 0 ] ; then
		echo "Building of CCORE unit-test project: SUCCESS."
	else
		echo "Building of CCORE unit-test project: FAILURE."
		exit 1
	fi

	# run unit-tests and obtain code coverage
	make utrun
	coveralls --exclude tst
}


run_python_job() {
	echo "[CI Job]: PYCLUSTERING (Python code unit-testing):"
	echo "- Run unit-tests of pyclustering."
	echo "- Measure code coverage."

	# install coveralls for python to measure code coverage
	pip install coveralls
	
	# initialize environment
	PYTHONPATH=`pwd`
	export PYTHONPATH=${PYTHONPATH}

	# run unit-tests and obtain coverage results
	coverage run --source=pyclustering --omit='pyclustering/*/tests/*,pyclustering/*/examples/*,pyclustering/ut/*' pyclustering/ut/__init__.py
	coveralls
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
		echo "[CI Job] Unknown target $PYCLUSTERING_TARGET"
		exit 1 ;;
esac
