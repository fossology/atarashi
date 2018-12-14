#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Copyright 2018 Aman Jain (amanjain5221@gmail.com)

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

__author__ = "Aman Jain"
__email__ = "amanjain5221@gmail.com"

import argparse
import re

from atarashi.agents.atarashiAgent import AtarashiAgent, exactMatcher
from atarashi.libs.utils import wordFrequency


class WordFrequencySimilarity(AtarashiAgent):

  def scan(self, filePath):
    '''
    Python Module to classify license using histogram similarity algorithm

    :param filePath: Input file path that needs to be scanned
    :return: License short name with maximum intersection with word frequency of licenses
    '''
    processedData = super().loadFile(filePath)
    if self.verbose > 0:
      print("PROCESSED DATA IS ", processedData)
      print("LICENSES[0]", str(self.licenseList.iloc[0]))

    temp = exactMatcher(processedData, self.licenseList)
    if temp == -1:
      # create array of frequency array of licenses
      licensesFrequency = []
      for idx in range(len(self.licenseList)):
        license = self.licenseList.at[idx, 'processed_text']
        licensesFrequency.append(wordFrequency(re.findall(r'\b[a-z]{3,15}\b', license)))

      processedLicense = wordFrequency(re.findall(r'\b[a-z]{3,15}\b', processedData))

      if self.verbose > 0:
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
        if self.verbose > 0:
          print(idx, self.licenseList.at[idx, 'shortname'], tempCount)
        if globalCount < tempCount:
          result = idx
          globalCount = tempCount
      if self.verbose > 0:
        print("Result is license with ID", result)
      return str(self.licenseList.at[result, 'shortname'])

    else:
      return temp


if __name__ == "__main__":
  print("The file has been called from main")
  parser = argparse.ArgumentParser()
  parser.add_argument("inputFile", help = "Specify the input file which needs to be scanned")
  parser.add_argument("processedLicenseList",
                      help = "Specify the processed license list file which contains licenses")
  parser.add_argument("-v", "--verbose", help = "increase output verbosity",
                      action = "count", default = 0)

  args = parser.parse_args()
  filename = args.inputFile
  licenseList = args.processedLicenseList
  verbose = args.verbose

  scanner = WordFrequencySimilarity(licenseList, verbose = verbose)
  print("The result from Histogram similarity algo is ", scanner.scan(filename))
