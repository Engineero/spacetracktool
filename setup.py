#!/usr/bin/env python

from setuptools import setup, find_packages

NAME = 'spacetracktool'
VERSION = '0.1.0b2'
DESCRIPTION = 'A Python API for querying space-track.org'
LONG_DESCRIPTION = 'README.rst'
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
               'Topic :: Scientific/Engineering',
               'Topic :: Scientific/Engineering :: Astronomy',
               'Topic :: Utilities']
KEYWORDS = 'space spacetrack elset tle satellite astronomy'
PROJECT_URLS = {'Source': 'https://github.com/Engineero/spacetracktool'}
PACKAGES = find_packages(exclude=['contrib', 'docs', 'tests*'])
INSTALL_REQUIRES = ['requests']

setup(name=Name,
      version=VERSION,
      description=DESCRIPTION,
      long_description=LONG_DESCRIPTION,
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
