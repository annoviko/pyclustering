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


CCORE_X64_BINARY_FOLDER=pyclustering/core/x64/linux
CCORE_X64_BINARY_PATH=$CCORE_X64_BINARY_FOLDER/ccore.so

CCORE_X86_BINARY_FOLDER=pyclustering/core/x86/linux
CCORE_X86_BINARY_PATH=$CCORE_X86_BINARY_FOLDER/ccore.so

DOXYGEN_FILTER=( "warning: Unexpected new line character" )


print_error() {
    echo "[PYCLUSTERING CI] ERROR: $1"
}


print_info() {
    echo "[PYCLUSTERING CI] INFO: $1"
}


check_failure() {
    if [ $? -ne 0 ] ; then
        if [ -z $1 ] ; then
            print_error $1
        else
            print_error "Failure exit code is detected."
        fi
        exit 1
    fi
}


check_error_log_file() {
    problems_amount=$(cat $1 | wc -l)
    printf "Total amount of errors and warnings: '%d'\n"  "$problems_amount"
    
    if [ $problems_amount -ne 0 ] ; then
        print_info "List of warnings and errors:"
        cat $1
        
        print_error $2
        exit 1
    fi
}


filter_content() {
    file_name=$1
    output_file_name=$2

    if [ ${#DOXYGEN_FILTER[@]} -eq 0 ]; then
        cat $file_name
        return
    fi

    while read line
    do
        for string_filter in "${DOXYGEN_FILTER[@]}"
        do
            if [[ "$line" != *"$string_filter"* ]]
            then
                echo -e "$line" >> $output_file_name
            fi
        done
    done < $file_name
}


build_ccore() {
    cd $TRAVIS_BUILD_DIR/ccore/

    [ -f stderr.log ] && rm stderr.log
    [ -f stdout.log ] && rm stdout.log
    
    if [ "$1" == "x64" ]; then
        make ccore_x64 > >(tee -a stdout.log) 2> >(tee -a stderr.log >&2)
        check_error_log_file stderr.log "Building CCORE (x64): FAILURE."
    elif [ "$1" == "x86" ]; then
        make ccore_x86 > >(tee -a stdout.log) 2> >(tee -a stderr.log >&2)
        check_error_log_file stderr.log "Building CCORE (x86): FAILURE."
    else
        print_error "Unknown CCORE platform is specified."
        exit 1
    fi

    cd -
}


run_build_ccore_job() {
    print_info "CCORE (C++ code building):"
    print_info "- Build CCORE library for x64 platform."
    print_info "- Build CCORE library for x86 platform."

    #install requirement for the job
    print_info "Install requirement for CCORE building."

    sudo apt-get install -qq g++-5
    sudo apt-get install -qq g++-5-multilib
    sudo update-alternatives --install /usr/bin/g++ g++ /usr/bin/g++-5 50

    # show info
    g++ --version
    gcc --version

    # build ccore library
    build_ccore x64
    build_ccore x86

    print_info "Upload ccore x64 binary."
    upload_binary x64
    
    print_info "Upload ccore x86 binary."
    upload_binary x86
}


run_analyse_ccore_job() {
    print_info "ANALYSE CCORE (C/C++ static analysis):"
    print_info "- Code checking using 'cppcheck'."

    # install requirement for the job
    print_info "Install requirement for static analysis of CCORE."

    sudo apt-get install -qq cppcheck
    sudo apt-get install -qq clang

    # analyse source code
    cd ccore/

    make cppcheck
    check_failure "C/C++ static analysis (tool: 'cppcheck'): FAILURE."

    print_info "- Code checking using 'scan-build clang++'."
    make clang > >(tee -a stdout.log) 2> >(tee -a stderr.log >&2)
    check_error_log_file stderr.log "C/C++ static analysis (tool: 'scan-build clang++'): FAILURE."
}


run_ut_ccore_job() {
    print_info "UT CCORE (C++ code unit-testing of CCORE library):"
    print_info "- Build C++ unit-test project for CCORE library."
    print_info "- Run CCORE library unit-tests."

    # install requirements for the job
    sudo apt-get install -qq g++-5
    sudo update-alternatives --install /usr/bin/g++ g++ /usr/bin/g++-5 50
    sudo update-alternatives --install /usr/bin/gcov gcov /usr/bin/gcov-5 50

    pip install cpp-coveralls

    # build unit-test project
    cd ccore/

    make ut > >(tee -a stdout.log) 2> >(tee -a stderr.log >&2)
    check_error_log_file stderr.log "Building CCORE unit-tests: FAILURE."

    # run unit-tests and obtain code coverage
    make utrun
    check_failure "CCORE unit-testing status: FAILURE."
    
    # step back to have full path to files in coverage reports
    coveralls --root ../ --build-root . --exclude ccore/tst/ --exclude ccore/external/ --gcov-options '\-lp'
}


run_valgrind_ccore_job() {
    print_info "VALGRIND CCORE (C++ code valgrind shock checking):"
    print_info "- Run unit-tests of pyclustering."
    print_info "- Shock memory leakage detection by valgrind."

    # install requirements for the job
    sudo apt-get install -qq g++-5
    sudo apt-get install -qq g++-5-multilib
    sudo apt-get install -qq valgrind
    sudo update-alternatives --install /usr/bin/g++ g++ /usr/bin/g++-5 50

    # build and run unit-test project under valgrind to check memory leakage
    cd ccore/

    make valgrind_shock
    check_failure "CCORE shock memory leakage status: FAILURE."
}


run_test_pyclustering_job() {
    print_info "TEST PYCLUSTERING (unit and integration testing):"
    print_info "- Download CCORE library."
    print_info "- Run unit and integration tests of pyclustering."
    print_info "- Measure code coverage for python code."

    # install requirements for the job
    install_miniconda x64
    pip install coveralls

    sudo apt-get install -qq g++-5
    sudo update-alternatives --install /usr/bin/g++ g++ /usr/bin/g++-5 50
    sudo update-alternatives --install /usr/bin/gcov gcov /usr/bin/gcov-5 50

    # set path to the tested library
    PYTHONPATH=`pwd`
    export PYTHONPATH=${PYTHONPATH}

    # build ccore library
    build_ccore x64

    # run unit and integration tests and obtain coverage results
    coverage run --source=pyclustering --omit='pyclustering/*/tests/*,pyclustering/*/examples/*,pyclustering/tests/*' pyclustering/tests/tests_runner.py
    coveralls
}


run_integration_test_job() {
    print_info "INTEGRATION TESTING ('ccore' <-> 'pyclustering' for platform '$1')."
    print_info "- Build CCORE library."
    print_info "- Run integration tests of pyclustering."

    PLATFORM_TARGET=$1

    # install requirements for the job
    install_miniconda $PLATFORM_TARGET

    sudo apt-get install -qq g++-5 gcc-5
    sudo apt-get install -qq g++-5-multilib gcc-5-multilib
    sudo update-alternatives --install /usr/bin/g++ g++ /usr/bin/g++-5 50
    sudo update-alternatives --install /usr/bin/gcov gcov /usr/bin/gcov-5 50

    # build ccore library
    build_ccore $PLATFORM_TARGET

    # run integration tests
    python pyclustering/tests/tests_runner.py --integration
}


run_build_test_ccore_macos_job() {
    print_info "BUILD AND TEST CCORE FOR MACOS."
    print_info "- Build CCORE library."
    print_info "- Run integration tests of pyclustering."
    print_info "- Upload binary to cloud."

    # build ccore library
    build_ccore x64

    # install python and corresponding packages
    brew install python3
    pip3 install numpy matplotlib scipy Pillow

    # run integration tests
    python pyclustering/tests/tests_runner.py --integration

    # TODO: upload binary to cloud
}


run_doxygen_job() {
    print_info "DOXYGEN (documentation generation)."
    print_info "- Generate documentation and check for warnings."

    print_info "Install doxygen"
    sudo apt-get install doxygen

    print_info "Install requirements for doxygen."
    sudo apt-get install graphviz
    sudo apt-get install texlive

    print_info "Prepare log files."
    report_file=doxygen_problems.log
    report_file_filtered=doxygen_problems_filtered.log

    rm -f $report_file
    rm -f $report_file_filtered

    print_info "Generate documentation."
    doxygen --version
    doxygen docs/doxygen_conf_pyclustering > /dev/null 2> $report_file

    filter_content $report_file $report_file_filtered
    check_error_log_file $report_file_filtered "Building doxygen documentation: FAILURE."
    print_info "Building doxygen documentation: SUCCESS."
}


run_deploy_job() {
    print_info "Deploy (upload linux binary file to github)"
    if [[ $TRAVIS_COMMIT_MESSAGE != *"[publish]"* ]]; then
        print_info "Binary files will not be published to github repository (keyword '[publish]' is not specified)."
        exit 0
    fi
    
    git config --global user.email "pyclustering@yandex.ru"
    git config --global user.name "Travis-CI"

    git config credential.helper "store --file=.git/credentials"
    echo "https://${GH_TOKEN}:@github.com" > .git/credentials
    git config credential.helper "store --file=.git/credentials"


    print_info "Prepare copy for pushing (reset, checkout, pull)"
    git reset --hard
    git checkout $TRAVIS_BRANCH
    git pull


    print_info "Prepare binary folder"
    [ ! -d $CCORE_X64_BINARY_FOLDER ] && mkdir $CCORE_X64_BINARY_FOLDER
    [ ! -d $CCORE_X86_BINARY_FOLDER ] && mkdir $CCORE_X86_BINARY_FOLDER

    download_binary x64
    download_binary x86

    print_info "Add changes for commit"
    echo "linux ccore $PLATFORM_TARGET build version: '$TRAVIS_BUILD_NUMBER'" > $CCORE_X64_BINARY_FOLDER/.linux.info
    echo "linux ccore $PLATFORM_TARGET build version: '$TRAVIS_BUILD_NUMBER'" > $CCORE_X86_BINARY_FOLDER/.linux.info
    git add $CCORE_X64_BINARY_FOLDER/.linux.info
    git add $CCORE_X86_BINARY_FOLDER/.linux.info
    git add $CCORE_X64_BINARY_FOLDER/ccore.so 
    git add $CCORE_X86_BINARY_FOLDER/ccore.so


    print_info "Display status and changes"
    git status

    print_info "Push changes to github repository"
    git commit . -m "[travis-ci][ci skip] push new ccore version '$TRAVIS_BUILD_NUMBER'"
    git push
}


install_miniconda() {
    print_info "Start downloading process of Miniconda."
    
    PLATFORM_TARGET=$1
    if [ "$PLATFORM_TARGET" == "x64" ]; then
        print_info "Download Miniconda for platform '$PLATFORM_TARGET'."
        wget https://repo.continuum.io/miniconda/Miniconda3-4.3.27-Linux-x86_64.sh -O miniconda.sh
    elif [ "$PLATFORM_TARGET" == "x86" ]; then
        print_info "Download Miniconda for platform '$PLATFORM_TARGET'"
        wget https://repo.continuum.io/miniconda/Miniconda3-4.3.27-Linux-x86.sh -O miniconda.sh
    else
        print_error "Unknown platform '$PLATFORM_TARGET' is specified for Miniconda."
        exit 1
    fi
    
    print_info "Installing Miniconda."
    bash miniconda.sh -b -p $HOME/miniconda

    export PATH="$HOME/miniconda/bin:$PATH"
    hash -r

    print_info "Configuring Miniconda."
    
    conda config --set always_yes yes

    conda install -q libgfortran

    conda create -q -n test-environment python=3.5 numpy scipy matplotlib Pillow

    source activate test-environment
}


upload_binary() {
    print_info "Upload binary files to storage."

    BUILD_FOLDER=linux
    BUILD_PLATFORM=$1
    BINARY_FOLDER=$TRAVIS_BUILD_NUMBER

    LOCAL_BINARY_PATH=
    if [ "$BUILD_PLATFORM" == "x64" ]; then
        LOCAL_BINARY_PATH=$CCORE_X64_BINARY_PATH
    elif [ "$BUILD_PLATFORM" == "x86" ]; then
        LOCAL_BINARY_PATH=$CCORE_X86_BINARY_PATH
    else
        print_error "Invalid platform is specified '$BUILD_PLATFORM' for uploading."
        exit 1
    fi

    # Create folder for uploaded binary file
    python3 ci/cloud $YANDEX_DISK_TOKEN mkdir /$TRAVIS_BRANCH
    python3 ci/cloud $YANDEX_DISK_TOKEN mkdir /$TRAVIS_BRANCH/$BUILD_FOLDER
    python3 ci/cloud $YANDEX_DISK_TOKEN mkdir /$TRAVIS_BRANCH/$BUILD_FOLDER/$BUILD_PLATFORM
    python3 ci/cloud $YANDEX_DISK_TOKEN mkdir /$TRAVIS_BRANCH/$BUILD_FOLDER/$BUILD_PLATFORM/$BINARY_FOLDER

    # Upload binary file
    REMOTE_BINARY_FILEPATH=/$TRAVIS_BRANCH/$BUILD_FOLDER/$BUILD_PLATFORM/$BINARY_FOLDER/ccore.so

    python3 ci/cloud $YANDEX_DISK_TOKEN upload $LOCAL_BINARY_PATH $REMOTE_BINARY_FILEPATH
}


download_binary() {
    print_info "Download CCORE binary (platform: '$1') file from cloud."

    BUILD_PLATFORM=$1
    
    LOCAL_BINARY_PATH=
    if [ "$BUILD_PLATFORM" == "x64" ]; then
        LOCAL_BINARY_PATH=$CCORE_X64_BINARY_PATH
    elif [ "$BUILD_PLATFORM" == "x86" ]; then
        LOCAL_BINARY_PATH=$CCORE_X86_BINARY_PATH
    else
        print_error "Unkown platform is specified impossible to identify where to place binary."
        exit 1
    fi

    # Download binary file
    BUILD_FOLDER=linux
    BINARY_FOLDER=$TRAVIS_BUILD_NUMBER
    BINARY_FILEPATH=/$TRAVIS_BRANCH/$BUILD_FOLDER/$BUILD_PLATFORM/$BINARY_FOLDER/ccore.so

    python3 ci/cloud $YANDEX_DISK_TOKEN download $BINARY_FILEPATH $LOCAL_BINARY_PATH
    
    print_info "Content of the binary folder."
    ls $LOCAL_BINARY_PATH -la
}



set -e
set -x

if [[ $TRAVIS_COMMIT_MESSAGE == *"[no-build]"* ]]; then
    print_info "Option '[no-build]' is detected, sources will not be built, checked, verified and published."
    exit 0
fi

if [[ $TRAVIS_COMMIT_MESSAGE == *"[build-only-osx]"* ]]; then
    if [[ $1 == BUILD_TEST_CCORE_MACOS ]]; then
        print_info "Option '[build-only-osx]' is detected, mac os build will be started."
    else
        print_info "Option '[build-only-osx]' is detected, sources will not be built, checked, verified and published."
        exit 0
    fi
fi

case $1 in
    BUILD_CCORE) 
        run_build_ccore_job ;;

    ANALYSE_CCORE)
        run_analyse_ccore_job ;;

    UT_CCORE) 
        run_ut_ccore_job ;;

    VALGRIND_CCORE)
        run_valgrind_ccore_job ;;

    TEST_PYCLUSTERING) 
        run_test_pyclustering_job ;;

    IT_CCORE_X86)
        run_integration_test_job x86 ;;

    IT_CCORE_X64)
        run_integration_test_job x64 ;;

    BUILD_TEST_CCORE_MACOS)
        run_build_test_ccore_macos_job ;;

    DOCUMENTATION)
        run_doxygen_job ;;

    DEPLOY)
        run_deploy_job ;;

    *)
        print_error "Unknown target is specified: '$1'"
        exit 1 ;;
esac
