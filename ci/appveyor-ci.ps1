#
# @authors Andrei Novikov (pyclustering@yandex.ru)
# @date 2014-2020
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


$env:CCORE_64BIT_BINARY_PATH = "pyclustering\core\64-bit\win\ccore.dll"
$env:CCORE_32BIT_BINARY_PATH = "pyclustering\core\32-bit\win\ccore.dll"

$env:RESULT_SUCCESS = "Success";
$env:RESULT_FAILURE = "Failure";



function build_ccore_library($platform_version) {
    Write-Host "[CI] Build C++ pyclustering library for Windows platform ($platform_version)." -ForegroundColor Green;

    msbuild ccore\ccore.sln /t:ccore:Rebuild /p:configuration=Release /p:platform=$platform_version;

    if ($LastExitCode -ne 0) {
        Write-Error -Message "[CI] Build process for C++ pyclustering library for Windows ($platform_version) is failed." -Category InvalidResult;
        $env:TESTING_RESULT = $env:RESULT_FAILURE;
        Exit 1;
    }

    Write-Host "[CI] C++ pyclustering library for WINDOWS platform ($platform_version) is successfully built." -ForegroundColor Green;
}



function job_build_windows_ccore($platform_version) {
    Write-Host "[CI] Build C++ pyclustering library." -ForegroundColor Green;

    build_ccore_library x86;
    build_ccore_library x64;

    Write-Host "[CI] C++ pyclustering library is successfully built for Windows." -ForegroundColor Green;

    if ($env:APPVEYOR_PULL_REQUEST_NUMBER) {
        Write-Host -Message "[CI] Binaries are not uploaded in case of Pull Requests." -ForegroundColor Green;
        Exit 0;
    }

    Write-Host "[CI] Upload C++ pyclustering library binaries to the cloud." -ForegroundColor Green;

    upload_binary 32-bit $env:CCORE_32BIT_BINARY_PATH;
    upload_binary 64-bit $env:CCORE_64BIT_BINARY_PATH;

    Write-Host "[CI] Binaries are sucessfully uploaded." -ForegroundColor Green;
}



function job_ut_windows_ccore() {
    Write-Host "[CI Job] CCORE unit-test building and running using Visual Studio on Windows platform." -ForegroundColor Green;

    msbuild ccore\ccore.sln /t:utcore:Rebuild /p:configuration=Release;
    if ($LastExitCode -ne 0) {
        Write-Error -Message "[CI Job] Building of CCORE unit-test project for WINDOWS platform: FAILURE." -Category InvalidResult;
        Exit 1;
    }
    
    Write-Host "[CI Job] Building of CCORE unit-test project for WINDOWS platform: SUCCESS." -ForegroundColor Green;
    
    cd ccore\tst;
    & $env:PYTHON_INTERPRETER ut-runner.py
    if ($LastExitCode -ne 0) {
        Write-Error -Message "[CI Job] Unit-testing CCORE library for WINDOWS platform: FAILURE." -Category InvalidResult;
        $env:TESTING_RESULT = $env:RESULT_FAILURE;
        Exit 1;
    }
    
    Write-Host "[CI Job] Unit-testing CCORE library for WINDOWS platform: SUCCESS." -ForegroundColor Green;
}



function job_build_cygwin_ccore() {
    Write-Host "[CI Job] CCORE building using GCC on Cygwin platform." -ForegroundColor Green;

    & $env:CYGWIN_PATH -lc "cygcheck -dc cygwin";
    & $env:CYGWIN_PATH -lc "cd '$env:APPVEYOR_BUILD_FOLDER'; cd ccore; make ccore_64bit";
    if ($LastExitCode -ne 0) {
        Write-Error -Message "[CI Job] Building CCORE library for CYGWIN platform: FAILURE." -Category InvalidResult;
        $env:TESTING_RESULT = $env:RESULT_FAILURE;
        Exit 1;
    }
    
    Write-Host "[CI Job] Building CCORE library for CYGWIN platform: SUCCESS." -ForegroundColor Green;
}



function job_ut_cygwin_ccore() {
    Write-Host "[CI Job] CCORE unit-test building and running using Visual Studio on Windows platform." -ForegroundColor Green;
    
    & $env:CYGWIN_PATH -lc "cd '$env:APPVEYOR_BUILD_FOLDER'; cd ccore; make ut; make utrun";
    if ($LastExitCode -ne 0) {
        Write-Error -Message "Unit-testing CCORE library for WINDOWS platform: FAILURE." -Category InvalidResult;
        $env:TESTING_RESULT = $env:RESULT_FAILURE;
        Exit 1;
    }
    
    Write-Host "Unit-testing CCORE library for CYGWIN platform: SUCCESS." -ForegroundColor Green;
}



function job_pyclustering_windows($platform_version) {
    Write-Host "[CI Job] Testing interaction between pyclustering and CCORE on Windows platform $platform_version." -ForegroundColor Green;

    if ($env:APPVEYOR_PULL_REQUEST_NUMBER) {
        Write-Host -Message "[CI Job] Integration tests are disabled for Pull Requests." -ForegroundColor Green;
        exit 0
    }

    install_miniconda $platform_version;

    Write-Host "[CI Job] Set path '$env:APPVEYOR_BUILD_FOLDER' to tested pyclustering library." -ForegroundColor Green;
    $env:PYTHONPATH = "$env:APPVEYOR_BUILD_FOLDER;$env:PYTHONPATH";

    Write-Host "[CI Job] Download built binary for platform '$platform_version'." -ForegroundColor Green;

    if ($platform_version -eq "x86") {
        download_binary 32-bit $env:CCORE_32BIT_BINARY_PATH
    }
    elseif ($platform_version -eq "x64") {
        download_binary 64-bit $env:CCORE_64BIT_BINARY_PATH
    }

    Write-Host "[CI Job] Starting integration testing using interpreter '$env:PYTHON_INTERPRETER'." -ForegroundColor Green;
    
    & $env:PYTHON_INTERPRETER pyclustering\tests\__main__.py --integration
    if ($LastExitCode -ne 0) {
        Write-Error -Message "[CI Job] Integration testing pyclustering <-> ccore for WINDOWS platform: FAILURE." -Category InvalidResult;
        $env:TESTING_RESULT = $env:RESULT_FAILURE;
        exit 1;
    }
    
    Write-Host "[CI Job] Integration testing pyclustering <-> ccore for WINDOWS platform: SUCCESS." -ForegroundColor Green;;
}



function job_pyclustering_cygwin() {
    Write-Host "[CI Job] Testing interaction between pyclustering and CCORE on Cygwin platform." -ForegroundColor Yellow;
    Write-Host "[CI Job] Job is not ready yet." -ForegroundColor Yellow;
}



function job_deploy() {
    Write-Host "[DEPLOY]: Deploy (upload windows binary file to github)";
    if ($env:APPVEYOR_REPO_COMMIT_MESSAGE -NotMatch "\[publish\]") {
        Write-Host "[DEPLOY]: Binary files will not be published to github repository (keyword '[publish]' is not specified)." -ForegroundColor Green;
        Exit 0;
    }
    
    if ($env:TESTING_RESULT -ne $env:RESULT_SUCCESS) {
        Write-Host "[DEPLOY]: One of the build/testing job is failed - cancel deployment." -ForegroundColor Green;
        Exit 0;
    }

    git.exe config --global credential.helper store
    Add-Content "$env:USERPROFILE\.git-credentials" "https://$($env:GITHUB_TOKEN):x-oauth-basic@github.com`n"

    git.exe config --global user.email "pyclustering@yandex.ru";
    git.exe config --global user.name "AppVeyor";

    Write-Host "[DEPLOY]: Prepare copy for pushing (reset, checkout, pull)" -ForegroundColor Green;
    git.exe reset --hard;
    git.exe checkout $env:APPVEYOR_REPO_BRANCH;
    git.exe pull;


    Write-Host "[DEPLOY]: Prepare binary folder" -ForegroundColor Green;
    mkdir pyclustering\core\64-bit\win;

    download_binary 32-bit $env:CCORE_32BIT_BINARY_PATH;
    download_binary 64-bit $env:CCORE_64BIT_BINARY_PATH;

    Write-Host "[DEPLOY]: Add changes for commit" -ForegroundColor Green;

    Write-Host "windows ccore 32-bit build version: '$env:APPVEYOR_BUILD_NUMBER'" > pyclustering\core\32-bit\win\.win.info;
    Write-Host "windows ccore 64-bit build version: '$env:APPVEYOR_BUILD_NUMBER'" > pyclustering\core\64-bit\win\.win.info;
    
    git.exe add pyclustering\core\32-bit\win\.win.info;
    git.exe add pyclustering\core\32-bit\win\ccore.dll;

    git.exe add pyclustering\core\64-bit\win\.win.info;
    git.exe add pyclustering\core\64-bit\win\ccore.dll;

    Write-Host "[DEPLOY]: Display status and changes" -ForegroundColor Green;
    git.exe status;


    Write-Host "[DEPLOY]: Push changes to github repository" -ForegroundColor Green;
    git.exe commit -m "[appveyor][ci skip] push new ccore version '$env:APPVEYOR_BUILD_NUMBER'";
    git.exe push;
}



function download_miniconda($platform_version) {
    Write-Host "[CI Job] Download Miniconda." -ForegroundColor Green;
    
    $webclient = New-Object System.Net.WebClient;
    
    $filename = "";
    if ($platform_version -eq "x86") {
        $filename = "Miniconda3-4.3.27-Windows-x86.exe";
    }
    elseif ($platform_version -eq "x64") {
        $filename = "Miniconda3-4.3.27-Windows-x86_64.exe";
    }
    else {
        Write-Error -Message "[CI Job] Unknown platform of Miniconda is specified '$platform_version'." -Category InvalidArgument;
        Exit 1;
    }
    

    $filepath = $pwd.Path + "\" + $filename
    $url = "https://repo.continuum.io/miniconda/" + $filename;


    Write-Host "[CI Job] Start downloading process from link '$url' to '$filepath'." -ForegroundColor Green;

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
        Write-Host "[CI Job] Installation file has been download to '$filepath'." -ForegroundColor Green;
    }
    else {
        Write-Error -Message  "[CI Job] Miniconda has not been downloaded." -Category ResourceUnavailable;
        Exit 1;
    }
    
    
    Write-Host "[CI Job] Start installing process using '$filepath'." -ForegroundColor Green;
    
    $env:MINICONDA_PATH = "C:\Specific-Miniconda";
    $args = "/InstallationType=AllUsers /S /AddToPath=1 /RegisterPython=1 /D=$env:MINICONDA_PATH";
    
    Start-Process -FilePath $filepath -ArgumentList $args -Wait -Passthru;
    
    if (Test-Path $env:MINICONDA_PATH) {
        Write-Host "[CI Job] Miniconda has been successfully installed to '$env:MINICONDA_PATH'." -ForegroundColor Green;
        
        Remove-Item $filepath;
    }
    else {
        Write-Host "[CI Job] Miniconda has not been installed." -ForegroundColor Green;
        Exit 1;
    }

    
    
    Write-Host "[CI Job] Set miniconda to PATH variable." -ForegroundColor Green;
    $env:PATH = "$env:PATH;$env:MINICONDA_PATH\Scripts";
}



function install_miniconda($platform_version) {
    Write-Host "[CI Job] Starting process of installation of miniconda." -ForegroundColor Green;
    
    download_miniconda $platform_version;
    
    conda config --set always_yes true;
    
    conda install -q conda;
    
    conda create -q -n test-environment python=3.5;
    conda install -q -n test-environment mkl numpy scipy matplotlib pillow;

    # Download pillow from the channel because of troubles on default channel.
    # conda install --channel conda-forge pillow=5.2.0;

    Write-Host "[CI Job] Activating environment for powershell manually (activate does not work)." -ForegroundColor Green;
    activate test-environment;
    
    $env:PYTHON_INTERPRETER = "$env:MINICONDA_PATH\envs\test-environment\python.exe";
    $env:PYTHONPATH = "$env:MINICONDA_PATH\envs\test-environment";
    
    $env:PATH = "$env:MINICONDA_PATH\envs\test-environment;$env:PATH";
    $env:PATH = "$env:MINICONDA_PATH\envs\test-environment\Scripts;$env:PATH";
    $env:PATH = "$env:MINICONDA_PATH\envs\test-environment\Library\bin;$env:PATH";


    Write-Host "[CI Job] Miniconda environment information after installation of miniconda:" -ForegroundColor Green;
    conda info -a;

    Write-Host "[CI Job] Python interpreter information after installation of miniconda:" -ForegroundColor Green;
    & $env:PYTHON_INTERPRETER --version;
}



function download_binary($platform_version, $binary_path) {
    Write-Host "[CI Job]: Download binary file" -ForegroundColor Green;

    # Obtain link for download
    $env:BUILD_FOLDER = "windows";
    $env:BINARY_FOLDER = $env:APPVEYOR_BUILD_NUMBER;
    $env:BINARY_FILEPATH = "/$env:APPVEYOR_REPO_BRANCH/$env:BUILD_FOLDER/$platform_version/$env:BINARY_FOLDER/ccore.dll";

    & $env:PYTHON ci/cloud $env:YANDEX_DISK_TOKEN download $env:BINARY_FILEPATH $binary_path
    if ($LastExitCode -ne 0) {
        Write-Error -Message "[CI Job] Impossible to download CCORE binary (platform '$platform_version') to '$binary_path'." -Category InvalidResult;
        $env:TESTING_RESULT = $env:RESULT_FAILURE;
        exit 1;
    }
}



function upload_binary($platform_version, $binary_path) {
    Write-Host "[CI Job]: Upload binary files (platform: '$platform_version', binary: '$binary_path') to storage." -ForegroundColor Green;

    $env:BUILD_FOLDER = "windows";
    $env:BINARY_FOLDER = $env:APPVEYOR_BUILD_NUMBER;

    # Create folder for uploaded binary file
    & $env:PYTHON ci/cloud $env:YANDEX_DISK_TOKEN mkdir "/$env:APPVEYOR_REPO_BRANCH"
    & $env:PYTHON ci/cloud $env:YANDEX_DISK_TOKEN mkdir "/$env:APPVEYOR_REPO_BRANCH/$env:BUILD_FOLDER"
    & $env:PYTHON ci/cloud $env:YANDEX_DISK_TOKEN mkdir "/$env:APPVEYOR_REPO_BRANCH/$env:BUILD_FOLDER/$platform_version"
    & $env:PYTHON ci/cloud $env:YANDEX_DISK_TOKEN mkdir "/$env:APPVEYOR_REPO_BRANCH/$env:BUILD_FOLDER/$platform_version/$env:BINARY_FOLDER"

    # Upload binary file
    $env:BINARY_FILEPATH = "/$env:APPVEYOR_REPO_BRANCH/$env:BUILD_FOLDER/$platform_version/$env:BINARY_FOLDER/ccore.dll";

    & $env:PYTHON ci/cloud $env:YANDEX_DISK_TOKEN upload $binary_path $env:BINARY_FILEPATH
}



if ($env:APPVEYOR_REPO_COMMIT_MESSAGE -Match "\[no-build\]") {
    Write-Host "Option '[no-build]' is detected, sources will not be built, checked, verified and published." -ForegroundColor Green;
    Exit 0;
}

if ($env:APPVEYOR_REPO_COMMIT_MESSAGE -Match "\[build-only-osx\]") {
    Write-Host "Option '[build-only-osx]' is detected, sources will not be built, checked, verified and published." -ForegroundColor Green;
    Exit 0;
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
    "PYCLUSTERING_WINDOWS_X64" {
        job_pyclustering_windows x64;
        break; 
    }
    "PYCLUSTERING_WINDOWS_X86" {
        job_pyclustering_windows x86;
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
