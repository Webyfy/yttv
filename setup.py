import os, sys
import setuptools


requires = [
    'PySide2'
]

_ROOT = os.path.abspath(os.path.dirname(__file__))

with open(os.path.join(_ROOT, 'README.md')) as f:
    long_description = f.read()

def __data_files():
    """
    Collect the data files.
    """
    root_dir = sys.prefix
    return [(os.path.join(root_dir, "share/applications"), ["yttv/platform/com.webyfy.yttv.desktop"]),
    (os.path.join(root_dir, "share/icons/hicolor/48x48/apps"), ["yttv/platform/icons/hicolor/48x48/apps/com.webyfy.yttv.png"]),]


def __package_files(directory):
    """
    Collect the package files.
    """
    paths = []
    for (path, _, filenames) in os.walk(directory):
        for filename in filenames:
            paths.append(os.path.join('..', path, filename))
    return paths

def __package_data():
    """
    Return a list of package data.
    """
    data = []
    data.extend(__package_files('yttv/platform'))
    return data

setuptools.setup(
    name="yttv",
    version="0.3.5",
    description="YouTube for 10 foot UI with D-pad navigation.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Webyfy",
    author_email="info@webyfy.com",
    url="https://gitlab.com/webyfy/iot/e-gurukul/yttv",
    # download_url="https://gitlab.com/webyfy/iot/e-gurukul/yttv/archive/v0.3.5.tar.gz",
    packages=setuptools.find_packages(),
    package_data={'yttv': __package_data()},
    data_files=__data_files(),
    install_requires=requires,
    entry_points={'console_scripts': ['yttv = yttv.__main__:main']},
    keywords='youtube video stream tv yot',
    classifiers=[
        "Operating System :: POSIX :: Linux",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Development Status :: 3 - Alpha",
        "Environment :: X11 Applications :: Qt",
        "Intended Audience :: End Users/Desktop",
        "Topic :: Multimedia :: Video",
        "Topic :: Internet"] + [('Programming Language :: Python :: %s' % x) for x in '3 3.5 3.6 3.7 3.8 3.9'.split()]
)
