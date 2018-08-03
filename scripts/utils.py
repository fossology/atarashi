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

__author__ = "Gaurav Mishra"
__email__ = "gmishx@gmail.com"

import os
import tarfile
from pathlib import Path

TAR_FILE_NAME = "Ngram_keywords.json.tar.gz"


def unpack_json_tar():
  '''
  Unzip the ngram file
  '''
  dir = os.path.dirname(os.path.abspath(__file__))
  dir = os.path.abspath(dir + "/../data/")
  tarFilePath = Path(os.path.abspath(dir + "/" + TAR_FILE_NAME))
  if tarFilePath.is_file():
    tar = tarfile.open(str(tarFilePath))
    tar.extractall(path=dir)
    tar.close()
    tarFilePath.unlink()

