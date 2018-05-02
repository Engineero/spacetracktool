#!/usr/bin/env python

import os
from setuptools import setup, find_packages

#def read(fname):
#    return open(os.path.join(os.path.dirname(__file__), fname)).read()
with open ('README.rst', 'r') as readme_file:
    README = readme_file.read()

NAME = 'spacetracktool'
VERSION = '0.1.0b5'
DESCRIPTION = 'A Python API for querying space-track.org'
LONG_DESCRIPTION_CONTENT_TYPE = 'text/x-rst'
URL = 'https://github.com/Engineero/spacetracktool'
AUTHOR = 'Engineero'
AUTHOR_EMAIL = 'engineerolabs@gmail.com'
LICENSE = 'MIT'
CLASSIFIERS = ['Development Status :: 4 - Beta',
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
PROJECT_URLS = {'Source': 'https://github.com/Engineero/spacetracktool'}
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
