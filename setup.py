#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Copyright 2018 Gaurav Mishra <gmishx@gmail.com>

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
from setuptools import setup, find_packages
import setuptools.command.build_py
import subprocess

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


class BuildAtarashiDependencies(distutils.cmd.Command):
  """
  Class to build dependency files for Atarashi.
  Files created:
  1.  data/Ngram_keywords.json
  2.  licenses/<spdx_license>.csv
  3.  licenses/processedLicenses.csv
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
    subprocess.run([
        "atarashi/build_deps.py",
        "-t", str(self.threads),
      ], check = True)


class BuildAtarashi(setuptools.command.build_py.build_py):
  """
  Class to replace default `build_py` and call `build_deps`.
  """
  def run(self):
    """Run `build_deps` target."""
    self.run_command('build_deps')
    setuptools.command.build_py.build_py.run(self)


requirements = [
  'tqdm>=4.23.4',
  'pandas>=0.23.1',
  'pyxDamerauLevenshtein>=1.5',
  'scikit-learn>=0.18.1',
  'scipy>=0.18.1',
  'textdistance>=3.0.3',
  'setuptools>=39.2.0']

setup(
  name = "atarashi",
  version = "0.0.9",
  author = "Aman Jain",
  author_email = "amanjain5221@gmail.com",
  description = ("An intelligent license scanner."),
  license = "GPL-2.0-only",
  url = "https://github.com/siemens/atarashi",
  long_description = read('README.md'),
  classifiers = [
    "Development Status ::  Pre-Alpha",
    "Topic :: Utilities",
    "License :: OSI Approved :: GPL v2.0 License",
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
  setup_requires = requirements,
  install_requires = requirements,
  dependency_links = ['git+https://github.com/amanjain97/code_comment#egg=code_comment'],
  package_data = {
    'data': ['data/Ngram_keywords.json'],
    'licenses': ['licenses/licenseList.csv', 'licenses/processedLicenses.csv']
  },
  data_files = [
    ('data', ['data/Ngram_keywords.json']),
    ('licenses', ['licenses/licenseList.csv', 'licenses/processedLicenses.csv'])
  ],
  cmdclass = {
    'build_deps': BuildAtarashiDependencies,
    'build_py': BuildAtarashi,
  },
)

