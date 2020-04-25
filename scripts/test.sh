#!/bin/sh

HIGHLIGHT_COLOR="\e[1;36m" # cyan
DEFAULT_COLOR="\e[0m"

# activate virtual environment
cd /vagrant
. ./application/env/bin/activate

if [ "$1" = "public" ]
then

  # run public functional tests
  echo "\n${HIGHLIGHT_COLOR}Running public functional tests${DEFAULT_COLOR}"
  if [ ! -z "$2" ]
  then
    echo "Module: $2"
  fi
  python -W ignore tests/api_public/functional/run.py $2

elif [ "$1" = "admin" ]
then

  # run admin functional tests
  echo "\n${HIGHLIGHT_COLOR}Running admin functional tests${DEFAULT_COLOR}"
  if [ ! -z "$2" ]
  then
    echo "Module: $2"
  fi
  python -W ignore tests/api_admin/functional/run.py $2

else

  # run all functional tests
  echo "\n${HIGHLIGHT_COLOR}Running public functional tests${DEFAULT_COLOR}"
  python -W ignore tests/api_public/functional/run.py

  echo "\n${HIGHLIGHT_COLOR}Running admin functional tests${DEFAULT_COLOR}"
  python -W ignore tests/api_admin/functional/run.py

fi
