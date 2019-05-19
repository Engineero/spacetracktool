#!/usr/bin/env python

import os
from setuptools import setup, find_packages
from distutils.util import convert_path

# Define paths and placeholders.
ver_dict = {}
VER_PATH = convert_path('spacetracktool/_version.py')
README_PATH = 'README.rst'

# Read the README contents.
with open (README_PATH, 'r') as readme_file:
    README = readme_file.read()

# Read the version info.
with open(VER_PATH, 'r') as ver_file:
    exec(ver_file.read(), ver_dict)

NAME = 'spacetracktool'
VERSION = ver_dict['__version__']  # update in spacetracktool/version.py!
DESCRIPTION = 'A Python API for querying space-track.org'
LONG_DESCRIPTION_CONTENT_TYPE = 'text/x-rst'
URL = 'https://github.com/Engineero/spacetracktool'
AUTHOR = 'Engineero'
AUTHOR_EMAIL = 'engineerolabs@gmail.com'
LICENSE = 'MIT'
CLASSIFIERS = ['Development Status :: 5 - Production/Stable',
               'Environment :: Console',
               'Intended Audience :: Developers',
               'Intended Audience :: Science/Research',
               'License :: OSI Approved :: MIT License',
               'Natural Language :: English',
               'Operating System :: OS Independent',
               'Programming Language :: Python',
               'Programming Language :: Python :: 3',
               'Programming Language :: Python :: 3.3',
               'Programming Language :: Python :: 3.4',
               'Programming Language :: Python :: 3.5',
               'Programming Language :: Python :: 3.6',
               'Topic :: Scientific/Engineering',
               'Topic :: Scientific/Engineering :: Astronomy',
               'Topic :: Utilities']
KEYWORDS = 'space spacetrack elset tle satellite astronomy'
PROJECT_URLS = {'Documentation': 'https://engineero.github.io/spacetracktool/',
                'Source': 'https://github.com/Engineero/spacetracktool',
                'Tracker': 'https://github.com/Engineero/spacetracktool/issues'}
PACKAGES = find_packages(exclude=['contrib', 'docs', 'tests*'])
INSTALL_REQUIRES = ['requests']

setup(name=NAME,
      version=VERSION,
      description=DESCRIPTION,
      long_description=README,
      long_description_content_type=LONG_DESCRIPTION_CONTENT_TYPE,
      url=URL,
      author=AUTHOR,
      author_email=AUTHOR_EMAIL,
      license=LICENSE,
      classifiers=CLASSIFIERS,
      keywords=KEYWORDS,
      project_urls=PROJECT_URLS,
      packages=PACKAGES,
      install_requires=INSTALL_REQUIRES)

# setup(setup_requires=['pbr'], pbr=True)
