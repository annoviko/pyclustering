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


    echo "[DEPLOY]: Prepare binary folder"
    mkdir pyclustering/core/x64/linux

    download_binary

    echo "[DEPLOY]: Add changes for commit"
    echo "linux ccore x64 build version: '$TRAVIS_BUILD_NUMBER'" > pyclustering/core/x64/linux/.linux.info
    git add pyclustering/core/x64/linux/.linux.info
    git add pyclustering/core/x64/linux/ccore.so


    echo "[DEPLOY]: Display status and changes"
    git status


    echo "[DEPLOY]: Push changes to github repository"
    git commit . -m "[travis-ci][ci skip] push new ccore version '$TRAVIS_BUILD_NUMBER'"
    git push
}


download_binary() {
    echo "[DEPLOY]: Download binary file"

    # Obtain link for download
    BUILD_FOLDER=linux
    BINARY_FOLDER=$TRAVIS_BUILD_NUMBER
    BINARY_FILENAME=ccore.so
    
    DOWNLOAD_LINK=`curl -s -H "Authorization: OAuth $YANDEX_DISK_TOKEN" -X GET https://cloud-api.yandex.net:443/v1/disk/resources/download?path=$BUILD_FOLDER%2F$BINARY_FOLDER%2F$BINARY_FILENAME |\
        python3 -c "import sys, json; print(json.load(sys.stdin)['href'])"`

    curl -H "Authorization: OAuth $YANDEX_DISK_TOKEN" -o $DOWNLOAD_LINK

    # Copy to binary folder
    mv ccore.so pyclustering/core/x64/linux/ccore.so
}


run_deploy_job
