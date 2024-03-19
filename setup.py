#!/usr/bin/env python3

from setuptools import setup, find_packages
from os import path, walk

_ROOT = path.abspath(path.dirname(__file__))

with open(path.join(_ROOT, 'README.md')) as f:
    long_description = f.read()

setup(
    name='yttv',
    version='0.1.3',
    description='YouTube on TV',
    long_description=long_description,
    long_description_content_type="text/markdown",
    author='Webyfy',
    author_email='info@webyfy.com',
    url='https://gitlab.com/webyfy/iot/e-gurukul/yttv',
    packages=find_packages()
)
