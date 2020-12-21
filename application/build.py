#   -*- coding: utf-8 -*-
import os

from pybuilder.core import use_plugin, init

use_plugin("python.core")
use_plugin("python.install_dependencies")
# use_plugin("python.distutils")
use_plugin("pypi:pybuilder_pytest")
use_plugin('pypi:pybuilder_pytest_coverage')
use_plugin("exec")


name = "base.api.python.vm"
version = "0.1.0.dev"

default_task = ['install_dependencies', 'analyze', 'publish']


@init
def set_properties(project):

    # dependencies
    project.depends_on_requirements("requirements.txt")
    project.build_depends_on_requirements("requirements-dev.txt")

    # testing
    project.set_property("dir_source_pytest_python", r"src/pytest/python")
    project.set_property('integrationtest_inherit_environment', True)
    project.set_property("pytest_extra_args", ["-m unit"])

    # linting
    project.set_property("analyze_command", "/vagrant/scripts/lint.sh")
