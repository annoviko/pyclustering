CCORE_X64_BINARY_PATH=pyclustering/core/x64/linux/ccore.so
CCORE_X86_BINARY_PATH=pyclustering/core/x86/linux/ccore.so


print_error() {
    echo "ERROR: $1"
}


print_info() {
    echo "INFO: $1"
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


build_ccore() {
    cd $TRAVIS_BUILD_DIR/ccore/

    if [ "$1" == "x64" ]; then
        make ccore_x64
        check_failure "Building CCORE (x64): FAILURE."
    elif [ "$1" == "x86" ]; then
        make ccore_x86
        check_failure "Building CCORE (x86): FAILURE."
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

    upload_binary x64
    upload_binary x86
}


run_analyse_ccore_job() {
    print_info "ANALYSE CCORE (C/C++ static analysis):"
    print_info "- Code checking using 'cppcheck'."

    # install requirement for the job
    print_info "Install requirement for static analysis of CCORE."

    sudo apt-get install -qq cppcheck

    # analyse source code
    cd ccore/

    make cppcheck
    check_failure "C/C++ static analysis: FAILURE."
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

    make ut
    check_failure "Building CCORE unit-tests: FAILURE."

    # run unit-tests and obtain code coverage
    make utrun
    check_failure "CCORE unit-testing status: FAILURE."
    
    # step back to have full path to files in coverage reports
    coveralls --root ../ --build-root . --exclude ccore/tst/ --exclude ccore/tools/ --gcov-options '\-lp'
}


run_valgrind_ccore_job() {
    print_info "VALGRIND CCORE (C++ code valgrind checking):"
    print_info "- Run unit-tests of pyclustering."
    print_info "- Memory leakage detection by valgrind."

    # install requirements for the job
    sudo apt-get install -qq g++-5
    sudo apt-get install -qq g++-5-multilib
    sudo apt-get install -qq valgrind
    sudo update-alternatives --install /usr/bin/g++ g++ /usr/bin/g++-5 50

    # build and run unit-test project under valgrind to check memory leakage
    cd ccore/

    make valgrind
    check_failure "CCORE memory leakage status: FAILURE."
}


run_test_pyclustering_job() {
    print_info "TEST PYCLUSTERING (unit and integration testing for x64):"
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
    sudo apt-get install -qq g++-5
    sudo update-alternatives --install /usr/bin/g++ g++ /usr/bin/g++-5 50
    sudo update-alternatives --install /usr/bin/gcov gcov /usr/bin/gcov-5 50

    install_miniconda $PLATFORM_TARGET

    # build ccore library
    build_ccore $PLATFORM_TARGET

    # run integration tests
    python pyclustering/tests/tests_runner.py --integration
}


run_doxygen_job() {
    print_info "DOXYGEN (documentation generation)."
    print_info "- Generate documentation and check for warnings."


    # install requirements for the job
    print_info "Install requirements for doxygen."

    sudo apt-get install doxygen
    sudo apt-get install graphviz
    sudo apt-get install texlive


    # generate doxygen documentation
    print_info "Generate documentation."

    doxygen docs/doxygen_conf_pyclustering > /dev/null 2> doxygen_problems.txt
    
    problems_amount=$(cat doxygen_problems.txt | wc -l)
    printf "Total amount of doxygen errors and warnings: '%d'\n"  "$problems_amount"
    
    if [ $problems_amount -ne 0 ] ; then
        print_info "List of warnings and errors:"
        cat doxygen_problems.txt
        
        print_error "Building doxygen documentation: FAILURE."
        exit 1
    fi

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
    mkdir pyclustering/core/x64/linux
    mkdir pyclustering/core/x86/linux

    download_binary x64
    download_binary x86

    print_info "Add changes for commit"
    echo "linux ccore $PLATFORM_TARGET build version: '$TRAVIS_BUILD_NUMBER'" > pyclustering/core/x64/linux/.linux.info
    echo "linux ccore $PLATFORM_TARGET build version: '$TRAVIS_BUILD_NUMBER'" > pyclustering/core/x86/linux/.linux.info
    git add pyclustering/core/x64/linux/.linux.info
    git add pyclustering/core/x86/linux/.linux.info
    git add pyclustering/core/x64/linux/ccore.so 
    git add pyclustering/core/x86/linux/ccore.so


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
    mkdir $HOME/miniconda
    bash miniconda.sh -b -p $HOME/miniconda

    export PATH="$HOME/miniconda/bin:$PATH"
    hash -r

    print_info "Configuring Miniconda."
    
    conda config --set always_yes yes

    conda install -q libgfortran

    conda create -q -n test-environment python=3.4 numpy scipy matplotlib Pillow

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
    curl -H "Authorization: OAuth $YANDEX_DISK_TOKEN" -X PUT https://cloud-api.yandex.net:443/v1/disk/resources?path=$TRAVIS_BRANCH
    curl -H "Authorization: OAuth $YANDEX_DISK_TOKEN" -X PUT https://cloud-api.yandex.net:443/v1/disk/resources?path=$TRAVIS_BRANCH%2F$BUILD_FOLDER
    curl -H "Authorization: OAuth $YANDEX_DISK_TOKEN" -X PUT https://cloud-api.yandex.net:443/v1/disk/resources?path=$TRAVIS_BRANCH%2F$BUILD_FOLDER%2F$BUILD_PLATFORM
    curl -H "Authorization: OAuth $YANDEX_DISK_TOKEN" -X PUT https://cloud-api.yandex.net:443/v1/disk/resources?path=$TRAVIS_BRANCH%2F$BUILD_FOLDER%2F$BUILD_PLATFORM%2F$BINARY_FOLDER

    # Obtain link for uploading
    REMOTE_BINARY_FILEPATH=$TRAVIS_BRANCH%2F$BUILD_FOLDER%2F$BUILD_PLATFORM%2F$BINARY_FOLDER%2Fccore.so
    
    print_info "Upload binary using path '$REMOTE_BINARY_FILEPATH'."

    UPLOAD_LINK=`curl -s -H "Authorization: OAuth $YANDEX_DISK_TOKEN" -X GET https://cloud-api.yandex.net:443/v1/disk/resources/upload?path=$REMOTE_BINARY_FILEPATH |\
        python3 -c "import sys, json; print(json.load(sys.stdin)['href'])"`

    curl -H "Authorization: OAuth $YANDEX_DISK_TOKEN" -X PUT $UPLOAD_LINK --upload-file $LOCAL_BINARY_PATH
}


download_binary() {
    print_info "Download CCORE binary (platform: '$1') file from cloud."

    BUILD_PLATFORM=$1
    
    LOCAL_BINARY_PATH=
    if [ "$BUILD_PLATFORM" -eq "x64" ]; then
        LOCAL_BINARY_PATH=$CCORE_X64_BINARY_PATH
    elif [ "$BUILD_PLATFORM" -eq "x86" ]; then
        LOCAL_BINARY_PATH=$CCORE_X86_BINARY_PATH
    else
        print_error "Unkown platform is specified impossible to identify where to place binary."
        exit 1
    fi

    # Obtain link for download
    BUILD_FOLDER=linux
    BINARY_FOLDER=$TRAVIS_BUILD_NUMBER
    BINARY_FILEPATH=$TRAVIS_BRANCH%2F$BUILD_FOLDER%2F$BUILD_PLATFORM%2F$BINARY_FOLDER%2Fccore.so

    DOWNLOAD_LINK=`curl -s -H "Authorization: OAuth $YANDEX_DISK_TOKEN" -X GET https://cloud-api.yandex.net:443/v1/disk/resources/download?path=$BINARY_FILEPATH |\
        python3 -c "import sys, json; print(json.load(sys.stdin)['href'])"`

    print_info "Download link '$DOWNLOAD_LINK'."

    # Download binary to specific folder
    curl -L "$DOWNLOAD_LINK" -o $LOCAL_BINARY_PATH
    
    print_info "Content of the binary folder."
    ls $LOCAL_BINARY_PATH -la
}



set -e
set -x


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

    DOCUMENTATION)
        run_doxygen_job ;;

    DEPLOY)
        run_deploy_job ;;

    *)
        print_error "Unknown target is specified: '$1'"
        exit 1 ;;
esac
