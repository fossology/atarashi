#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Copyright 2018 Aman Jain

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

import csv
import sys
import os
import time
import argparse
from pathlib import Path
from tqdm import tqdm
import pandas as pd

from CommentPreprocessor import preprocess
from getLicenses import fetch_licenses

'''Python Module to preprocess license list
Input: License list (CSV)
Output: Preprocessed license list
Description: Module to pre process the license list for further use.
            python LicensePreprocessor.py <licenseList> <processedLicenseList>
'''

args = None

def load_licenses(licenseList):
  ''' Fetch license short name and description from the License List (CSV) 
  and preprocess them
  
  licenseList -- Path to CSV to read
  
  Return pandas.DataFrame with processed fullname, header and text
  '''
  licenses = fetch_licenses(licenseList)
  if args is not None and args.verbose:
    print("Loaded " + str(len(licenses)) + " licenses")
  iterator = ""
  if args is not None and args.verbose:
    iterator = tqdm(range(len(licenses)),
                  desc = "Licenses processed:",
                  total = len(licenses), unit = "license")
  else:
    iterator = range(len(licenses))
  for idx in iterator:
    licenses.at[idx, 'processed_fullname'] = preprocess(str(licenses.at[idx, 'fullname']))
    licenses.at[idx, 'processed_header']   = preprocess(str(licenses.at[idx, 'license_header']))
    licenses.at[idx, 'processed_text']     = preprocess(str(licenses.at[idx, 'text']))
  return licenses

def write_csv(licenseList, fileLocation):
  ''' Write the preprocessed license list to a CSV file
  
  licenseList  -- pandas.DataFrame to be written
  fileLocation -- Path where to write the CSV
  '''
  licenseList.to_csv(fileLocation, index=False, encoding='utf-8')

def file_is_modified(source, destination):
  ''' Check if source is modified before destination.
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

def create_processed_file(licenseList, processedFile):
  ''' Drop in for __main__'''
  licenseList = os.path.abspath(licenseList)
  processedFile = os.path.abspath(processedFile)
  if file_is_modified(licenseList, processedFile):
    processedList = load_licenses(licenseList)
    write_csv(processedList, processedFile)
  return processedFile

if __name__ == "__main__":
  parser = argparse.ArgumentParser()
  parser.add_argument("licenseList", help="Specify the license list file which contains licenses")
  parser.add_argument("processedFile", help="Specify the destination to store processed list")
  parser.add_argument("-v", "--verbose", help="increase output verbosity",
                      action="store_true")
  args = parser.parse_args()
  licenseList = os.path.abspath(args.licenseList)
  processedFile = os.path.abspath(args.processedFile)
  if file_is_modified(licenseList, processedFile):
    processedList = load_licenses(licenseList)
    write_csv(processedList, processedFile)
    if args is not None and args.verbose:
      print("First 5 processed licenses")
      print(processedList[:5])
  elif args is not None and args.verbose:
    print("Preprocessed file is newer than source. Not creating new file!")
  print("Use " + processedFile + " with other agents")
