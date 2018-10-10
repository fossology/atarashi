#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Copyright 2018 Gaurav Mishra (gmishx@gmail.com)

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

import argparse
import os
from pathlib import Path

from tqdm import tqdm

from atarashi.libs.commentPreprocessor import CommentPreprocessor
from atarashi.license.licenseLoader import LicenseLoader

args = None


class LicensePreprocessor(object):

  @staticmethod
  def __load_licenses(licenseList, verbose=0):
    '''
    Fetch license short name and description from the License List (CSV)
    and preprocess them

    :param licenseList: Path to license list (CSV)
    :param verbose: Specify if verbose mode is on or not (Default is Off/ None)
    :return: Return pandas.DataFrame with processed fullname, header and text
    '''
    licenses = LicenseLoader.fetch_licenses(licenseList)
    if verbose > 0:
      print("Loaded " + str(len(licenses)) + " licenses")
    if verbose > 0:
      iterator = tqdm(range(len(licenses)),
                      desc="Licenses processed:",
                      total=len(licenses), unit="license")
    else:
      iterator = range(len(licenses))
    for idx in iterator:
      licenses.at[idx, 'processed_fullname'] = CommentPreprocessor.preprocess(str(licenses.at[idx, 'fullname']))
      licenses.at[idx, 'processed_header'] = CommentPreprocessor.preprocess(str(licenses.at[idx, 'license_header']))
      licenses.at[idx, 'processed_text'] = CommentPreprocessor.preprocess(str(licenses.at[idx, 'text']))
    return licenses

  @staticmethod
  def __write_csv(processedList, fileLocation):
    '''
    Write the preprocessed license list to a CSV file

    :param processedList: pandas.DataFrame to be written to a CSV file
    :param fileLocation: Location/ Path of the file where you want to write CSV
    '''
    processedList.to_csv(fileLocation, index=False, encoding='utf-8')

  @staticmethod
  def file_is_modified(source, destination):
    '''
    Check if source is modified before destination.
    If destination does not exists, create a new file.
    '''
    sourceTime = os.path.getmtime(source)
    destinationFilePath = Path(destination)
    if destinationFilePath.is_file():
      destTime = os.path.getmtime(destination)
    else:
      destinationDir = Path(os.path.dirname(destination))
      destinationDir.mkdir(parents=True, exist_ok=True)
      destTime = 0
    return sourceTime > destTime

  @staticmethod
  def create_processed_file(licenseList, processedFile, verbose=0):
    '''
    :param licenseList: Specify the license list file which contains licenses
    :param processedFile: Specify the destination to store processed list
    :param verbose: Specify if verbose mode is on or not (Default is Off/ None)
    :return: Path of processed license list to use. (This path will be default by further script)
    '''
    licenseList = os.path.abspath(licenseList)
    processedFile = os.path.abspath(processedFile)
    if LicensePreprocessor.file_is_modified(licenseList, processedFile):
      processedList = LicensePreprocessor.__load_licenses(licenseList, verbose)
      LicensePreprocessor.__write_csv(processedList, processedFile)
    return processedFile


if __name__ == "__main__":
  parser = argparse.ArgumentParser()
  parser.add_argument("licenseList", help="Specify the license list file which contains licenses")
  parser.add_argument("processedFile", help="Specify the destination to store processed list")
  parser.add_argument("-v", "--verbose", help="increase output verbosity",
                      action="count", default=0)
  args = parser.parse_args()
  licenseList = os.path.abspath(args.licenseList)
  processedFile = os.path.abspath(args.processedFile)
  verbose = args.verbose

  print("Use: " + LicensePreprocessor.create_processed_file(licenseList, processedFile, verbose))
