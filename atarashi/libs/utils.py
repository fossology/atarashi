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
from collections import Counter
import math
import os
from pathlib import Path
import tarfile

from numpy import dot

__author__ = "Gaurav Mishra"
__email__ = "gmishx@gmail.com"

TAR_FILE_NAME = "Ngram_keywords.json.tar.gz"


def unpack_json_tar():
  dir = os.path.dirname(os.path.abspath(__file__))
  dir = os.path.abspath(dir + "/../data/")
  tarFilePath = Path(os.path.abspath(dir + "/" + TAR_FILE_NAME))
  if tarFilePath.is_file():
    tar = tarfile.open(str(tarFilePath))
    tar.extractall(path = dir)
    tar.close()
    tarFilePath.unlink()


def wordFrequency(data):
  frequency = Counter()
  for word in data:
    frequency[word] += 1
  return frequency


def l2_norm(a):
  return math.sqrt(dot(a, a))


def ngram_l2_norm(a):
  a = [value for key, value in a.items()]
  return l2_norm(a)


def cosine_similarity(a, b):
  dot_product = 0
  for key, count in a.items():
    if key in b:
      dot_product += b[key] * count
  temp = ngram_l2_norm(a) * ngram_l2_norm(b)
  if temp == 0:
    return 0
  else:
    return dot_product / temp
