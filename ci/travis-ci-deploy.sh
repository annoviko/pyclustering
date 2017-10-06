run_deploy_job() {
    echo "[DEPLOY]: Deploy (upload linux binary file to github)"
    
    git config --global user.email "travis@travis-ci.org"
    git config --global user.name "Travis CI"
    
    echo "[DEPLOY]: Switch to branch '$TRAVIS_BRANCH'"
    git checkout $TRAVIS_BRANCH
    
    echo "[DEPLOY]: Pull changes to make push clean"
    git pull
    
    echo "[DEPLOY]: Display status and changes"
    git status
    git diff
    
    echo "[DEPLOY]: Prepare changes and commit them"
    mkdir pyclustering/core/x64/linux
    echo "linux ccore x64 build version: '$TRAVIS_BUILD_NUMBER'" > pyclustering/core/x64/linux/.linux.info
    git add pyclustering/core/x64/linux/.linux.info
    git status
    git diff
    
    echo "[DEPLOY]: Push changes to github repository"
    git commit . -m "[travis-ci][ci skip] push new ccore version '$TRAVIS_BUILD_NUMBER'"
    git push --quiet
}


run_deploy_job