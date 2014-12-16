#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function, unicode_literals
import contextlib
import logging
import os
import subprocess
import sys

import jinja2
import six


try:
    DEVNULL = subprocess.DEVNULL
except AttributeError:
    DEVNULL = open(os.devnull, 'r+b')

LOGGING = {
    'level': logging.INFO,
    'loggers': {},
}

TEMPLATE_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(
        os.path.join(os.path.dirname(__file__), 'templates')
    )
)


def python_2_unicode_compatible(klass):
    """Class decorator that bridges __str__ to __unicode__ under Python 2.

    Based on Django's decorator of the same name.
    """
    if six.PY2:
        klass.__unicode__ = klass.__str__
        klass.__str__ = lambda self: six.text_type(self).encode('utf-8')
    return klass


@contextlib.contextmanager
def change_working_directory(path):
    """Context manager to resume old working directory on exit.
    """
    prev_wd = os.getcwd()
    os.chdir(path)
    yield
    os.chdir(prev_wd)


def get_logger(name):
    try:
        logger = LOGGING['loggers'][name]
    except KeyError:
        logger = logging.getLogger(name)
        ch = logging.StreamHandler(sys.stdout)
        formatter = logging.Formatter('%(message)s')
        ch.setFormatter(formatter)
        logger.addHandler(ch)
        logger.setLevel(LOGGING['level'])
        LOGGING['loggers'][name] = logger
    return logger


def set_logger_level(level):
    LOGGING['level'] = level
    for _, value in enumerate(LOGGING['loggers']):
        value.setLevel(level)


def get_template(name):
    return TEMPLATE_ENVIRONMENT.get_template(name)
