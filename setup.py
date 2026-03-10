#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Minimal setup.py shim for Atarashi.
Supports setuptools-based tools like stdeb for Debian packaging.
Main project meta-data lives in pyproject.toml (Poetry).
"""
from setuptools import setup, find_packages
import os

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname), encoding='utf-8').read()

# Note: Dependency management is handled by pyproject.toml in modern installs.
# This file is provided for compatibility with debian package builders.
setup(
    name="atarashi",
    version="0.0.11",
    packages=find_packages(),
    long_description=read('README.md'),
    long_description_content_type='text/markdown',
    entry_points={
        'console_scripts': [
            'atarashi = atarashi.atarashii:main',
        ]
    },
    # PR #47 fix: Do NOT automate --user flag. 
    # Let pip/setup tools handle user-level installs natively and correctly.
)
