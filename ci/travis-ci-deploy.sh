run_deploy_job() {
    echo "[DEPLOY]: Deploy (upload linux binary file to github)"

    local head_ref branch_ref
    head_ref=$(git rev-parse HEAD)
    if [[ $? -ne 0 || ! $head_ref ]]; then
        echo "[DEPLOY]: Failed to get HEAD reference"
        exit -1
    fi
    
    branch_ref=$(git rev-parse "$TRAVIS_BRANCH")
    if [[ $? -ne 0 || ! $branch_ref ]]; then
        echo "[DEPLOY]: Failed to get '$TRAVIS_BRANCH' reference"
        exit -2
    fi
    
    if [[ $head_ref != $branch_ref ]]; then
        echo "[DEPLOY]: HEAD ref ($head_ref) does not match '$TRAVIS_BRANCH' ref ($branch_ref)"
        echo "[DEPLOY]: Someone may have pushed new commits before this build cloned the repository"
        exit -3
    fi
    
    git config --global user.email "pyclustering@yandex.ru"
    git config --global user.name "Travis-CI"

	git config credential.helper "store --file=.git/credentials"
    echo "https://${GH_TOKEN}:@github.com" > .git/credentials
    git config credential.helper "store --file=.git/credentials"


    echo "[DEPLOY]: Pull changes to make push clean"
    git pull


    echo "[DEPLOY]: Prepare changes and commit them"
    mkdir pyclustering/core/x64/linux
    echo "linux ccore x64 build version: '$TRAVIS_BUILD_NUMBER'" > pyclustering/core/x64/linux/.linux.info
    git add pyclustering/core/x64/linux/.linux.info


    echo "[DEPLOY]: Display status and changes"
    git status


    echo "[DEPLOY]: Push changes to github repository"
    git commit . -m "[travis-ci][ci skip] push new ccore version '$TRAVIS_BUILD_NUMBER'"
    git push
}

run_deploy_job
