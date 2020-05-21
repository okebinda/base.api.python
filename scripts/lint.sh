#!/bin/sh

HIGHLIGHT_COLOR="\e[1;36m" # cyan
DEFAULT_COLOR="\e[0m"

export PIPENV_PIPFILE='/vagrant/application/Pipfile'

cd /vagrant/application

echo "\n${HIGHLIGHT_COLOR}Running bandit...${DEFAULT_COLOR}"
pipenv run bandit -r src/main/python/

echo "\n${HIGHLIGHT_COLOR}Running pyflakes...${DEFAULT_COLOR}"
pipenv run pyflakes src/main/python/

echo "\n${HIGHLIGHT_COLOR}Running pycodestyle...${DEFAULT_COLOR}"
pipenv run pycodestyle src/main/python/

echo "\n${HIGHLIGHT_COLOR}Running pylint...${DEFAULT_COLOR}"
pipenv run pylint src/main/python/*
