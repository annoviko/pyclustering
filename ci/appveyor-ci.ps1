$env:CCORE_X64_BINARY_PATH = "pyclustering\core\x64\win\ccore.dll"


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
    
    & $env:PYTHON_INTERPRETER pyclustering\tests\tests_runner.py --integration
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


function job_deploy() {
    echo "[DEPLOY]: Deploy (upload windows binary file to github)";
    
    git config --global user.email "pyclustering@yandex.ru";
    git config --global user.name "AppVeyor";

    git config credential.helper "store --file=.git\credentials";
    echo "https://$env:GITHUB_TOKEN:@github.com" > .git\credentials;
    git config credential.helper "store --file=.git\credentials";


    echo "[DEPLOY]: Prepare copy for pushing (reset, checkout, pull)";
    git reset --hard;
    git checkout $env:APPVEYOR_REPO_BRANCH;
    git pull;


    echo "[DEPLOY]: Prepare binary folder";
    mkdir pyclustering\core\x64\win;

    download_binary;

    echo "[DEPLOY]: Add changes for commit";
    echo "windows ccore x64 build version: '$env:APPVEYOR_BUILD_NUMBER'" > pyclustering\core\x64\win\.win.info;
    git add pyclustering\core\x64\win\.win.info;
    git add pyclustering\core\x64\win\ccore.dll;


    echo "[DEPLOY]: Display status and changes";
    git status;


    echo "[DEPLOY]: Push changes to github repository";
    git commit . -m "[appveyor][ci skip] push new ccore version '$env:APPVEYOR_BUILD_NUMBER'";
    git push;
}


function install_miniconda() {
    $env:PATH="$env:PATH;$env:MINICONDA_PATH\Scripts";
    
    echo "Starting process of installation of miniconda.";
    
    conda config --set always_yes yes --set changeps1 no;
    conda update -q conda;
    conda create -q -n test-environment python=3.4 numpy scipy matplotlib Pillow;
    
    echo "Activating environment for powershell manually."
    $env:PYTHON_INTERPRETER = "$env:MINICONDA_PATH\envs\test-environment\python.exe";
    $env:PYTHONPATH = "$env:MINICONDA_PATH\envs\test-environment"
    
    echo "Miniconda environment information after installation of miniconda:";
    conda info -a;
    
    echo "Python interpreter information after installation of miniconda:"
    & $env:PYTHON_INTERPRETER --version;
}


function download_binary() {
    echo "[DEPLOY]: Download binary file"

    # Obtain link for download
    $env:BUILD_FOLDER = "windows"
    $env:BINARY_FOLDER = $env:APPVEYOR_BUILD_NUMBER;
    $env:BINARY_FILEPATH = "$env:APPVEYOR_REPO_BRANCH%2F$env:BUILD_FOLDER%2F$env:BINARY_FOLDER%2Fccore.dll"

    $env:RESPONSE = curl.exe -s -H "Authorization: OAuth $env:YANDEX_DISK_TOKEN" -X GET "https://cloud-api.yandex.net:443/v1/disk/resources/download?path=$env:BINARY_FILEPATH" | ConvertFrom-Json
    $env:DOWNLOAD_LINK = $env:RESPONSE.href;

    # Download binary
    curl.exe -s -H "Authorization: OAuth $env:YANDEX_DISK_TOKEN" -X GET $env:DOWNLOAD_LINK > pyclustering\core\x64\win\ccore.dll
}


function upload_binary() {
    echo "[CI Job]: Upload binary files to storage.";

    $env:BUILD_FOLDER = "windows";
    $env:BINARY_FOLDER = $env:APPVEYOR_BUILD_NUMBER;

    # Create folder for uploaded binary file
    curl.exe -H "Authorization: OAuth $env:YANDEX_DISK_TOKEN" -X PUT "https://cloud-api.yandex.net:443/v1/disk/resources?path=$env:APPVEYOR_REPO_BRANCH";
    curl.exe -H "Authorization: OAuth $env:YANDEX_DISK_TOKEN" -X PUT "https://cloud-api.yandex.net:443/v1/disk/resources?path=$env:APPVEYOR_REPO_BRANCH%2F$env:BUILD_FOLDER";
    curl.exe -H "Authorization: OAuth $env:YANDEX_DISK_TOKEN" -X PUT "https://cloud-api.yandex.net:443/v1/disk/resources?path=$env:APPVEYOR_REPO_BRANCH%2F$env:BUILD_FOLDER%2F$env:BINARY_FOLDER";

    # Obtain link for uploading
    $env:BINARY_FILEPATH = "$env:APPVEYOR_REPO_BRANCH%2F$env:BUILD_FOLDER%2F$env:BINARY_FOLDER%2Fccore.dll"
    $env:RESPONSE = curl.exe -s -H "Authorization: OAuth $env:YANDEX_DISK_TOKEN" -X GET https://cloud-api.yandex.net:443/v1/disk/resources/upload?path=$env:BINARY_FILEPATH | ConvertFrom-Json
    $env:UPLOAD_LINK = $env:RESPONSE.href;

    curl.exe -H "Authorization: OAuth $env:YANDEX_DISK_TOKEN" -X PUT $env:UPLOAD_LINK --upload-file $env:CCORE_X64_BINARY_PATH
}


switch ($env:CI_JOB) {
    "BUILD_WINDOWS_CCORE" {
        job_build_windows_ccore;
        upload_binary;
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
    "DEPLOY" {
        job_deploy;
        break;
    }
    default {
        echo "[CI Job] Unknown target '$CI_JOB'";
        exit 1;
    }
}
