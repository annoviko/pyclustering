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

    & $env:CYGWIN_PATH -lc "cygcheck -dc cygwin";
    & $env:CYGWIN_PATH -lc "cd '$env:APPVEYOR_BUILD_FOLDER'; cd ccore; make ccore";
    if ($LastExitCode -ne 0) {
        echo "Building CCORE library for CYGWIN platform: FAILURE.";
        exit 1;
    }
    
    echo "Building CCORE library for CYGWIN platform: SUCCESS.";
}


function job_ut_cygwin_ccore() {
    echo "[CI Job] CCORE unit-test building and running using Visual Studio on Windows platform.";
    
    & $env:CYGWIN_PATH -lc "cd '$env:APPVEYOR_BUILD_FOLDER'; cd ccore; make ut; make utrun";
    if ($LastExitCode -ne 0) {
        echo "Unit-testing CCORE library for WINDOWS platform: FAILURE.";
        exit 1;
    }
    
    echo "Unit-testing CCORE library for CYGWIN platform: SUCCESS.";
}


function job_pyclustering_windows() {
    echo "[CI Job] Testing interaction between pyclustering and CCORE on Windows platform.";

    install_miniconda;

    echo "Set path '$env:APPVEYOR_BUILD_FOLDER' to tested pyclustering library."
    $env:PYTHONPATH = "$env:APPVEYOR_BUILD_FOLDER;$env:PYTHONPATH";

    job_build_windows_ccore;

    echo "Starting integration testing.";
    
    & $env:PYTHON_INTERPRETER pyclustering\ut\__init__.py
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
    $env:PATH="$env:PATH;$env:MINICONDA_PATH\Scripts";
    
    echo "Starting process of installation of miniconda.";
    
    conda config --set always_yes yes --set changeps1 no;
    conda update -q conda;
    conda create -q -n test-environment python=3.4 numpy scipy matplotlib Pillow;
    
    echo "Activating environment for powershell manually."
    $env:PYTHON_INTERPRETER="$env:MINICONDA_PATH\envs\test-environment\python.exe";
    $env:PYTHONPATH="$env:MINICONDA_PATH\envs\test-environment"
    
    echo "Miniconda environment information after installation of miniconda:";
    conda info -a;
    
    echo "Python interpreter information after installation of miniconda:"
    & $env:PYTHON_INTERPRETER --version;
}


switch ($env:CI_JOB) {
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
