#!/bin/sh

############################
#
# BASE.API.PYTHON.VM
#
#  Development Bootstrap
#
#  Ubuntu 18.04
#  https://www.ubuntu.com/
#
#  Packages:
#   Python3
#   PostgreSQL
#   Nginx
#   vim tmux screen git zip
#   awscli
#   ansible
#
#  author: okebinda
#  date: October, 2019
#
############################


#################
#
# System Updates
#
#################

# get list of updates
apt-get update

# update all software
apt-get upgrade -y


###################
#
# Install Ansible
#
###################

apt install software-properties-common
apt-add-repository --yes --update ppa:ansible/ansible
apt install ansible -y
chown -R vagrant:vagrant /home/vagrant.ansible/
cp /vagrant/provision/development/templates/etc/ansible/hosts /etc/ansible/hosts


################
#
# Install Tools
#
################

apt-get install vim tmux screen git zip -y

# install AWS command line interface
apt-get install awscli -y


#####################
#
# Install PostgreSQL
#
#####################

# @ref: https://www.digitalocean.com/community/tutorials/how-to-install-and-use-postgresql-on-ubuntu-18-04
apt-get install postgresql postgresql-contrib -y
apt-get install python-psycopg2 -y
apt-get install libpq-dev -y
adduser --disabled-password --gecos "" api_admin
su postgres -c "psql -c \"CREATE USER api_admin WITH PASSWORD 'passpass';\""
su postgres -c "createdb api_db_dev -O api_admin"
su postgres -c "createdb api_db_test -O api_admin"
# su postgres -c "psql -c \"create extension pgcrypto;\""

# allow PostgreSQL access for local development
ufw allow 5432
sed -i "s/^#\?listen_addresses =.*/listen_addresses = '*'/g" /etc/postgresql/10/main/postgresql.conf
echo "
host    all             all              0.0.0.0/0                       md5
host    all             all              ::/0                            md5
" >> /etc/postgresql/10/main/pg_hba.conf
systemctl restart postgresql


########################
#
# Install Python Tools
#
########################

apt-get install python3-pip python3-dev build-essential -y
apt-get install python3-virtualenv virtualenvwrapper -y
apt-get install python3-pexpect -y
apt-get install libffi-dev -y


################
#
# Install Nginx
#
################

apt-get install nginx -y
ufw allow 'Nginx Full'
systemctl enable nginx.service


##################
#
# Configure Nginx
#
##################

mkdir -p /var/www/vhosts
ln -s /vagrant/application /var/www/vhosts/base.api.python.vm
cp /vagrant/provision/development/templates/etc/nginx/sites-available/base.api.python.vm.conf /etc/nginx/sites-available/base.api.python.vm.conf
ln -s /etc/nginx/sites-available/base.api.python.vm.conf /etc/nginx/sites-enabled/base.api.python.vm.conf
cp /vagrant/provision/development/templates/etc/nginx/sites-available/base.api.admin.python.vm.conf /etc/nginx/sites-available/base.api.admin.python.vm.conf
ln -s /etc/nginx/sites-available/base.api.admin.python.vm.conf /etc/nginx/sites-enabled/base.api.admin.python.vm.conf
systemctl restart nginx


###############
#
# VIM Settings
#
###############

su vagrant <<EOSU
echo 'syntax enable
set hidden
set history=100
set number
filetype plugin indent on
set tabstop=4
set shiftwidth=4
set expandtab' > ~/.vimrc
EOSU
