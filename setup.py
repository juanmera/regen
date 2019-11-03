#!/usr/bin/env python
# Copyright 2019 Juan Manuel Mera
# Distributed under the terms of GNU General Public License v3 (GPLv3)

from setuptools import setup

with open('README.md') as f:
    long_description = f.read()

setup(
    name='regen',
    version='0.1.0',
    description='Fixed-size pattern generator',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='Juan Mera',
    author_email='juanmera@gmail.com',
    url='https://www.github.com/juanmera/regen',
    packages=['regen']
)
