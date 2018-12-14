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
from collections import Counter
import math
import os
from pathlib import Path

from numpy import dot

__author__ = "Gaurav Mishra"
__email__ = "gmishx@gmail.com"


def wordFrequency(data):
  '''
  Calculates the frequency of each unique word in the file

  :param data: Processed and Extracted text from the input file
  :return: Word frequency Dictionary
  '''
  frequency = Counter()
  for word in data:
    frequency[word] += 1
  return frequency


def l2_norm(a):
  ''' Scalar value of word frequency array (vector)'''
  return math.sqrt(dot(a, a))


def ngram_l2_norm(a):
  ''' Scalar value of word frequency dictionary'''
  a = [value for key, value in a.items()]
  return l2_norm(a)


def cosine_similarity(a, b):
  '''
  https://blog.nishtahir.com/2015/09/19/fuzzy-string-matching-using-cosine-similarity/
  Cosine similarity value of two word frequency dictionaries
  '''
  dot_product = 0
  for key, count in a.items():
    if key in b:
      dot_product += b[key] * count
  temp = ngram_l2_norm(a) * ngram_l2_norm(b)
  if temp == 0:
    return 0
  else:
    return dot_product / temp
