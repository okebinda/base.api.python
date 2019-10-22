# BASE.API.PYTHON

This repository holds the source code for a simple RESTful API written in Python using Flask that can be used as the starter package for a new project. It also contains a virtual machine for local development.

Contains the source code for two API domains: base.api.python.vm and base.api.admin.python.vm. The first is the public API for user-facing products, the second is the private API for administrator use to manage data. The two APIs have different routes and schema, while sharing the data model, library and dependencies. They are packaged independently for deployment.

Local development is run on a local virtual machine managed by Vagrant. To install the virtual machine, make sure you have installed Vagrant (https://www.vagrantup.com/) and a virtual machine provider, such as VirtualBox (https://www.virtualbox.org/).

## Manage Local Development Environment

### Provision Virtual Machine

Sets up the local development environment.

```ssh
> vagrant up
> vagrant ssh
$ cd /vagrant
$ ./scripts/build.sh
```

Additionaly you will need to manually log in to the local PostgreSQL server to enable some extensions for the development and test databases. Once the extensions are setup you can load the development data fixtures. (This is a temporary step until I get around to incorporating the extensions into the build script above.)

```ssh
$ sudo bash
# su postgres
$ psql
=# \connect api_db_dev;
=# create extension pgcrypto;
=# \connect api_db_test;
=# create extension pgcrypto;
=# \q
$ exit
# exit

$ cd /vagrant
$ source application/env/bin/activate
$ python ./scripts/load_fixtures.py
```

Also, to access the API from your host machine you should update your local DNS to point the two development API domains to the virtual machine's IP address. For example, on a Mac/Linux box you can update your `/etc/hosts` file with the following line:

```
172.29.17.200 base.api.python.vm base.api.admin.python.vm
```

### Start Virtual Machine

Starts the local development environment. This is a prerequisite for any following steps if the machine is not already booted.

```ssh
> vagrant up
> vagrant ssh
$ cd /vagrant/application
$ source env/bin/activate
```

### Stop Virtual Machine

Stops the local development environment. Run this command from the host (i.e. log out of any virtual machine SSH sessions).

```ssh
> vagrant halt
```

### Delete Virtual Machine

Deletes the local development environment. Run this command from the host (i.e. log out of any virtual machine SSH sessions).

```ssh
> vagrant destroy
```

Sometimes it is useful to completely remove all residual Vagrant files after destroying the box, in this case run the additional command:

```ssh
> rm -rf ./vagrant
```

## Public API: base.api.python.vm

### Start Development Server

Runs the local Flask development server, displays logs in standard output.

```ssh
$ cd /vagrant/application
$ ./run_public.sh
```

URL: http://base.api.python.vm/v/dev/

### Run Tests

All tests must pass before committing any code into the repository.

```ssh
$ cd /vagrant
$ python -W ignore tests/api_public/functional/run.py
```

## Admin API: base.api.admin.python.vm

### Start Development Server

Runs the local Flask development server, displays logs in standard output.

```ssh
$ cd /vagrant/application
$ ./run_admin.sh
```

URL: http://base.api.admin.python.vm/v/dev/

### Run Tests

All tests must pass before committing any code into the repository.

```ssh
$ cd /vagrant
$ python -W ignore tests/api_admin/functional/run.py
```

## Linters

#### Bandit

Bandit is a security linter to find common security issues in Python code.

```ssh
$ cd /vagrant/application
$ bandit -r src/
```

Ref: https://bandit.readthedocs.io/en/latest/

#### Pyflakes

Pyflakes is a simple linter that checks for errors.

```ssh
$ cd /vagrant/application
$ pyflakes src/
```

Ref: https://github.com/PyCQA/pyflakes

#### Pycodestyle

Pycodestyle is a tool to check Python code against the style conventions of PEP 8.

```ssh
$ cd /vagrant/application
$ pycodestyle src/
```

Ref: https://pycodestyle.readthedocs.io/en/latest/

#### Pylint

Pylint is a robust linter that checks for errors, coding standards, and code smell.

```ssh
$ cd /vagrant/application
$ pylint src/
```

Ref: https://pylint.readthedocs.io/en/latest/

## Deployment

Deployment is broken up into two steps: `make` and `deploy`.

`make` creates a deployment package with all the required code, installs production dependencies, and optionally runs tests and uploads the package to a storage bucket.

`deploy` logs into the production server, downloads the package from the storage bucket, installs it in a new directory and promotes the new packages using a blue-green deployment.

Details can be found at the top of each script in the `/deploy` diretory.

Options for [API NAME] are: `public` or `admin`.

The [TAG] argument for production releases should follow the pattern: major.minor.build. For the build I usually use the git commit (short) hash.

```ssh
$ cd /vagrant
$ ./deploy/make.sh [OPTIONS] [API NAME] [TAG]
$ ./deploy/deploy.sh [OPTIONS] [API NAME] [VERSION] [FILENAME]
```

#### Example:

```ssh
$ cd /vagrant
$ ./deploy/make.sh -tu public 1.1.3.165
$ ./deploy/deploy.sh -p public 1.1 base.api.python.vm-1.1.3.165.zip
```

## Repository Directory Structure

| Directory/File     | Purpose       |
| ------------------ | ------------- |
| /application       | Contains all files required for the application to run |
| ├─/env             | Contains application dependencies installed via `virtualenv`, `pip` or `pipenv` |
| ├─/etc             | Sample config files |
| ├─/src             | Application source code |
| └─/web             | Any publicly available web resources, such as HTML, CSS, images, etc. |
| /data              | Contains the data used to populate the application for development and testing, such as data fixtures |
| /deploy            | Deployment scripts |
| └─/packages        | Contains packages created by the `make` script - can be temporary or committed |
| /documentation     | Documentation files |
| /provision         | Provision scripts for local virtual machine and production servers |
| /scripts           | Contains various scripts, such as the script to build the application for the first time (installs dependencies) |
| /tests             | Unit and functional tests |
| README.md          | This file |
| Vagranfile         | Configuration file for Vagrant when provisioning local development virtual machine |

