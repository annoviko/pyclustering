#!/bin/bash


run_build_ccore_job() {
	echo "[CI Job] CCORE (C++ code building):"
	echo "- Build CCORE library."
	
	#install requirement for the job
	sudo apt-get install -qq g++-4.8
	sudo update-alternatives --install /usr/bin/g++ g++ /usr/bin/g++-4.8 50
	
	# build ccore library
	cd ccore/
	make ccore
	
	if [ $? -eq 0 ] ; then
		echo "Building CCORE library: SUCCESS."
	else
		echo "Building CCORE library: FAILURE."
		exit 1
	fi
}


run_ut_ccore_job() {
	echo "[CI Job] UT CCORE (C++ code unit-testing of CCORE library):"
	echo "- Build C++ unit-test project for CCORE library."
	echo "- Run CCORE library unit-tests."
	
	# install requirements for the job
	sudo apt-get install -qq g++-4.8
	sudo update-alternatives --install /usr/bin/g++ g++ /usr/bin/g++-4.8 50
  
	pip install cpp-coveralls
	
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
	coveralls --exclude tst/ --exclude tools/ --gcov-options '\-lp'
}


run_ut_pyclustering_job() {
	echo "[CI Job]: UT PYCLUSTERING (Python code unit-testing):"
	echo "- Run unit-tests of pyclustering."
	echo "- Measure code coverage."

	# install requirements for the job
	sudo apt-get install python3-scipy
	pip3 install numpy
	pip3 install Pillow
	pip3 install matplotlib
	
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

case $CI_JOB in
	BUILD_CCORE) 
		run_build_ccore_job ;;
		
	UT_CCORE) 
		run_ut_ccore_job ;;
		
	UT_PYCLUSTERING) 
		run_ut_pyclustering_job ;;
		
	*)
		echo "[CI Job] Unknown target $CI_JOB"
		exit 1 ;;
esac
