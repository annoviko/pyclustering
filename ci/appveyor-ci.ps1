$CI_JOB = $env:CI_JOB
$APPVEYOR_BUILD_FOLDER = $env:APPVEYOR_BUILD_FOLDER
#param([string]$CI_JOB)


function job_build_windows_ccore() {
    echo "[CI Job] CCORE building using Visual Studio on Windows platform."

    msbuild ccore\ccore.sln /t:ccore:Rebuild /p:configuration=Release
}


function job_ut_windows_ccore() {
    echo "[CI Job] CCORE unit-test building and running using Visual Studio on Windows platform."

    msbuild ccore\ccore.sln /t:utcore:Rebuild /p:configuration=Release
    cd ccore\Release;
    .\utcore.exe;
}


function job_build_cygwin_ccore() {
    echo "[CI Job] CCORE building using GCC on Cygwin platform.";

    & $CYGWIN_PATH -lc "cygcheck -dc cygwin";
    & $CYGWIN_PATH -lc "cd $APPVEYOR_BUILD_FOLDER; cd ccore; make $PROJECT_TARGET";
}


function job_ut_cygwin_ccore() {
    echo "[CI Job] CCORE unit-test building and running using Visual Studio on Windows platform.";
    
    & $CYGWIN_PATH -lc "cd $APPVEYOR_BUILD_FOLDER; cd ccore; make utrun";
}


function job_pyclustering_windows() {
    echo "[CI Job] Testing interaction between pyclustering and CCORE on Windows platform.";

    install_miniconda;

    $env:PATH="$env:PATH;$pwd.Path";

    job_build_windows_ccore;

    & $PYTHON_PATH\python.exe pyclustering\ut\__init__.py
}


function job_pyclustering_cygwin() {
    echo "[CI Job] Testing interaction between pyclustering and CCORE on Cygwin platform.";
    echo "[CI Job] Job is not ready yet.";
}


function install_miniconda() {
    $env:PATH="$env:PATH;$MINICONDA_PATH;$MINICONDA_PATH\Scripts";
    
    conda config --set always_yes yes --set changeps1 no;
    conda update -q conda;
    conda create -q -n test-environment python=3.4 numpy scipy matplotlib Pillow;
}


switch ($CI_JOB)
    {
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