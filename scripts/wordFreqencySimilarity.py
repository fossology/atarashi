#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
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
import re
from collections import Counter

from CommentExtractor import CommentExtract
from CommentPreprocessor import preprocess
from exactMatch import exactMatcher
from getLicenses import fetch_licenses

'''Python Module to classify license using histogram similarity algorithm
Input: File from which license needs to be scanned and license list (CSV)
Output: License which is contained in the file.
Description: It extract comments from the file and after preprocessing,
              it creates a frequency array of words and then classify it
              by finding the best match.
              python wordFrequencySimilarity.py <filename> <licenseList>
'''

args = None


def initialize(filename, licenseList):
  commentFile = CommentExtract(filename)
  with open(commentFile) as file:
    data = file.read().replace('\n', ' ')
  processedData = preprocess(data)

  # fetch preprocessed licenses
  licenses = fetch_licenses(licenseList)
  if 'processed_text' not in licenses.columns:
    raise ValueError('The license list does not contain processed_text column.')

  return processedData, licenses


def wordFrequency(data):
  # Find word frequency
  match_pattern = re.findall(r'\b[a-z]{3,15}\b', data)
  frequency = Counter()
  for word in match_pattern:
    frequency[word] += 1
  return frequency


def classifyLicenseFreqMatch(filename, licenseList):
  processedData, licenses = initialize(filename, licenseList)
  if args is not None and args.verbose:
    print("PROCESSED DATA IS ", processedData)
    print("LICENSES[0]", str(licenses.iloc[0]))

  temp = exactMatcher(processedData, licenses)
  if temp == -1:
    # create array of frequency array of licenses
    licensesFrequency = []
    for idx in range(len(licenses)):
      license = licenses.at[idx, 'processed_text']
      licensesFrequency.append(wordFrequency(license))

    processedLicense = wordFrequency(processedData)

    if args is not None and args.verbose:
      print("Frequency array of licenses", licensesFrequency[0])
      print("Frequency table of input data", processedLicense)

    # Histogram Similarity Algorithm
    globalCount = 0
    result = 0
    for idx in range(len(licensesFrequency)):
      tempCount = 0
      for word, processedLicenseWordFreq in processedLicense.items():
        licenseWordFreq = licensesFrequency[idx].get(word, 0)
        if min(licenseWordFreq, processedLicenseWordFreq) > 0:
          tempCount = tempCount + min(licenseWordFreq, processedLicenseWordFreq)
      if args is not None and args.verbose:
        print(idx, licenses.at[idx,'shortname'], tempCount)
      if globalCount < tempCount:
        result = idx
        globalCount = tempCount
    if args is not None and args.verbose:
      print("Result is license with ID", result)
    return str(licenses.at[result,'shortname'])

  else:
    return temp


if __name__ == "__main__":
  print("The file has been called from main")
  parser = argparse.ArgumentParser()
  parser.add_argument("inputFile", help="Specify the input file which needs to be scanned")
  parser.add_argument("processedLicenseList",
                      help="Specify the processed license list file which contains licenses")
  parser.add_argument("-v", "--verbose", help="increase output verbosity",
                      action="store_true")
  args = parser.parse_args()

  filename = args.inputFile
  licenseList = args.processedLicenseList
  print("The result from Histogram similarity algo is ", classifyLicenseFreqMatch(filename, licenseList))
