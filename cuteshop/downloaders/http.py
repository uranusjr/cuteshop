#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals
import io
import os
import tarfile
import zipfile

from six.moves.urllib.request import urlopen

from ..exceptions import CommandError
from .base import DOWNLOAD_CONTAINER


COMPRESS_FORMATS = {
    '.zip': lambda fileobj: zipfile.ZipFile(file=fileobj),
    '.gz': lambda fileobj: tarfile.open(fileobj=fileobj, mode='r:gz'),
}


def download(source_info):
    """Downloads data from URL specified in ``http`` key.

    Returns an archive file that can be called ``extractall`` on. The callee
    is responsible to close the archive after use.
    """
    url = source_info['http']
    ext = os.path.splitext(url)[-1]
    try:
        klass = COMPRESS_FORMATS[ext]
    except KeyError:
        raise CommandError(
            'Unrecognized archive format: `{ext}`'.format(ext=ext)
        )
    response = urlopen(url)
    data = response.read()
    archive = klass(fileobj=io.BytesIO(data))
    archive.extractall('_')
    archive.close()
    contents = os.listdir('_')
    if len(contents) == 1:
        os.rename(os.path.join('_', contents[0]), DOWNLOAD_CONTAINER)
        os.rmdir('_')
    else:
        os.rename('_', 'src')
