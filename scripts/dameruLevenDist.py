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

__author__ = "Aman Jain"

import argparse
import sys
from pyxdameraulevenshtein import damerau_levenshtein_distance

from CommentExtractor import CommentExtract
from CommentPreprocessor import preprocess
from getLicenses import fetch_licenses
from exactMatch import exactMatcher

'''Python Module to classify license using Damerau Levenshtein distance algorithm
Input: File from which license needs to be scanned and processed license list (CSV)
Output: License which is contained in the file.
Description: It extract comments from the file and after preprocessing,
              it calculates the damerau_levenshtein_distance and then classify
              by finding the leadt distance.
              python dameruLevenDist.py <filename> <processedLicenseList>
'''

args = None


def classifyLicenseDameruLevenDist(filename, licenseList):
  '''
  Read the content content of filename, extract the comments and preprocess them.
  Find the Damerau Levenshtein distance between the preprocessed file content
  and the license text.
  
  Arguments:
  filename    -- path of the file to scan
  licenseList -- path of the preprocessed license list (CSV)
  
  Returns the license's shortname
  '''
  licenses = fetch_licenses(licenseList)
  if 'processed_text' not in licenses.columns:
    raise ValueError('The license list does not contain processed_text column.')

  commentFile = CommentExtract(filename)
  with open(commentFile) as file:
    data = file.read().replace('\n', ' ')
  processedData = preprocess(data)

  temp = exactMatcher(processedData, licenseList)
  if temp == -1:
    # Classify the license with minimum distance with scanned file
    globalDistance = sys.maxsize
    result = 0
    for idx in range(len(licenses)):
      distance = damerau_levenshtein_distance(processedData.split(" "), licenses[idx][1].split(" "))
      if args is not None and args.verbose:
        print(str(idx) + "  " + licenses.loc[idx]['shortname'] + "  " + str(distance))
      if distance < globalDistance:
        globalDistance = distance
        result = idx

    return str(licenses.loc[result]['shortname'])
  else:
    return temp[0]


if __name__ == "__main__":
  print("The file has been run directly")
  parser = argparse.ArgumentParser()
  parser.add_argument("inputFile", help="Specify the input file which needs to be scanned")
  parser.add_argument("processedLicenseList",
                      help="Specify the processed license list file which contains licenses")
  parser.add_argument("-v", "--verbose", help="increase output verbosity",
                      action="store_true")
  args = parser.parse_args()
  filename = args.inputFile
  licenseList = args.processedLicenseList

  print("License Detected using Dameru Leven Distance: " + str(classifyLicenseDameruLevenDist(filename, licenseList)))
