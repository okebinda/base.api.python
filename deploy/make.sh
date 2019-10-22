#!/usr/bin/env bash

############################################
#
# Make
#
#  Creates a ZIP package of the Python application and its dependencies.
#
#  Usage: make.sh [OPTIONS] [API NAME] [TAG]
#
#  Arguments:
#   API NAME: [required] Specifies which API to package: 'public' or 'admin'
#   TAG:      [optional] Appends the argument to the package name for versioning.
#             Default behavior is to use the current Unix timestamp.
#
#  Options:
#   -d : Package dependencies only - exclude runtime environment and web
#        resources (useful for Lambda).
#   -t : Run test suite on package.
#   -u : Upload package to S3 bucket.
#
#  Requirements:
#    1) Configure awscli on VM (for -u option)
#
#  Examples:
#
#    * Create a default package for the public api with a full runtime
#      environment in the packages directory. Appends the Unix timestamp to
#      package name for versioning.
#
#        ./make.sh public
#
#    * Create a default package with for the public api a full runtime
#      environment in the packages directory. Appends the first argument to
#      package name for versioning.
#
#        ./make.sh public 1.0.2
#
#    * Create a default package for the admin api with a full runtime
#      environment in the packages directory. Run unit tests on package and
#      upload to S3 bucket. Appends the first argument to package name for
#      versioning.
#
#        ./make.sh -tu admin 1.4.12
#
#    * Create a package for the public api with no runtime environment,
#      installing the dependencies in the root directory next to the
#      application source code. Appends the first argument to package name
#      for versioning.
#
#        ./make.sh -d public 2.3.0
#
############################################

# app names -> domain names
declare -A apps=(
    [public]="api.domain.com"
    [admin]="api.admin.domain.com"
)

# pip dependencies (not in Pipfile)
pip_install=('uwsgi' 'pipenv')

# aws params
BUCKET_NAME="code.domain.com"

# directories
BASE_DIR="/vagrant"
APP_DIR="${BASE_DIR}/application"
APP_SRC_DIR="${BASE_DIR}/application/src"
APP_WEB_DIR="${BASE_DIR}/application/web"
PACKAGE_DIR="${BASE_DIR}/deploy/packages"
TMP_DIR="${BASE_DIR}/deploy/tmp"

# app names -> unit tests
declare -A app_tests=(
    [public]="${BASE_DIR}/tests/api_public/functional/run.py"
    [admin]="${BASE_DIR}/tests/api_admin/functional/run.py"
)

# app names -> directories to exclude from package
declare -A app_exclude=(
    [public]="admin"
    [admin]="public"
)


# flags
DEPENDENCIES_ONLY=false
RUN_TEST_SUITE=false
UPLOAD_PACKAGE=false

while getopts 'dtu' flag; do
  case "${flag}" in
      d) DEPENDENCIES_ONLY=true ;;
      t) RUN_TEST_SUITE=true ;;
      u) UPLOAD_PACKAGE=true ;;
      *) error "Unexpected option ${flag}" ;;
    esac
done
shift $((OPTIND-1))

# INPUT CHECKS

if [ -z "$1" ];
then
    echo "Please specify an API name to package."
    echo "Usage: make.sh [OPTIONS] [API NAME] [TAG]"
    exit 0
else
    if [ ! -n "${apps[$1]}" ];
    then
        echo "'${1}' is not a valid API name."
        exit 0
    fi
fi

# more paths based on API name
PACKAGE_NAME="${apps[$1]}"
TEST_SCRIPT_PATH="${app_tests[$1]}"

# get tag or timestamp for filename
if [ $2 ];
then
    tag=$2
else
    tag=$(date +%s)
fi

# build filename
filename="${PACKAGE_DIR}/${PACKAGE_NAME}-${tag}.zip"

# make zip if file doesn't already exist
if [ -e $filename ];
then
    echo "Filename: '${filename}' already exists."
else
  
    # APPLICATION SOURCE

    #  zip options:
    #   -r: recursive
    #   -y: store symbolic links as symbolic links (i.e.: do not create a new copy)
    #   -9: compression level (max)
    #   -x: do not include directories and files within (__pycache__, ./migrations)
    BASE_SRC_DIR=$(basename $APP_SRC_DIR)
    if [ "$DEPENDENCIES_ONLY" = true ]
    then
        cd $APP_SRC_DIR
        zip -ry9 $filename * -x \*__pycache__\* ./migrations\* "./app/api_${app_exclude[$1]}"\* "./main_${app_exclude[$1]}.py"
    else
        cd "$APP_SRC_DIR/.."
        zip -ry9 $filename $BASE_SRC_DIR -x \*__pycache__\* $BASE_SRC_DIR/migrations\* "$BASE_SRC_DIR/app/api_${app_exclude[$1]}"\* "$BASE_SRC_DIR/main_${app_exclude[$1]}.py"
    fi

    # WEB RESOURCES

    #  zip options:
    #   -g: append (grow) to an existing archive (do not create a new one)
    #   -r: recursive
    #   -y: store symbolic links as symbolic links (i.e.: do not create a new copy)
    if [ ! "$DEPENDENCIES_ONLY" = true ]
    then
        cd "$APP_WEB_DIR/.."
        BASE_WEB_DIR=$(basename $APP_WEB_DIR)
        zip -gry $filename $BASE_WEB_DIR
    fi

    # ENVIRONMENT AND DEPENEDENCIES

    # initialize and activate temporary environment
    mkdir -p $TMP_DIR
    cd $TMP_DIR
    cp "${APP_DIR}/Pipfile" .
    cp "${APP_DIR}/Pipfile.lock" .
    virtualenv -p python3 env
    . ./env/bin/activate

    # install pip dependencies
    for i in "${pip_install[@]}"
    do
        pip install $i
    done

    # install pipenv dependencies
    pipenv install

    # make pipenv activation and scripts more portable
    sed -i 's/^VIRTUAL_ENV=.*/VIRTUAL_ENV="$( cd "$( dirname "${BASH_SOURCE[0]}" )\/.." >\/dev\/null 2>\&1 \&\& pwd )"/g' "${TMP_DIR}/env/bin/activate"
    grep -l '^#!/vagrant[^\s]*/python3' env/bin/* | while read -r line ; do
        shebang='#!\/usr\/bin\/awk BEGIN{a=ARGV[1];b="";for(i=1;i<ARGC;i++){b=b" \\""ARGV[i]"\\"";}sub(\/[a-z_.\\-]+$\/,"python3",a);system(a"\\t"b)}'
        sed -i "1s/.*/$shebang/" $line
    done

    #  zip options:
    #   -g: append (grow) to an existing archive (do not create a new one)
    #   -r: recursive
    #   -y: store symbolic links as symbolic links (do not create a new copy)
    if [ "$DEPENDENCIES_ONLY" = true ]
    then
        cd env/lib/python3.?/site-packages
        zip -gry $filename .
    else
        zip -gry $filename env
    fi

    # cleanup
    deactivate
    cd "$TMP_DIR/.."
    rm -rf $TMP_DIR

    # UNIT TESTS

    if [ "$RUN_TEST_SUITE" = true ]
    then
        echo ""
        echo "Preparing for unit tests..."
        mkdir -p $TMP_DIR
        unzip -qo $filename -d $TMP_DIR
        echo "Running unit tests:"
        . ../application/env/bin/activate
        if ! python -W ignore $TEST_SCRIPT_PATH -d  "${TMP_DIR}/${BASE_SRC_DIR}" ; then
            rm -rf $TMP_DIR
            echo ""
            echo "Unit tests failed. Aborting."
            exit
        fi
        rm -rf $TMP_DIR
    fi

    # UPLOAD TO S3

    if [ "$UPLOAD_PACKAGE" = true ]
    then
        # upload package to S3 bucket
        echo "Uploading package..."
        if ! aws s3 cp $filename "s3://${BUCKET_NAME}/${PACKAGE_NAME}-${tag}.zip" ; then
            echo "Package upload failed. Aborting."
            exit
        fi
        echo "Complete."
    fi

    echo
    echo "Package created: ${filename}"
    echo
fi
