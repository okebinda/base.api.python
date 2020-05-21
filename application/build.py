#   -*- coding: utf-8 -*-
from pybuilder.core import use_plugin, init

use_plugin("python.core")
use_plugin("python.install_dependencies")
use_plugin("python.flake8")
use_plugin("python.distutils")
use_plugin("pypi:pybuilder_pytest")
use_plugin('pypi:pybuilder_pytest_coverage')


name = "base.api.python.vm"
default_task = ['install_dependencies', 'publish']


@init
def set_properties(project):
    project.depends_on('bcrypt')
    project.depends_on('flask')
    project.depends_on('flask-cors')
    project.depends_on('flask-httpauth')
    project.depends_on('flask-marshmallow')
    project.depends_on('flask-migrate')
    project.depends_on('flask-principal')
    project.depends_on('flask-sqlalchemy')
    project.depends_on('intervals')
    project.depends_on('itsdangerous')
    project.depends_on('marshmallow')
    project.depends_on('marshmallow-sqlalchemy')
    project.depends_on('psycopg2')
    project.depends_on('psycopg2-binary')
    project.depends_on('python-dateutil')
    project.depends_on('sparkpost')
    project.depends_on('sqlalchemy-utils')

    project.build_depends_on("pytest-flask")
    project.build_depends_on("pytest-mock")
    project.build_depends_on("py_yaml_fixtures")

    project.set_property("dir_source_pytest_python", r"src/pytest/python")
    # project.set_property("pytest_extra_args", ["-m unit"])
