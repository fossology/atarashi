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

__author__ = "Gaurav Mishra"
__email__ = "gmishx@gmail.com"

from abc import ABCMeta, abstractmethod

from atarashi.libs.commentPreprocessor import CommentPreprocessor
from atarashi.license.licenseLoader import LicenseLoader


class AtarashiAgent(object):
  __metaclass__ = ABCMeta

  def __init__(self, licenseList, verbose=0):
    if isinstance(licenseList, str):
      self.licenseList = LicenseLoader.fetch_licenses(licenseList)
    else:
      self.licenseList = licenseList
    if 'processed_text' not in self.licenseList.columns:
      raise ValueError('The license list does not contain processed_text column.')
    self.verbose = verbose

  def loadFile(self, filePath):
    self.commentFile = CommentPreprocessor.extract(filePath)
    with open(self.commentFile) as file:
      data = file.read().replace('\n', ' ')
    return CommentPreprocessor.preprocess(data)

  def getVerbose(self):
    return self.verbose

  def setVerbose(self, verbose):
    self.verbose = int(verbose)

  @abstractmethod
  def scan(self, filePath):
    pass


def exactMatcher(licenseText, licenses):
  '''
  :param licenseText: Processed and extracted input text
  :param licenses: Processed licenses pandas data frame
  :return: License short name if exact match is found else -1 if no match
  '''
  output = []
  if 'processed_text' not in licenses.columns:
    raise ValueError('The license list does not contain processed_text column.')

  for idx in range(len(licenses)):
    if licenses.iloc[idx]['processed_text'] in licenseText and licenses.iloc[idx]['shortname'] != 'Void':
      output.append(licenses.iloc[idx]['shortname'])
  if not output:
    return -1
  return output
