#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function, unicode_literals
import os

import yaml

from .package import PACKAGE_SOURCE_CONTAINER, Package
from .utils import change_working_directory, get_logger, get_template


RULEFILE_NAME = 'Shopfile'
DEFAULT_INSTALL_PREFIX = '3rdparty'

logger = get_logger(__file__)


def generate_common_includes():
    template = get_template('common.pri')
    result = template.render()
    with open('common.pri', 'w') as f:
        f.write(result)


def generate_aggregated_project(packages):
    # TODO: Handle project dependency.
    name = os.path.basename(DEFAULT_INSTALL_PREFIX) + '.pro'
    logger.info('Generating {name}'.format(name=name))
    template = get_template('aggregation.pro')
    result = template.render(packages=packages)
    with open(name, 'w') as f:
        f.write(result)


def run(rulefile=None):
    if rulefile is None:
        rulefile = RULEFILE_NAME
    if not hasattr(rulefile, 'read'):
        with open(rulefile) as f:
            rules = yaml.load(f)
    else:
        rules = yaml.load(f)

    prefix = os.path.abspath(rules.get('prefix', DEFAULT_INSTALL_PREFIX))
    if not os.path.exists(prefix):
        os.makedirs(prefix)
    with change_working_directory(DEFAULT_INSTALL_PREFIX):
        generate_common_includes()
    package_names = []
    for info in rules['packages']:
        package = Package(info)
        package_names.append(
            os.path.join(PACKAGE_SOURCE_CONTAINER, package.name)
        )
        package.install(prefix)
    # TODO: Uninstall obsolete packages.
    with change_working_directory(DEFAULT_INSTALL_PREFIX):
        generate_aggregated_project(package_names)
