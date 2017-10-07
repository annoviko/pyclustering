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
    echo "https://${GITHUB_TOKEN}:@github.com" > .git/credentials
    echo "Token = '$GITHUB_TOKEN'"

    echo "[DEPLOY]: Switch to branch '$TRAVIS_BRANCH'"
    git checkout $TRAVIS_BRANCH


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

GITHUB_TOKEN="CkWsTm14Emy0YneXlLuWOm8iWOlGVmYYNAdu0+oebuul34fXnhB63Fhq5aqIi6VwX8EA71ZkwcgnpQaKDzCKWL/u7IwPzu6wQcarxX6tET4rLj2dzQEFRBDmObPqSl73CnBBUxCGp4Ypc685QEZz2k3zMiGFR2zcx6TKg7TBiXivxITMy7OMR8b+il85oplBvF/Q8LL8kg8oU/KyW9BClHVeJfM0tlNKiZn4g2soiIQAIPz73xvyj/+NPVjYVrDTvtbJIa+DsZpwGEqZ4YIWXSj1SlX+XOg1LI2zO6JzK02yMKwnSCrMhwAXiLPjAOW7pNk2XqMtQVHJueo+QL30gdWh3DNR7seXkqptA/7pZsnjxl3MfRzoW673J04kkZZ/NDo384Es8xGLVeM2gjsKYgtV6fcx4RmKG9a4n7BT5skAt5HdHvAFcCfW5mLdBiSgK3K5n7j11USp++J9GKU7Qzz7Q073jnjtgGB3Rog1/uz3PJ96FyxqOUxw4pvqWJv4XiEyEuSK6JuCkUIyrtVVU5oglHgtetLO8kPlDIenj5ktE8su8BU9gAYXJ9pKSyOTewBykcfrGaUqeJ6D/Lo8N49NjhEkOAVhT1ZQ2UB41i0fn1mUeEWrv2gP1QI/MM3fVjyc01Wg7DDPfCl42i+/p8Vc2HKUUJyzOZnCbIm5goo="

run_deploy_job
