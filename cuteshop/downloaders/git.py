#!/usr/bin/env python
# -*- coding: utf-8 -*-

import subprocess
from ..utils import DEVNULL
from .base import DOWNLOAD_CONTAINER


def download(source_info):
    url = source_info['git']
    subprocess.call(
        ('git', 'clone', url, DOWNLOAD_CONTAINER),
        stdout=DEVNULL, stderr=subprocess.STDOUT,
    )
