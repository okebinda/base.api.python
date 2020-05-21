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
#   ansible
#
#  author: https://github.com/okebinda
#  date: May, 2020
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


################
#
# Install Tools
#
################

# install basic tools
apt install -y vim tmux screen git zip

# install AWS command line interface
apt install -y awscli

# install ansible
apt install ansible -y
cp /vagrant/provision/development/templates/etc/ansible/hosts /etc/ansible/hosts


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


############################
#
# Install Python with Tools
#
############################

# install pyenv for vagrant user
apt install -y make build-essential libssl-dev zlib1g-dev libbz2-dev libreadline-dev libsqlite3-dev wget curl llvm libncurses5-dev libncursesw5-dev xz-utils tk-dev libffi-dev liblzma-dev python-openssl
su - vagrant -c "curl https://pyenv.run | bash"
echo 'export PATH="$HOME/.pyenv/bin:$PATH"' >> /home/vagrant/.bashrc
echo 'eval "$(pyenv init -)"' >> /home/vagrant/.bashrc
echo 'eval "$(pyenv virtualenv-init -)"' >> /home/vagrant/.bashrc

# install and use python 3.8.3
su - vagrant -c "/home/vagrant/.pyenv/bin/pyenv install 3.8.3"
su - vagrant -c "/home/vagrant/.pyenv/bin/pyenv global 3.8.3"

# install pipenv
su - vagrant -c "/home/vagrant/.pyenv/shims/pip install pipenv"


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
