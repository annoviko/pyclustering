#!/bin/bash


CCORE_X64_BINARY_PATH=pyclustering/core/x64/linux/ccore.so


run_build_ccore_job() {
    echo "[CI Job] CCORE (C++ code building):"
    echo "- Build CCORE library."

    #install requirement for the job
    sudo apt-get install -qq g++-5
    sudo update-alternatives --install /usr/bin/g++ g++ /usr/bin/g++-5 50

    # build ccore library
    cd ccore/
    make ccore

    if [ $? -eq 0 ] ; then
        echo "Building CCORE library: SUCCESS."
    else
        echo "Building CCORE library: FAILURE."
        exit 1
    fi

    # return back (keep current folder)
    cd ../
}


run_ut_ccore_job() {
    echo "[CI Job] UT CCORE (C++ code unit-testing of CCORE library):"
    echo "- Build C++ unit-test project for CCORE library."
    echo "- Run CCORE library unit-tests."

    # install requirements for the job
    sudo apt-get install -qq g++-5
    sudo update-alternatives --install /usr/bin/g++ g++ /usr/bin/g++-5 50
    sudo update-alternatives --install /usr/bin/gcov gcov /usr/bin/gcov-5 50

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
    
    # step back to have full path to files in coverage reports
    coveralls --root ../ --build-root . --exclude ccore/tst/ --exclude ccore/tools/ --gcov-options '\-lp'

    # return back (keep current folder)
    cd ../
}


run_valgrind_ccore_job() {
    echo "[CI Job]: VALGRIND CCORE (C++ code valgrind checking):"
    echo "- Run unit-tests of pyclustering."
    echo "- Memory leakage detection by valgrind."

    # install requirements for the job
    sudo apt-get install -qq g++-5
    sudo apt-get install -qq valgrind
    sudo update-alternatives --install /usr/bin/g++ g++ /usr/bin/g++-5 50

    # build and run unit-test project under valgrind to check memory leakage
    cd ccore/
    make valgrind

    # return back (keep current folder)
    cd ../
}


run_test_pyclustering_job() {
    echo "[CI Job]: TEST PYCLUSTERING (unit and integration testing):"
    echo "- Rebuilt CCORE library."
    echo "- Run unit and integration tests of pyclustering."
    echo "- Measure code coverage for python code."

    # install requirements for the job
    install_miniconda
    pip install coveralls

    # set path to the tested library
    PYTHONPATH=`pwd`
    export PYTHONPATH=${PYTHONPATH}

    # build ccore library
    run_build_ccore_job

    # run unit-tests and obtain coverage results
    coverage run --source=pyclustering --omit='pyclustering/*/tests/*,pyclustering/*/examples/*,pyclustering/tests/*' pyclustering/tests/tests_runner.py
    coveralls
}


run_doxygen_job() {
    echo "[CI Job]: DOXYGEN (documentation generation)."
    
    # install requirements for the job
    sudo apt-get install doxygen
    sudo apt-get install graphviz
    sudo apt-get install texlive
    
    # generate doxygen documentation
    doxygen docs/doxygen_conf_pyclustering > /dev/null 2> doxygen_problems.txt
    
    problems_amount=$(cat doxygen_problems.txt | wc -l)
    printf "Total amount of doxygen errors and warnings: '%d'\n"  "$problems_amount"
    
    if [ $problems_amount -ne 0 ] ; then
        echo "List of warnings and errors:"
        cat doxygen_problems.txt
        
        echo "Building doxygen documentation: FAILURE."
        exit 1
    else
        echo "Building doxygen documentation: SUCCESS."
    fi
}


run_deploy_job() {
    echo "[CI_JOB]: Deploy (upload linux binary file to github)"
    
    git config --global user.email "travis@travis-ci.org"
    git config --global user.name "Travis CI"
    
    git checkout . -b $TRAVIS_BRANCH
    git add pyclustering/core/linux/ccore.so
    git commit . -m "[travis-ci build] push new ccore version '$TRAVIS_BUILD_NUMBER'"
    git push
}


install_miniconda() {
    wget https://repo.continuum.io/miniconda/Miniconda3-latest-Linux-x86_64.sh -O miniconda.sh

    bash miniconda.sh -b -p $HOME/miniconda

    export PATH="$HOME/miniconda/bin:$PATH"
    hash -r

    conda config --set always_yes yes --set changeps1 no
    conda update -q conda

    conda install libgfortran
    conda create -q -n test-environment python=3.4 numpy scipy matplotlib Pillow
    source activate test-environment
}


set -e
set -x


case $CI_JOB in
    BUILD_CCORE) 
        run_build_ccore_job ;;
        
    UT_CCORE) 
        run_ut_ccore_job ;;

    VALGRIND_CCORE)
        run_valgrind_ccore_job ;;

    TEST_PYCLUSTERING) 
        run_test_pyclustering_job ;;

    DOCUMENTATION)
        run_doxygen_job ;;

    DEPLOY)
        echo "[CI Job] Deploy job is disabled" ;;
#        run_deploy_job ;;

    *)
        echo "[CI Job] Unknown target $CI_JOB"
        exit 1 ;;
esac
