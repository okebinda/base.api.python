#!/usr/bin/env bash

############################################
#
# Deploy
#
#  Logs in to the application server, downloads a ZIP package of the Python
#  application and its dependencies (created by the make.sh script) from an S3
#  bucket, installs and activates it. If the package already exists on the
#  server it will skip the download step and reactivate the previous package - 
#  in this way it can act as a rollback operation.
#
#  Usage: deploy.sh [OPTIONS] [API NAME] [VERSION] [FILENAME]
#
#  Arguments:
#   API NAME: [required] Specifies which API to package: 'public' or 'admin'
#   VERSION: [required] The version (branch) label to deploy to, such as '1.0',
#            '2.3' or 'beta'.
#   FILENAME: [required] The filename ZIP package in the S3 bucket for deployment.
#
#  Options:
#   -p : Promote the new package to serving the live endpoint.
#   -F : Force re-download of package if it already exists.
#   -P : Deply the package to the production server. Default is to user the development
#        environment.
#
#  Requirements:
#    1) Add SSH key to VM
#    2) Use SSH to login to server interactively first time to accept server's public key
#    3) Configure awscli on server
#
#  Examples:
#
#    * Copy the package for the public API to the development server using the 1.1 version
#      label.
#
#        ./deploy.sh public 1.1 host.domain.com-1.1.4.165.zip
#
#    * Deploy the package for the admin API to the development server using the 2.3 version
#      label, update the web server's live symlink to point to the new package directory and
#      restart the systemd service to reload the bytecode.
#
#        ./deploy.sh -p admin 2.3 host.domain.com-2.3.4.165.zip
#
#    * Deploy the package for the public API to the production server using the 1.5
#      version label, update the web server's live symlink to point to the new package
#      directory and restart the systemd service to reload the bytecode.
#
#        ./deploy.sh -pP public 1.5 host.domain.com-1.5.1.048.zip
#
############################################

# app names -> subdomain names
declare -A apps=(
    [public]="api"
    [admin]="api.admin"
)

# environment -> base domain names
declare -A base_domain_names=(
    [development]="dev.domain.com"
    [production]="domain.com"
)

# environment -> servers
declare -A server_ip_or_hosts=(
    [development]="dev.domain.com"
    [production]="domain.com"
)

# params
BUCKET_NAME="code.domain.com"
SSH_KEY="/home/vagrant/.ssh/SSH_KEY.pem"
SERVER_USER="ubuntu"
SERVER_APP_USER="app_username"

# flags
PROMOTE_PACKAGE=false
FORCE_REDOWNLOAD=false
PRODUCTION_DEPLOYMENT=false

while getopts 'FpP' flag; do
  case "${flag}" in
      p) PROMOTE_PACKAGE=true ;;
      F) FORCE_REDOWNLOAD=true ;;
      P) PRODUCTION_DEPLOYMENT=true ;;
      *) error "Unexpected option ${flag}" ;;
    esac
done
shift $((OPTIND-1))

# INPUT CHECKS

if [ -z "$1" ];
then
    echo "Please specify an API name to package."
    echo "Usage: deploy.sh [OPTIONS] [API NAME] [VERSION] [FILENAME]"
    exit 0
else
    if [ ! -n "${apps[$1]}" ];
    then
        echo "'${1}' is not a valid API name."
        exit 0
    fi
fi

if [ -z "$2" ];
  then
    echo "Please specify a version to deploy."
    echo "Usage: deploy.sh [OPTIONS] [API NAME] [VERSION] [FILENAME]"
    exit 0
fi

if [ -z "$3" ];
  then
    echo "Please specify a filename in the S3 bucket [${BUCKET_NAME}] to deploy."
    echo "Usage: deploy.sh [OPTIONS] [API NAME] [VERSION] [FILENAME]"
    exit 0
fi

# DEPLOYMENT

# assign domains based on environment
if [ "$PRODUCTION_DEPLOYMENT" = true ]; then
    SERVER_IP_OR_HOST="${server_ip_or_hosts[production]}"
    APP_DOMAIN_NAME="${apps[$1]}.${base_domain_names[production]}"
else
    SERVER_IP_OR_HOST="${server_ip_or_hosts[development]}"
    APP_DOMAIN_NAME="${apps[$1]}.${base_domain_names[development]}"
fi

# assign directories and services
SERVER_DOWNLOAD_DIR="/home/${SERVER_USER}"
SERVER_APP_DIR="/home/${SERVER_APP_USER}/${APP_DOMAIN_NAME}"
SERVER_PROD_DIR="/var/www/vhosts/${APP_DOMAIN_NAME}"
SERVER_SERVICE_NAME="${APP_DOMAIN_NAME}"

# assign args to local vars
DEPLOY_VERSION=$2
FILE_NAME=$3

# parse the file id from the full filename
FILE_ID=$(basename "$FILE_NAME" .zip)

# log in to server
ssh -i $SSH_KEY "${SERVER_USER}@${SERVER_IP_OR_HOST}" << EOF

echo

# if package is already installed on server, skip download and unpacking
if [ -e "${SERVER_APP_DIR}/${DEPLOY_VERSION}/${FILE_ID}" ] && [ ! $FORCE_REDOWNLOAD = true ] ; then
    echo "${SERVER_APP_DIR}/${DEPLOY_VERSION}/${FILE_ID} already exists. Skipping download."
else

    # change to download directory
    if ! cd ${SERVER_DOWNLOAD_DIR} ; then
        echo "Could not change to ${SERVER_DOWNLOAD_DIR} directory. Aborting."
        exit
    fi

    # download package
    echo "Downloading package..."
    if ! aws s3 cp "s3://${BUCKET_NAME}/${FILE_NAME}" . ; then
        echo "Package download failed. Aborting."
        exit
    fi
    echo "Complete."

    # remove old files if they exist
    if [ $FORCE_REDOWNLOAD = true ] && [ -e "${SERVER_APP_DIR}/${DEPLOY_VERSION}/${FILE_ID}" ] ; then
        echo "Deleting existing package: ${SERVER_APP_DIR}/${DEPLOY_VERSION}/${FILE_ID}"
        sudo su ${SERVER_APP_USER} -c "rm -rf ${SERVER_APP_DIR}/${DEPLOY_VERSION}/${FILE_ID}"
    fi

    # change to application directory
    if ! cd ${SERVER_APP_DIR} ; then
        echo "Could not change to ${SERVER_APP_DIR} directory. Aborting."
        exit
    fi

    # create new application build directory
    if ! sudo su ${SERVER_APP_USER} -c "mkdir -p ${DEPLOY_VERSION}/${FILE_ID}" ; then
        echo "Could not create ${DEPLOY_VERSION}/${FILE_ID} directory. Aborting."
        exit
    fi

    # change to new application build directory
    if ! sudo su ${SERVER_APP_USER} -c "cd ${SERVER_APP_DIR}/${DEPLOY_VERSION}/${FILE_ID}" ; then
        echo "Could not change to ${SERVER_APP_DIR}/${DEPLOY_VERSION}/${FILE_ID} directory. Aborting."
        exit
    fi

    # unzip package to app build directory
    echo "Extracting package..."
    if ! sudo su ${SERVER_APP_USER} -c "unzip -qo ${SERVER_DOWNLOAD_DIR}/${FILE_NAME} -d ${SERVER_APP_DIR}/${DEPLOY_VERSION}/${FILE_ID}" ; then
        echo "Could not unzip ${SERVER_DOWNLOAD_DIR}/${FILE_NAME} into ${SERVER_APP_DIR}/${DEPLOY_VERSION}/${FILE_ID}. Aborting."
        exit
    fi
    echo "Complete."

    # cleanup
    if ! rm "${SERVER_DOWNLOAD_DIR}/${FILE_NAME}" ; then
        echo "Could not delete ${SERVER_DOWNLOAD_DIR}/${FILE_NAME}."
    fi
    echo "Package download removed."
fi

# promote new package to production
if [ "${PROMOTE_PACKAGE}" = true ] ; then

    # symlink app build directory to production web server directory
    if ! sudo su ${SERVER_APP_USER} -c "ln -sfn ${SERVER_APP_DIR}/${DEPLOY_VERSION}/${FILE_ID} ${SERVER_PROD_DIR}/${DEPLOY_VERSION}" ; then
        echo "Could not symlink ${SERVER_APP_DIR}/${DEPLOY_VERSION}/${FILE_ID} to ${SERVER_PROD_DIR}/${DEPLOY_VERSION}. Aborting."
        exit
    fi
    echo "Symlink updated."

    # restart application service
    if ! sudo systemctl restart ${SERVER_SERVICE_NAME}-${DEPLOY_VERSION}.service ; then
        echo "Could not restat ${SERVER_SERVICE_NAME}-${DEPLOY_VERSION}.service. Aborting."
        exit
    fi
    echo "Service restarted."

    # update CHANGELOG
    sudo su ${SERVER_APP_USER} -c "echo \"$(date): [${DEPLOY_VERSION}] ${FILE_ID}\" >> ${SERVER_APP_DIR}/${DEPLOY_VERSION}/CHANGELOG.txt"
fi

echo 
echo "Deployment complete."
echo

EOF
