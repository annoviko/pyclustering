$env:CCORE_X64_BINARY_PATH = "pyclustering\core\x64\win\ccore.dll"

$env:RESULT_SUCCESS = "Success";
$env:RESULT_FAILURE = "Failure";


function job_build_windows_ccore() {
    echo "[CI Job] CCORE building using Visual Studio on Windows platform.";

    msbuild ccore\ccore.sln /t:ccore:Rebuild /p:configuration=Release;
    if ($LastExitCode -ne 0) {
        echo "Building CCORE library for WINDOWS platform: FAILURE.";
        $env:TESTING_RESULT = $env:RESULT_FAILURE;
        exit 1;
    }
    
    echo "Building CCORE library for WINDOWS platform: SUCCESS.";
}


function job_ut_windows_ccore() {
    echo "[CI Job] CCORE unit-test building and running using Visual Studio on Windows platform.";

    msbuild ccore\ccore.sln /t:utcore:Rebuild /p:configuration=Release;
    if ($LastExitCode -ne 0) {
        echo "[CI Job] Building of CCORE unit-test project for WINDOWS platform: FAILURE.";
        exit 1;
    }
    
    echo "[CI Job] Building of CCORE unit-test project for WINDOWS platform: SUCCESS.";
    
    cd ccore\Release;
    .\utcore.exe;
    if ($LastExitCode -ne 0) {
        echo "[CI Job] Unit-testing CCORE library for WINDOWS platform: FAILURE.";
        $env:TESTING_RESULT = $env:RESULT_FAILURE;
        exit 1;
    }
    
    echo "[CI Job] Unit-testing CCORE library for WINDOWS platform: SUCCESS.";
}


function job_build_cygwin_ccore() {
    echo "[CI Job] CCORE building using GCC on Cygwin platform.";

    & $env:CYGWIN_PATH -lc "cygcheck -dc cygwin";
    & $env:CYGWIN_PATH -lc "cd '$env:APPVEYOR_BUILD_FOLDER'; cd ccore; make ccore";
    if ($LastExitCode -ne 0) {
        echo "[CI Job] Building CCORE library for CYGWIN platform: FAILURE.";
        $env:TESTING_RESULT = $env:RESULT_FAILURE;
        exit 1;
    }
    
    echo "[CI Job] Building CCORE library for CYGWIN platform: SUCCESS.";
}


function job_ut_cygwin_ccore() {
    echo "[CI Job] CCORE unit-test building and running using Visual Studio on Windows platform.";
    
    & $env:CYGWIN_PATH -lc "cd '$env:APPVEYOR_BUILD_FOLDER'; cd ccore; make ut; make utrun";
    if ($LastExitCode -ne 0) {
        echo "Unit-testing CCORE library for WINDOWS platform: FAILURE.";
        $env:TESTING_RESULT = $env:RESULT_FAILURE;
        exit 1;
    }
    
    echo "Unit-testing CCORE library for CYGWIN platform: SUCCESS.";
}


function job_pyclustering_windows() {
    echo "[CI Job] Testing interaction between pyclustering and CCORE on Windows platform.";

    install_miniconda;

    echo "[CI Job] Set path '$env:APPVEYOR_BUILD_FOLDER' to tested pyclustering library."
    $env:PYTHONPATH = "$env:APPVEYOR_BUILD_FOLDER;$env:PYTHONPATH";

    job_build_windows_ccore;

    echo "[CI Job] Starting integration testing using interpreter '$env:PYTHON_INTERPRETER'.";
    
    & $env:PYTHON_INTERPRETER pyclustering\tests\tests_runner.py --integration
    if ($LastExitCode -ne 0) {
        echo "[CI Job] Integration testing pyclustering <-> ccore for WINDOWS platform: FAILURE.";
        $env:TESTING_RESULT = $env:RESULT_FAILURE;
        exit 1;
    }
    
    echo "[CI Job] Integration testing pyclustering <-> ccore for WINDOWS platform: SUCCESS.";
}


function job_pyclustering_cygwin() {
    echo "[CI Job] Testing interaction between pyclustering and CCORE on Cygwin platform.";
    echo "[CI Job] Job is not ready yet.";
}


function job_deploy() {
    echo "[DEPLOY]: Deploy (upload windows binary file to github)";
    if ($env:APPVEYOR_REPO_COMMIT_MESSAGE -NotMatch "\[publish\]") {
        echo "[DEPLOY]: Binary files will not be published to github repository (keyword '[publish]' is not specified).";
        exit 0;
    }
    
    if ($env:TESTING_RESULT -ne $env:RESULT_SUCCESS) {
        echo "[DEPLOY]: One of the build/testing job is failed - cancel deployment."
        exit 0;
    }

    git.exe config --global credential.helper store
    Add-Content "$env:USERPROFILE\.git-credentials" "https://$($env:GITHUB_TOKEN):x-oauth-basic@github.com`n"

    git.exe config --global user.email "pyclustering@yandex.ru";
    git.exe config --global user.name "AppVeyor";

    echo "[DEPLOY]: Prepare copy for pushing (reset, checkout, pull)";
    git.exe reset --hard;
    git.exe checkout $env:APPVEYOR_REPO_BRANCH;
    git.exe pull;


    echo "[DEPLOY]: Prepare binary folder";
    mkdir pyclustering\core\x64\win;

    download_binary;

    echo "[DEPLOY]: Add changes for commit";
    echo "windows ccore x64 build version: '$env:APPVEYOR_BUILD_NUMBER'" > pyclustering\core\x64\win\.win.info;
    git.exe add pyclustering\core\x64\win\.win.info;
    git.exe add pyclustering\core\x64\win\ccore.dll;


    echo "[DEPLOY]: Display status and changes";
    git.exe status;


    echo "[DEPLOY]: Push changes to github repository";
    git.exe commit -m "[appveyor][ci skip] push new ccore version '$env:APPVEYOR_BUILD_NUMBER'";
    git.exe push;
}


function download_miniconda() {
    echo "[CI Job] Download Miniconda.";
    
    $webclient = New-Object System.Net.WebClient;
    
    $filename = "Miniconda3-4.3.27-Windows-x86_64.exe";
    $filepath = $pwd.Path + "\" + $filename
    
    $url = "https://repo.continuum.io/miniconda/" + $filename;


    echo "[CI Job] Start downloading process from link '$url' to '$filepath'.";

    $retry_attempts = 3
    for($i = 0; $i -lt $retry_attempts; $i++){
        try {
            $webclient.DownloadFile($url, $filepath);
            break;
        }
        Catch [Exception]{
            Start-Sleep 1;
        }
    }
    
    if (Test-Path $filepath) {
        echo "[CI Job] Installation file has been download to '$filepath'.";
    }
    else {
        echo "[CI Job] Miniconda has not been downloaded."
        Exit 1;
    }
    
    
    
    echo "[CI Job] Start installing process using '$filepath'.";
    
    $env:MINICONDA_PATH = "C:\Specific-Miniconda\";
    $args = "/InstallationType=AllUsers /S /AddToPath=1 /RegisterPython=1 /D=$env:MINICONDA_PATH";
    
    Start-Process -FilePath $filepath -ArgumentList $args -Wait -Passthru;
    
    if (Test-Path $env:MINICONDA_PATH) {
        echo "[CI Job] Miniconda has been successfully installed to '$env:MINICONDA_PATH'.";
        
        Remove-Item $filepath;
    }
    else {
        echo "[CI Job] Miniconda has not been installed.";
        Exit 1;
    }

    
    
    echo "[CI Job] Set miniconda to PATH variable.";
    $env:PATH = "$env:PATH;$env:MINICONDA_PATH\Scripts";
}


function install_miniconda() {
    echo "[CI Job] Starting process of installation of miniconda.";
    
    download_miniconda;
    
    conda config --set always_yes true;
    
    conda install -q conda;
    
    conda create -q -n test-environment python=3.4 numpy=1.11.3 scipy=0.18.1 matplotlib Pillow;

    
    echo "[CI Job] Activating environment for powershell manually (activate does not work).";
    activate test-environment;
    
    $env:PYTHON_INTERPRETER = "$env:MINICONDA_PATH\envs\test-environment\python.exe";
    $env:PYTHONPATH = "$env:MINICONDA_PATH\envs\test-environment";
    
    $env:PATH = "$env:MINICONDA_PATH\envs\test-environment;$env:PATH";
    $env:PATH = "$env:MINICONDA_PATH\envs\test-environment\Scripts;$env:PATH";
    $env:PATH = "$env:MINICONDA_PATH\envs\test-environment\Library\bin;$env:PATH";


    echo "[CI Job] Miniconda environment information after installation of miniconda:";
    conda info -a;

    echo "[CI Job] Python interpreter information after installation of miniconda:";
    & $env:PYTHON_INTERPRETER --version;
}


function download_binary() {
    echo "[DEPLOY]: Download binary file"

    # Obtain link for download
    $env:BUILD_FOLDER = "windows"
    $env:BINARY_FOLDER = $env:APPVEYOR_BUILD_NUMBER;
    $env:BINARY_FILEPATH = "$env:APPVEYOR_REPO_BRANCH%2F$env:BUILD_FOLDER%2F$env:BINARY_FOLDER%2Fccore.dll"

    $env:DOWNLOAD_LINK = (curl.exe -H "Authorization: OAuth $env:YANDEX_DISK_TOKEN" -X GET "https://cloud-api.yandex.net:443/v1/disk/resources/download?path=$env:BINARY_FILEPATH" | ConvertFrom-Json).href

    # Download binary
    #curl.exe -s -H "Authorization: OAuth $env:YANDEX_DISK_TOKEN" -X GET $env:DOWNLOAD_LINK > pyclustering\core\x64\win\ccore.dll
    curl.exe $env:DOWNLOAD_LINK -o pyclustering\core\x64\win\ccore.dll;
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
    $env:UPLOAD_LINK = (curl.exe -H "Authorization: OAuth $env:YANDEX_DISK_TOKEN" -X GET https://cloud-api.yandex.net:443/v1/disk/resources/upload?path=$env:BINARY_FILEPATH | ConvertFrom-Json).href

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
