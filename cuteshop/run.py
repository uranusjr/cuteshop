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

EXTRA_SPEC_SOURCES_ENVIRON = 'CUTESHOP_EXTRA_SPEC_SOURCES'

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


def build_sources_from_namespace(namespace):
    # Flatten nested lists.
    return [s for sl in namespace.spec_source for s in sl]


def build_sources_from_env():
    paths = os.getenv(EXTRA_SPEC_SOURCES_ENVIRON, '').split(':')
    paths = [os.path.abspath(os.path.expanduser(path)) for path in paths]
    return paths


def run(extra_sources=None, rulefile=None):
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
        package = Package(info, extra_sources=extra_sources)
        package_names.append(
            os.path.join(PACKAGE_SOURCE_CONTAINER, package.name)
        )
        package.install(prefix)
        try:
            obsolete_packages.remove(package.name)
        except KeyError:
            pass    # Ignore unexisted packages.
    for name in obsolete_packages:
        if not os.path.isdir(name):
            continue
        package = Package(name, extra_sources=extra_sources)
        package.uninstall(DEFAULT_INSTALL_PREFIX)
    with change_working_directory(DEFAULT_INSTALL_PREFIX):
        generate_aggregated_project(package_names)


def main():
    parser = argparse.ArgumentParser(
        description='Manages Qt project depedencies.',
    )
    parser.add_argument('-e', '--raise-exception', action='store_true')
    parser.add_argument(
        '-s', '--spec-source',
        action='append', nargs='+', default=[],
    )
    namespace = parser.parse_args()

    extra_sources = (
        build_sources_from_namespace(namespace)
        + build_sources_from_env()
    )
    try:
        run(extra_sources=extra_sources)
    except Exception as e:
        if namespace.raise_exception:
            raise
        else:
            print('[!] {exception}'.format(exception=e), file=sys.stderr)
            sys.exit(1)
