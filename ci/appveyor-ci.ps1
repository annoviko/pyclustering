#
# @authors Andrei Novikov (pyclustering@yandex.ru)
# @date 2014-2020
# @copyright BSD-3-Clause
#


$env:CCORE_64BIT_BINARY_PATH = "pyclustering\core\64-bit\win\pyclustering.dll"
$env:CCORE_32BIT_BINARY_PATH = "pyclustering\core\32-bit\win\pyclustering.dll"

$env:RESULT_SUCCESS = "Success";
$env:RESULT_FAILURE = "Failure";



function build_ccore_library($target, $platform, $configuration) {
    Write-Host "[CI] Build C++ pyclustering library (target: '$target') '$configuration' for Windows platform '$platform'." -ForegroundColor Green;

    msbuild ccore\ccore.sln /t:$target /p:configuration=$configuration /p:platform=$platform;

    if ($LastExitCode -ne 0) {
        Write-Error -Message "[CI] Build process for C++ pyclustering library (target: '$target') '$configuration' for Windows ($platform) is failed." -Category InvalidResult;
        $env:TESTING_RESULT = $env:RESULT_FAILURE;
    }

    Write-Host "[CI] C++ pyclustering library (target: '$target') '$configuration' for WINDOWS platform ($platform) is successfully built." -ForegroundColor Green;
}


function bvt_ccore_library($target, $platform, $configuration) {
    Write-Host "[CI] Run BVT for C++ pyclustering library '$target' ('$configuration', '$platform')." -ForegroundColor Green;

    msbuild ccore\ccore.sln /t:$target /p:configuration=$configuration /p:platform=$platform

    if ($LastExitCode -ne 0) {
        Write-Error -Message "[CI] Build process for C++ pyclustering library BVT '$target' is failed." -Category InvalidResult;
        Exit 1;
    }

    $smoke_test = "ccore\x64\$target.exe";

    & $smoke_test
    if ($LastExitCode -ne 0)
    {
        Write-Error -Message "[CI] The BVT for '$target' failed with code '$LastExitCode'.";
        Exit 1;
    }
}


function ut_ccore_library($target, $platform, $configuration) {
    Write-Host "[CI] Run UT for C++ pyclustering library '$target' ('$configuration', '$platform')." -ForegroundColor Green;

    msbuild ccore\ccore.sln /t:$target /p:configuration=$configuration /p:platform=$platform

    if ($LastExitCode -ne 0) {
        Write-Error -Message "[CI] Build process for C++ pyclustering library UT '$target' is failed." -Category InvalidResult;
        Exit 1;
    }

    cd ccore\tst;
    & $env:PYTHON_INTERPRETER ut-runner.py $target.exe
    if ($LastExitCode -ne 0) {
        Write-Error -Message "[CI] The UT for '$target' failed with code '$LastExitCode'.";
        Exit 1;
    }
    cd ..\..\;
}


function job_build_windows_ccore($platform_version) {
    Write-Host "[CI] Build C++ pyclustering library." -ForegroundColor Green;

    build_ccore_library pyclustering-shared x86 "Release";
    build_ccore_library pyclustering-shared x64 "Release";

    Write-Host "[CI] C++ pyclustering library is successfully built for Windows." -ForegroundColor Green;

    bvt_ccore_library bvt\bvt-shared x64 "Release"
    bvt_ccore_library bvt\bvt-static x64 "Release"

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
    Write-Host "[CI] Build and run unit-tests for C++ pyclustering library." -ForegroundColor Green;

    ut_ccore_library ut\ut-static x64 "Release"
    ut_ccore_library ut\ut-shared x64 "Release"

    Write-Host "[CI] Build and run unit-tests for C++ pyclustering library: SUCCESS." -ForegroundColor Green;
}


function job_build_cygwin_ccore() {
    Write-Host "[CI] C++ pyclustering library build for Cygwin." -ForegroundColor Green;

    & $env:CYGWIN_PATH -lc "cygcheck -dc cygwin";
    & $env:CYGWIN_PATH -lc "cd '$env:APPVEYOR_BUILD_FOLDER'; cd ccore; make ccore_64bit";
    if ($LastExitCode -ne 0) {
        Write-Error -Message "[CI] C++ pyclustering library build for Cygwin: FAILURE." -Category InvalidResult;
        $env:TESTING_RESULT = $env:RESULT_FAILURE;
        Exit 1;
    }
    
    Write-Host "[CI] C++ pyclustering library build for Cygwin: SUCCESS." -ForegroundColor Green;
}


function job_pyclustering_windows($platform_version) {
    Write-Host "[CI] Testing interaction between pyclustering and CCORE on Windows platform $platform_version." -ForegroundColor Green;

    if ($env:APPVEYOR_PULL_REQUEST_NUMBER) {
        Write-Host -Message "[CI] Integration tests are disabled for Pull Requests." -ForegroundColor Green;
        exit 0
    }

    install_miniconda $platform_version;

    Write-Host "[CI] Set path '$env:APPVEYOR_BUILD_FOLDER' to tested pyclustering library." -ForegroundColor Green;
    $env:PYTHONPATH = "$env:APPVEYOR_BUILD_FOLDER;$env:PYTHONPATH";

    Write-Host "[CI] Download built binary for platform '$platform_version'." -ForegroundColor Green;

    if ($platform_version -eq "x86") {
        download_binary 32-bit $env:CCORE_32BIT_BINARY_PATH
    }
    elseif ($platform_version -eq "x64") {
        download_binary 64-bit $env:CCORE_64BIT_BINARY_PATH
    }

    Write-Host "[CI] Starting integration testing using interpreter '$env:PYTHON_INTERPRETER'." -ForegroundColor Green;
    
    & $env:PYTHON_INTERPRETER pyclustering\tests\__main__.py --integration
    if ($LastExitCode -ne 0) {
        Write-Error -Message "[CI Job] Integration testing pyclustering <-> ccore for WINDOWS platform: FAILURE." -Category InvalidResult;
        $env:TESTING_RESULT = $env:RESULT_FAILURE;
        exit 1;
    }
    
    Write-Host "[CI] Integration testing pyclustering <-> ccore for WINDOWS platform: SUCCESS." -ForegroundColor Green;;
}


function download_miniconda($platform_version) {
    Write-Host "[CI] Download Miniconda." -ForegroundColor Green;
    
    $webclient = New-Object System.Net.WebClient;
    
    $filename = "";
    if ($platform_version -eq "x86") {
        $filename = "Miniconda3-4.3.27-Windows-x86.exe";
    }
    elseif ($platform_version -eq "x64") {
        $filename = "Miniconda3-4.3.27-Windows-x86_64.exe";
    }
    else {
        Write-Error -Message "[CI] Unknown platform of Miniconda is specified '$platform_version'." -Category InvalidArgument;
        Exit 1;
    }
    

    $filepath = $pwd.Path + "\" + $filename
    $url = "https://repo.continuum.io/miniconda/" + $filename;


    Write-Host "[CI] Start downloading process from link '$url' to '$filepath'." -ForegroundColor Green;

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
        Write-Host "[CI] Installation file has been download to '$filepath'." -ForegroundColor Green;
    }
    else {
        Write-Error -Message  "[CI] Miniconda has not been downloaded." -Category ResourceUnavailable;
        Exit 1;
    }
    
    
    Write-Host "[CI] Start installing process using '$filepath'." -ForegroundColor Green;
    
    $env:MINICONDA_PATH = "C:\Specific-Miniconda";
    $args = "/InstallationType=AllUsers /S /AddToPath=1 /RegisterPython=1 /D=$env:MINICONDA_PATH";
    
    Start-Process -FilePath $filepath -ArgumentList $args -Wait -Passthru;
    
    if (Test-Path $env:MINICONDA_PATH) {
        Write-Host "[CI] Miniconda has been successfully installed to '$env:MINICONDA_PATH'." -ForegroundColor Green;
        
        Remove-Item $filepath;
    }
    else {
        Write-Host "[CI] Miniconda has not been installed." -ForegroundColor Green;
        Exit 1;
    }


    Write-Host "[CI] Set miniconda to PATH variable." -ForegroundColor Green;
    $env:PATH = "$env:PATH;$env:MINICONDA_PATH\Scripts";
}


function install_miniconda($platform_version) {
    Write-Host "[CI] Starting process of installation of miniconda." -ForegroundColor Green;
    
    download_miniconda $platform_version;
    
    conda config --set always_yes true;
    
    conda install -q conda;
    
    conda create -q -n test-environment python=3.5;
    conda install -q -n test-environment mkl numpy scipy matplotlib pillow;

    # Download pillow from the channel because of troubles on default channel.
    # conda install --channel conda-forge pillow=5.2.0;

    Write-Host "[CI] Activating environment for powershell manually (activate does not work)." -ForegroundColor Green;
    activate test-environment;
    
    $env:PYTHON_INTERPRETER = "$env:MINICONDA_PATH\envs\test-environment\python.exe";
    $env:PYTHONPATH = "$env:MINICONDA_PATH\envs\test-environment";
    
    $env:PATH = "$env:MINICONDA_PATH\envs\test-environment;$env:PATH";
    $env:PATH = "$env:MINICONDA_PATH\envs\test-environment\Scripts;$env:PATH";
    $env:PATH = "$env:MINICONDA_PATH\envs\test-environment\Library\bin;$env:PATH";


    Write-Host "[CI] Miniconda environment information after installation of miniconda:" -ForegroundColor Green;
    conda info -a;

    Write-Host "[CI] Python interpreter information after installation of miniconda:" -ForegroundColor Green;
    & $env:PYTHON_INTERPRETER --version;
}


function download_binary($platform_version, $binary_path) {
    Write-Host "[CI]: Download binary file" -ForegroundColor Green;

    # Obtain link for download
    $env:BUILD_FOLDER = "windows";
    $env:BINARY_FOLDER = $env:APPVEYOR_BUILD_NUMBER;
    $env:BINARY_FILEPATH = "/$env:APPVEYOR_REPO_BRANCH/$env:BUILD_FOLDER/$platform_version/$env:BINARY_FOLDER/pyclustering.dll";

    & $env:PYTHON ci/cloud $env:YANDEX_DISK_TOKEN download $env:BINARY_FILEPATH $binary_path
    if ($LastExitCode -ne 0) {
        Write-Error -Message "[CI] Impossible to download C++ pyclustering binary (platform '$platform_version') to '$binary_path'." -Category InvalidResult;
        $env:TESTING_RESULT = $env:RESULT_FAILURE;
        exit 1;
    }
}


function upload_binary($platform_version, $binary_path) {
    Write-Host "[CI]: Upload binary files (platform: '$platform_version', binary: '$binary_path') to the storage." -ForegroundColor Green;

    $env:BUILD_FOLDER = "windows";
    $env:BINARY_FOLDER = $env:APPVEYOR_BUILD_NUMBER;

    # Create folder for uploaded binary file
    & $env:PYTHON ci/cloud $env:YANDEX_DISK_TOKEN mkdir "/$env:APPVEYOR_REPO_BRANCH"
    & $env:PYTHON ci/cloud $env:YANDEX_DISK_TOKEN mkdir "/$env:APPVEYOR_REPO_BRANCH/$env:BUILD_FOLDER"
    & $env:PYTHON ci/cloud $env:YANDEX_DISK_TOKEN mkdir "/$env:APPVEYOR_REPO_BRANCH/$env:BUILD_FOLDER/$platform_version"
    & $env:PYTHON ci/cloud $env:YANDEX_DISK_TOKEN mkdir "/$env:APPVEYOR_REPO_BRANCH/$env:BUILD_FOLDER/$platform_version/$env:BINARY_FOLDER"

    # Upload binary file
    $env:BINARY_FILEPATH = "/$env:APPVEYOR_REPO_BRANCH/$env:BUILD_FOLDER/$platform_version/$env:BINARY_FOLDER/pyclustering.dll";

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


if ($env:APPVEYOR_REPO_COMMIT_MESSAGE -Match "\[build-only-docs\]") {
    Write-Host "Option '[build-only-docs]' is detected, sources will not be built, checked, verified and published." -ForegroundColor Green;
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
    "PYCLUSTERING_WINDOWS_X64" {
        job_pyclustering_windows x64;
        break; 
    }
    "PYCLUSTERING_WINDOWS_X86" {
        job_pyclustering_windows x86;
        break;
    }
    default {
        Write-Error -Message "[CI] Unknown target is specified '$CI_JOB'"  -Category InvalidArgument;
        exit 1;
    }
}
