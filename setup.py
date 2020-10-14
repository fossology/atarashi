#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Copyright 2018 Gaurav Mishra <gmishx@gmail.com>

SPDX-License-Identifier: GPL-2.0

This program is free software; you can redistribute it and/or
modify it under the terms of the GNU General Public License
version 2 as published by the Free Software Foundation.
This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License along
with this program; if not, write to the Free Software Foundation, Inc.,
51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.
"""
import distutils.cmd
import os
import subprocess
import sys

from atarashi.build_deps import download_dependencies
from setuptools import setup, find_packages
import setuptools.command.build_py


sys.path.insert(0, os.path.dirname(os.path.realpath(__file__)))


__author__ = "Gaurav Mishra"
__email__ = "gmishx@gmail.com"


# Utility function to read the README file.
# Used for the long_description.  It's nice, because now 1) we have a top level
# README file and 2) it's easier to type in the README file than to put a raw
# string in below ...
def read(fname):
  """
  Utility function to read the README file.
  :param fname: Path to file to read
  :rtype: String
  Returns file content
  """
  return open(os.path.join(os.path.dirname(__file__), fname)).read()


build_requirements = [
  'setuptools>=39.2.0',
  'numpy>=1.16.0',
  'tqdm>=4.23.4',
  'pandas>=0.23.1',
  'urllib3>=1.24.1',
  'nirjas>=0.0.3'
]

requirements = [
  'setuptools>=39.2.0',
  'numpy>=1.16.0',
  'tqdm>=4.23.4',
  'pandas>=0.23.1',
  'scikit-learn>=0.18.1',
  'scipy>=0.18.1',
  'textdistance>=3.0.3',
  'pyxDamerauLevenshtein>=1.5',
  'urllib3>=1.24.1',
  'nirjas>=0.0.3'
]

class BuildAtarashiDependencies(distutils.cmd.Command):
  """
  Class to build dependency files for Atarashi.
  Files created:
  1.  data/Ngram_keywords.json
  2.  data/licenses/<spdx_license>.csv
  3.  data/licenses/processedLicenses.csv
  """
  description = 'build Atarashi dependency files'
  user_options = [
    ('threads=', 't', 'Number of threads to use')
  ]

  def initialize_options(self):
    """Set default values for options."""
    self.threads = os.cpu_count()

  def finalize_options(self):
    """Check the values for options."""
    if self.threads:
      self.threads = int(self.threads)
      assert self.threads > 0

  def run(self):
    """Run atarashi/build_deps.py"""
    download_dependencies(self.threads)


class BuildAtarashi(setuptools.command.build_py.build_py):
  """
  Class to replace default `build_py` and call `build_deps`.
  """

  def run(self):
    """Run `build_deps` target."""
    self.run_command('build_deps')
    setuptools.command.build_py.build_py.run(self)


metadata = dict(
  name = "atarashi",
  version = "0.0.11",
  author = "Aman Jain",
  author_email = "amanjain5221@gmail.com",
  description = ("An intelligent license scanner."),
  license = "GPL-2.0-only",
  url = "https://github.com/fossology/atarashi",
  long_description = read('README.md'),
  long_description_content_type='text/markdown',
  classifiers = [
    "Development Status :: 2 - Pre-Alpha",
    "Topic :: Utilities",
    "Intended Audience :: Legal Industry",
    "License :: OSI Approved :: GNU General Public License v2 (GPLv2)"
  ],
  keywords = [
    "atarashi", "license", "license-scanner", "oss",
    "oss-compliance"
  ],
  python_requires = ">=3.5",
  packages = find_packages(),
  entry_points = {
    'console_scripts': [
      'atarashi = atarashi.atarashii:main'
    ]
  },
  zip_safe = False,
  setup_requires = build_requirements,
  install_requires = requirements,
  include_package_data = True,
  package_data = {
    'atarashi': [
      'data/Ngram_keywords.json',
      'data/licenses/processedLicenses.csv'
    ]
  },
  cmdclass = {
    'build_deps': BuildAtarashiDependencies,
    'build_py': BuildAtarashi,
  },
)

setup(**metadata)
