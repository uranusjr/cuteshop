#!/usr/bin/env python
# -*- coding: utf-8 -*-

import subprocess
from ..utils import DEVNULL, change_working_directory
from .base import DOWNLOAD_CONTAINER


def _checkout(name):
    with change_working_directory(DOWNLOAD_CONTAINER):
        subprocess.call(
            ('git', 'checkout', name),
            stdout=DEVNULL, stderr=subprocess.STDOUT,
        )


def download(source_info):
    url = source_info['git']
    subprocess.call(
        ('git', 'clone', '--recursive', url, DOWNLOAD_CONTAINER),
        stdout=DEVNULL, stderr=subprocess.STDOUT,
    )
    if 'tag' in source_info:
        _checkout(source_info['tag'])
    elif 'branch' in source_info:
        _checkout(source_info['branch'])
