#!/usr/bin/env python
"""Packaging configuration.

This file actually doesn't contain any info. Everything is exctracted from pyproject.toml or git.
"""

import os

from poetry.semver import parse_constraint  # type: ignore
from poetry.utils.toml_file import TomlFile  # type: ignore
from setuptools import setup  # type: ignore

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

# Extract infos from pyproject.toml
# waiting for a better solution in https://github.com/python-poetry/poetry/issues/761
POETRY = TomlFile('pyproject.toml').read()['tool']['poetry']
with open(POETRY['readme']) as readme:
    README = readme.read()

setup(name=POETRY['name'],
      packages=[pkg['include'] for pkg in POETRY['packages']],
      install_requires=[f'{k}{parse_constraint(v)}' for k, v in POETRY['dependencies'].items() if k != 'python'],
      include_package_data=True,
      exclude_package_data={'': ['*.orig', '*.pyc']},
      license=POETRY['license'],
      description=POETRY['description'],
      long_description=README,
      long_description_content_type="text/markdown",
      url=POETRY['homepage'],
      author=POETRY['authors'][0].split('<')[0].strip(),
      author_email=POETRY['authors'][0].split('<')[1][:-1],
      python_requires=str(parse_constraint(POETRY['dependencies']['python'])),
      zip_safe=False,
      use_scm_version=True,
      setup_requires=['setuptools_scm'],
      classifiers=POETRY['classifiers'])
