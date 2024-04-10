#!/usr/bin/env python3

from setuptools import setup, find_packages
from os import path, walk
from build_manpages import build_manpages, get_build_py_cmd, get_install_cmd

from yttv import YTTV_VERSION

_ROOT = path.abspath(path.dirname(__file__))

with open(path.join(_ROOT, 'README.md')) as f:
    long_description = f.read()


def __package_files(directory):
    """
    Collect the package files.
    """
    paths = []
    for (dirpath, _, filenames) in walk(directory):
        for filename in filenames:
            paths.append(path.join('..', dirpath, filename))
    return paths


def __package_data():
    """
    Return a list of package data.
    """
    data = []
    data.extend(__package_files('yttv/icons'))
    return data


setup(
    name='yttv',
    version=YTTV_VERSION,
    description='YouTube on TV',
    long_description=long_description,
    long_description_content_type="text/markdown",
    author='Webyfy',
    author_email='info@webyfy.com',
    url='https://gitlab.com/webyfy/iot/e-gurukul/yttv',
    maintainer='Webyfy',
    maintainer_email='info@webyfy.com',
    packages=find_packages(),
    package_data={'yttv': __package_data()},
    entry_points={'console_scripts': ['yttv = yttv.__main__:main']},
    python_requires='>=3.8',
    classifiers=[
        'Operating System :: POSIX :: Linux',
        'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
        'Development Status :: 4 - Beta',
        'Environment :: X11 Applications',
        'Intended Audience :: End Users/Desktop',
        'Programming Language :: Python :: 3',
        'Topic :: Internet',
        'Topic :: Multimedia :: Video'
    ],
    cmdclass={
        'build_manpages': build_manpages,
        # Re-define build_py and install commands so the manual pages
        # are automatically re-generated and installed
        'build_py': get_build_py_cmd(),
        'install': get_install_cmd(),
    }
)
