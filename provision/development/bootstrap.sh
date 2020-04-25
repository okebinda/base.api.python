#!/bin/sh

############################
#
# BASE.API.PYTHON.VM
#
#  Development Bootstrap
#
#  Ubuntu 20.04
#  https://www.ubuntu.com/
#
#  Packages:
#   Python3 3.8
#   PostgreSQL 12
#   Nginx 1.17
#   vim tmux screen git zip
#   awscli
#   ansible (not suppoted yet)
#
#  author: https://github.com/okebinda
#  date: April, 2020
#
############################


#################
#
# System Updates
#
#################

# get list of updates
apt update

# update all software
apt upgrade -y


###################
#
# Install Ansible
#
###################

#apt install -y software-properties-common
#apt-add-repository --yes --update ppa:ansible/ansible
#apt install ansible -y
#chown -R vagrant:vagrant /home/vagrant.ansible/
#cp /vagrant/provision/development/templates/etc/ansible/hosts /etc/ansible/hosts


################
#
# Install Tools
#
################

# install basic tools
apt install -y vim tmux screen git zip

# install AWS command line interface
apt install -y awscli


#####################
#
# Install PostgreSQL
#
#####################

# install PostgreSQL
apt install -y postgresql postgresql-contrib
apt install -y libpq-dev

# create development user and databases
su postgres -c "psql -c \"CREATE USER api_admin WITH PASSWORD 'passpass';\""
su postgres -c "createdb api_db_dev -O api_admin"
su postgres -c "createdb api_db_test -O api_admin"

# allow PostgreSQL access for local development
ufw allow 5432
sed -i "s/^#\?listen_addresses =.*/listen_addresses = '*'/g" /etc/postgresql/12/main/postgresql.conf
echo "
# Allow all connections - DEVELOPMENT usage only
host    all             all              0.0.0.0/0                       md5
host    all             all              ::/0                            md5
" >> /etc/postgresql/12/main/pg_hba.conf
systemctl restart postgresql


########################
#
# Install Python Tools
#
########################

# install build tools
apt install -y build-essential python3-dev

# install virtualenv
apt install -y python3-virtualenv


################
#
# Install Nginx
#
################

apt install -y nginx
ufw allow 'Nginx Full'
systemctl enable nginx.service


##################
#
# Configure Nginx
#
##################

# symlink mapped application directory to operational /var subdirectory
mkdir -p /var/www/vhosts
ln -s /vagrant/application /var/www/vhosts/base.api.python.vm

# setup public API reverse proxy
cp /vagrant/provision/development/templates/etc/nginx/sites-available/base.api.python.vm.conf /etc/nginx/sites-available/base.api.python.vm.conf
ln -s /etc/nginx/sites-available/base.api.python.vm.conf /etc/nginx/sites-enabled/base.api.python.vm.conf

# setup admin API reverse proxy
cp /vagrant/provision/development/templates/etc/nginx/sites-available/base.api.admin.python.vm.conf /etc/nginx/sites-available/base.api.admin.python.vm.conf
ln -s /etc/nginx/sites-available/base.api.admin.python.vm.conf /etc/nginx/sites-enabled/base.api.admin.python.vm.conf

# restart nginx
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
