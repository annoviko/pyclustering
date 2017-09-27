#!/bin/bash


CCORE_LIB_NAME=ccore.so
CCORE_X64_BINARY_DIRECTORY=pyclustering/core/x64/linux/


run_deploy_job() {
    echo "[CI_JOB]: Deploy (upload linux binary file to github)"
    
    git config --global user.email "travis@travis-ci.org"
    git config --global user.name "Travis CI"
    
    echo "linux ccore x64 build version: $TRAVIS_BUILD_NUMBER" > $CCORE_X64_BINARY_DIRECTORY/.linux.info
    git add $CCORE_X64_BINARY_DIRECTORY/.linux.info
    
    git commit . -m "[travis-ci][ci skip] push new ccore version '$TRAVIS_BUILD_NUMBER'"
    git push
}