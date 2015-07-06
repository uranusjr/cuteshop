#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from setuptools import find_packages, setup


def get_version():
    code = None
    path = os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        'cuteshop',
        '__init__.py',
    )
    with open(path) as f:
        for line in f:
            if line.startswith('VERSION'):
                code = line[len('VERSION = '):]
    return '.'.join([str(c) for c in eval(code)])


readme = open('README.rst').read()
history = open('HISTORY.rst').read().replace('.. :changelog:', '')

requirements = open('requirements.txt').read().strip().split('\n')

setup(
    name='cuteshop',
    version=get_version(),
    description='Package manager for Qt projects.',
    long_description='\n\n'.join([readme, history]),
    author='Tzu-ping Chung',
    author_email='uranusjr@gmail.com',
    url='https://github.com/uranusjr/cuteshop',
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'cuteshop=cuteshop.run:main',
        ],
    },
    include_package_data=True,
    install_requires=requirements,
    license='MIT',
    zip_safe=False,
    keywords=['cuteshop', 'qt'],
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
    ],
)
