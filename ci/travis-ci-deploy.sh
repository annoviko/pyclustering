run_deploy_job() {
    echo "[DEPLOY]: Deploy (upload linux binary file to github)"
    
    git config --global user.email "pyclustering@yandex.ru"
    git config --global user.name "Travis-CI"

	git config credential.helper "store --file=.git/credentials"
  	echo "https://${GH_TOKEN}:@github.com" > .git/credentials
    git config credential.helper "store --file=.git/credentials"


    echo "[DEPLOY]: Prepare copy for pushing (reset, checkout, pull)"
    git reset --hard
    git checkout $TRAVIS_BRANCH
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
