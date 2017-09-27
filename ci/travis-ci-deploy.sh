run_deploy_job() {
    echo "[DEPLOY]: Deploy (upload linux binary file to github)"
    
    
    git config --global user.email "travis@travis-ci.org"
    git config --global user.name "Travis CI"
    
    mkdir pyclustering/core/x64/linux
    echo "linux ccore x64 build version: '$TRAVIS_BUILD_NUMBER'" > pyclustering/core/x64/linux/.linux.info
    git add pyclustering/core/x64/linux/.linux.info
    
    git commit . -m "[travis-ci][ci skip] push new ccore version '$TRAVIS_BUILD_NUMBER'"
    git push
}


run_deploy_job