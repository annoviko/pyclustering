$CI_JOB                = $env:CI_JOB
$APPVEYOR_BUILD_FOLDER = $env:APPVEYOR_BUILD_FOLDER
$CYGWIN_PATH           = $env:CYGWIN_PATH
$MINICONDA_PATH        = $env:MINICONDA_PATH
$PYTHON_VERSION        = $env:PYTHON_VERSION


function job_build_windows_ccore() {
    echo "[CI Job] CCORE building using Visual Studio on Windows platform.";

    msbuild ccore\ccore.sln /t:ccore:Rebuild /p:configuration=Release;
    if ($LastExitCode -ne 0) {
        echo "Building CCORE library for WINDOWS platform: FAILURE.";
        exit 1;
    }
    
    echo "Building CCORE library for WINDOWS platform: SUCCESS.";
}


function job_ut_windows_ccore() {
    echo "[CI Job] CCORE unit-test building and running using Visual Studio on Windows platform.";

    msbuild ccore\ccore.sln /t:utcore:Rebuild /p:configuration=Release;
    if ($LastExitCode -ne 0) {
        echo "Building of CCORE unit-test project for WINDOWS platform: FAILURE.";
        exit 1;
    }
    
    echo "Building of CCORE unit-test project for WINDOWS platform: SUCCESS.";
    
    cd ccore\Release;
    .\utcore.exe;
    if ($LastExitCode -ne 0) {
        echo "Unit-testing CCORE library for WINDOWS platform: FAILURE.";
        exit 1;
    }
    
    echo "Unit-testing CCORE library for WINDOWS platform: SUCCESS.";
}


function job_build_cygwin_ccore() {
    echo "[CI Job] CCORE building using GCC on Cygwin platform.";

    & $CYGWIN_PATH -lc "cygcheck -dc cygwin";
    & $CYGWIN_PATH -lc "cd '$APPVEYOR_BUILD_FOLDER'; cd ccore; make ccore";
    if ($LastExitCode -ne 0) {
        echo "Building CCORE library for CYGWIN platform: FAILURE.";
        exit 1;
    }
    
    echo "Building CCORE library for CYGWIN platform: SUCCESS.";
}


function job_ut_cygwin_ccore() {
    echo "[CI Job] CCORE unit-test building and running using Visual Studio on Windows platform.";
    
    & $CYGWIN_PATH -lc "cd '$APPVEYOR_BUILD_FOLDER'; cd ccore; make ut; make utrun";
    if ($LastExitCode -ne 0) {
        echo "Unit-testing CCORE library for WINDOWS platform: FAILURE.";
        exit 1;
    }
    
    echo "Unit-testing CCORE library for CYGWIN platform: SUCCESS.";
}


function job_pyclustering_windows() {
    echo "[CI Job] Testing interaction between pyclustering and CCORE on Windows platform.";

    install_miniconda;

    $env:PATH="$env:PATH;$pwd.Path";

    job_build_windows_ccore;

    echo "Starting integration testing.";
    
    & $MINICONDA_PATH\python.exe pyclustering\ut\__init__.py
    if ($LastExitCode -ne 0) {
        echo "Integration testing pyclustering <-> ccore for WINDOWS platform: FAILURE.";
        exit 1;
    }
    
    echo "Integration testing pyclustering <-> ccore for WINDOWS platform: SUCCESS.";
}


function job_pyclustering_cygwin() {
    echo "[CI Job] Testing interaction between pyclustering and CCORE on Cygwin platform.";
    echo "[CI Job] Job is not ready yet.";
}


function install_miniconda() {
    $env:PATH="$env:PATH;$MINICONDA_PATH;$MINICONDA_PATH\Scripts";
    
    echo "Starting process of installation of miniconda.";
    
    conda config --set always_yes yes --set changeps1 no;
    conda update -q conda;
    conda config --add channels bashtage;
    conda create -q -n test-environment python=3.4 numpy scipy matplotlib Pillow;
    source activate test-environment;
    
    echo "Python information after installation of miniconda:";
    & $MINICONDA_PATH\python.exe --version;
}


switch ($CI_JOB) {
    "BUILD_WINDOWS_CCORE" {
        job_build_windows_ccore;
        break; 
    }
    "UT_WINDOWS_CCORE" {
        job_ut_windows_ccore;
        break;
    }
    "BUILD_CYGWIN_CCORE" {
        job_build_cygwin_ccore;
        break;
    }
    "UT_CYGWIN_CCORE" {
        job_ut_cygwin_ccore;
        break;
    }
    "PYCLUSTERING_WINDOWS" {
        job_pyclustering_windows;
        break; 
    }
    "PYCLUSTERING_CYGWIN" {
        job_pyclustering_cygwin;
        break;
    }
    default {
        echo "[CI Job] Unknown target '$CI_JOB'";
        exit 1;
    }
}
