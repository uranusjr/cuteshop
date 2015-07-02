#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function, unicode_literals
import argparse
import os
import sys

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
        if os.path.isdir('src'):
            obsolete_packages = set(os.listdir('src'))
        else:
            obsolete_packages = set()
    package_names = []
    for info in rules['packages']:
        package = Package(info)
        package_names.append(
            os.path.join(PACKAGE_SOURCE_CONTAINER, package.name)
        )
        package.install(prefix)
        try:
            obsolete_packages.remove(package.name)
        except KeyError:
            pass    # Ingore unexisted packages.
    for name in obsolete_packages:
        if not os.path.isdir(name):
            continue
        package = Package(name)
        package.uninstall(DEFAULT_INSTALL_PREFIX)
    with change_working_directory(DEFAULT_INSTALL_PREFIX):
        generate_aggregated_project(package_names)


def main():
    parser = argparse.ArgumentParser(
        description='Manages depedencies for Qt project.',
    )
    parser.add_argument('-e', '--raise-exception', action='store_true')
    namespace = parser.parse_args()

    try:
        run()
    except Exception as e:
        if namespace.raise_exception:
            raise
        else:
            print('[!] {exception}'.format(exception=e))
            sys.exit(1)
