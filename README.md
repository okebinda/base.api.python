# BASE.API.PYTHON

This repository holds the source code for a simple RESTful API written in Python using Flask that can be used as the starter package for a new project. It also contains a virtual machine for local development.

Contains the source code for two API domains: base.api.python.vm and base.api.admin.python.vm. The first is the public API for user-facing products, the second is the private API for administrator use to manage data. The two APIs have different routes and schema, while sharing the data model, library and dependencies. The build process creates a single artifact that can serve both APIs, determined by configuration settings.

Local development is run on a local virtual machine managed by Vagrant. To install the virtual machine, make sure you have installed Vagrant (https://www.vagrantup.com/) and a virtual machine provider, such as VirtualBox (https://www.virtualbox.org/).

## Manage Local Development Environment

### Provision Virtual Machine

Sets up the local development environment.

```ssh
> vagrant up
> vagrant ssh
$ cd /vagrant
$ ./scripts/build.sh -d
```

Also, to access the API from your host machine you should update your local DNS to point the two development API domains to the virtual machine's IP address. For example, on a Mac/Linux box you can update your `/etc/hosts` file with the following line:

```
172.29.17.200 base.api.python.vm base.api.admin.python.vm
```

### Start Virtual Machine

Starts the local development environment and logs in to the virtual machine. This is a prerequisite for any following steps if the machine is not already booted.

```ssh
> vagrant up
> vagrant ssh
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

### Activate the Python virtual environment

Most of the shell commands manage their own Python virtual environment, but if you want to activate your own session to run Python scripts manually use the following command:

```ssh
$ cd /vagrant/application
$ pipenv shell
```

### Rebuild the Project

To reinstall any dependencies (if there are updates in the Pipfile, for example) and rebuild the development database use the following command:

```ssh
$ cd /vagrant
$ ./scripts/build.sh -r
```

### Rebuild the Development Database

The development database is built and data fixtures are loaded as part of the initial build procedure. However, you can rebuild the database and reload the data to its original state using the following command:

```ssh
$ cd /vagrant
$ ./scripts/load_data.sh
```

## Public API: base.api.python.vm

### Start Development Server

Runs the local Flask development server, displays logs in standard output.

```ssh
$ cd /vagrant
$ ./scripts/run_public.sh
```

URL: http://base.api.python.vm/v/dev/

## Admin API: base.api.admin.python.vm

### Start Development Server

Runs the local Flask development server, displays logs in standard output.

```ssh
$ cd /vagrant
$ ./scripts/run_admin.sh
```

URL: http://base.api.admin.python.vm/v/dev/

## Testing

All tests must pass before committing any code into the repository.

For both unit and integration tests the following options are available: `-c` to display the coverage report and `-h` to create an HTML coverage report for detailed gap analysis.

### Unit Tests

```ssh
$ cd /vagrant
$ ./tests/unit/run.sh [OPTIONS]
```

### Integration Tests

```ssh
$ cd /vagrant
$ ./tests/integration/run.sh [OPTIONS]
```

## Linters

Before committing code into the repository static analysis should be performed and any issues resolved.

```ssh
$ cd /vagrant
$ ./scripts/lint.sh
```

The following linters are are run as part of the `lint.sh` command:

#### Bandit

Bandit is a security linter to find common security issues in Python code.

Ref: https://bandit.readthedocs.io/en/latest/

#### Pyflakes

Pyflakes is a simple linter that checks for errors.

Ref: https://github.com/PyCQA/pyflakes

#### Pycodestyle

Pycodestyle is a tool to check Python code against the style conventions of PEP 8.


Ref: https://pycodestyle.readthedocs.io/en/latest/

#### Pylint

Pylint is a robust linter that checks for errors, coding standards, and code smell.


Ref: https://pylint.readthedocs.io/en/latest/

## Deployment

### Build

To create a release artifact using pybuilder, use the following command:

```ssh
$ cd /vagrant
$ ./scripts/build.sh
```

### Deploy

[TBD]

## Repository Directory Structure

| Directory/File           | Purpose       |
| ------------------------ | ------------- |
| ```application/```       | Contains all files required for the application to run |
| ```├─ docs/```           | Location for automatically generated source code documentation (not currently enabled) |
| ```├─ src/```            | Source code |
| ```│ ├─ main/```         | Application source code |
| ```│ │ ├─ python/```     | Python source code |
| ```│ │ └─scripts/```     | Source code for various scripts used during application operation |
| ```│ └─ pytest/```       | Unit and integration tests written with pytest |
| ```│   └─ python/```     | Automated tests for python source code |
| ```├─ build.py```        | The build spec used by pybuilder |
| ```└─ Pipfile```         | The Pip dependency manifest file for the project |
| ```data/```              | Contains the data used to populate the application for development and testing, such as data fixtures |
| ```documentation/```     | Documentation files |
| ```provision/```         | Provision scripts for local virtual machine and production servers |
| ```scripts/```           | Contains various scripts, such as the script to build the application for the first time (installs dependencies) |
| ```tests/```             | Unit and integration tests |
| ```LICENSE```            | The project's licensing terms |
| ```README.md```          | This file |
| ```Vagrantfile```        | Configuration file for Vagrant when provisioning local development virtual machine |
