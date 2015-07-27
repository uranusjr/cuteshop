#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals
import glob
import json
import os
import shutil

import six
import yaml
from cached_property import cached_property

from . import downloaders
from .exceptions import SpecError
from .utils import change_working_directory, get_logger, get_template


PACKAGE_SOURCE_CONTAINER = 'src'

logger = get_logger(__file__)

empty = object()


def process_file_list(file_list):
    expand = lambda p: os.path.join(downloaders.DOWNLOAD_CONTAINER, p)
    return sum((glob.glob(expand(p)) for p in file_list), [])


def get_list(dic, key, default=empty):
    if default is empty:
        default = []
    value = dic.get(key, default)
    if isinstance(value, tuple):
        value = list(value)
    elif not isinstance(value, list):
        value = [value]
    return value


class Package(object):

    SPEC_FORMATS = {
        '.json': json,
        '.yaml': yaml,
        '.yml': yaml,
    }
    SPEC_DIR = os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        'specs',
    )
    DOWNLOAD_METHODS = ('http', 'git',)

    def __init__(self, info_or_name):
        if isinstance(info_or_name, six.string_types):
            name, options = info_or_name, []
        else:
            name, options = info_or_name.popitem()
        self.name = name
        self.options = options

    @cached_property
    def spec(self):
        for ext in self.SPEC_FORMATS:
            spec_path = os.path.join(self.SPEC_DIR, self.name.lower() + ext)
            if os.path.exists(spec_path):
                load = self.SPEC_FORMATS[ext].load
                with open(spec_path) as f:
                    info = load(f)
                return info
        raise SpecError(name=self.name, verb='find')

    def download(self):
        # If the directory exists, pretend the installation is done.
        if os.path.exists(downloaders.DOWNLOAD_CONTAINER):
            logger.info('Using {name}'.format(name=self.name))
            return
        logger.info('Installing {name}'.format(name=self.name))
        source = self.spec['source']
        for method in self.DOWNLOAD_METHODS:
            if method in source:
                downloader = getattr(downloaders, method)
                break
        else:
            # No matching downloader. Fail.
            raise SpecError(name=self.name, verb='download')
        downloader.download(source)

    def generate_project(self):
        project_spec = self.spec.get('project', {})
        settings = {
            k: process_file_list(get_list(project_spec, k))
            for k in ('sources', 'headers', 'forms', 'resources',)
        }
        settings.update({
            'name': self.name,
            'qt': get_list(project_spec, 'qt'),
            'config': get_list(project_spec, 'config'),
            'defines': get_list(project_spec, 'defines'),
            'includepath': process_file_list(
                get_list(project_spec, 'includepath'),
            ),
            'public_headers': process_file_list(get_list(
                self.spec, 'public_headers',
                default=project_spec.get('headers', []),
            )),
            'extra': self.spec.get('project_extra', ''),
            'target': project_spec.get('target', self.name),
        })
        template = get_template('project.pro')
        result = template.render(**settings)
        with open(self.name + '.pro', 'w') as f:
            f.write(result)

    def install(self, prefix):
        path = os.path.join(prefix, PACKAGE_SOURCE_CONTAINER, self.name)
        if not os.path.exists(path):
            os.makedirs(path)
        with change_working_directory(path):
            self.download()
            self.generate_project()

    def uninstall(self, prefix):
        path = os.path.join(prefix, PACKAGE_SOURCE_CONTAINER, self.name)
        if os.path.exists(path):
            logger.info('Uninstalling {name}'.format(name=self.name))
            shutil.rmtree(path)
