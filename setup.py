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
from setuptools import setup, find_packages
import setuptools.command.build_py
import subprocess
import sys

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
    'numpy>=1.15.1',
    'tqdm>=4.23.4',
    'pandas>=0.23.1']

requirements = [
    'setuptools>=39.2.0',
    'numpy>=1.15.1',
    'tqdm>=4.23.4',
    'pandas>=0.23.1',
    'scikit-learn>=0.18.1',
    'scipy>=0.18.1',
    'textdistance>=3.0.3',
    'pyxDamerauLevenshtein>=1.5']

ext_links = [
    'git+https://github.com/amanjain97/code_comment#egg=code_comment'
]

install_options = [sys.executable, '-m', 'pip', 'install', '--upgrade', '--ignore-installed']


class InstallAtarashiBuildRequirements(distutils.cmd.Command):
    """
    Class to install build time dependencies for Atarashi.
    """
    description = 'install Atarashi build time dependencies'
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        """Install build time dependencies using PIP"""
        global install_options
        global build_requirements
        global ext_links
        if os.geteuid() != 0:
            install_options += ['--user']

        subprocess.run(install_options + build_requirements, check=True)
        for package in ext_links:
            subprocess.run(install_options + ['-e', package], check=True)


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
            sys.executable,
            "atarashi/build_deps.py",
            "-t", str(self.threads),
        ], check=True)


class BuildAtarashi(setuptools.command.build_py.build_py):
    """
    Class to replace default `build_py` and call `build_deps`.
    """

    def run(self):
        """Run `build_deps` target."""
        self.run_command('install_deps')
        self.run_command('build_deps')
        setuptools.command.build_py.build_py.run(self)


metadata = dict(
    name="atarashi",
    version="0.0.9",
    author="Aman Jain",
    author_email="amanjain5221@gmail.com",
    description="An intelligent license scanner.",
    license="GPL-2.0-only",
    url="https://github.com/fossology/atarashi",
    long_description=read('README.md'),
    classifiers=[
        "Development Status ::  Pre-Alpha",
        "Topic :: Utilities",
        "License :: OSI Approved :: GPL v2.0 License",
    ],
    keywords=[
        "atarashi", "license", "license-scanner", "oss",
        "oss-compliance"
    ],
    python_requires=">=3.5",
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'atarashi = atarashi.atarashii:main'
        ]
    },
    zip_safe=False,
    setup_requires=build_requirements,
    install_requires=requirements,
    dependency_links=ext_links,
    package_data={
        'data': ['data/Ngram_keywords.json'],
        'licenses': ['licenses/licenseList.csv', 'licenses/processedLicenses.csv']
    },
    data_files=[
        ('data', ['data/Ngram_keywords.json']),
        ('licenses', ['licenses/licenseList.csv', 'licenses/processedLicenses.csv'])
    ],
    cmdclass={
        'install_deps': InstallAtarashiBuildRequirements,
        'build_deps': BuildAtarashiDependencies,
        'build_py': BuildAtarashi,
    },
)

if len(sys.argv) >= 2 and sys.argv[1] == 'install':
    subprocess.run(install_options + ['pyxDamerauLevenshtein>=1.5'], check=True)
    for package in ext_links:
        subprocess.run(install_options + ['-e', package], check=True)
setup(**metadata)
