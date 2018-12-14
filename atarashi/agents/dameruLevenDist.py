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

import argparse
import sys

from pyxdameraulevenshtein import damerau_levenshtein_distance

from atarashi.agents.atarashiAgent import AtarashiAgent, exactMatcher

__author__ = "Aman Jain"
__email__ = "amanjain5221@gmail.com"


class DameruLevenDist(AtarashiAgent):

  def scan(self, filePath):
    '''
    Read the content content of filename, extract the comments and preprocess them.
    Find the Damerau Levenshtein distance between the preprocessed file content
    and the license text.

    :param filePath: Path of the file to scan
    :return: Returns the license's short name with least damerau levenshtien distance
    '''
    processedData = super().loadFile(filePath)

    temp = exactMatcher(processedData, self.licenseList)
    if temp == -1:
      # Classify the license with minimum distance with scanned file
      globalDistance = sys.maxsize
      result = 0
      for idx in range(len(self.licenseList)):
        distance = damerau_levenshtein_distance(processedData.split(" "),
                                                self.licenseList.iloc[idx]['processed_text'].split(" "))
        if self.verbose > 0:
          print(str(idx) + "  " + self.licenseList.iloc[idx]['shortname'] + "  " + str(distance))
        if distance < globalDistance:
          globalDistance = distance
          result = idx

      return str(self.licenseList.iloc[result]['shortname'])
    else:
      return temp[0]


if __name__ == "__main__":
  print("The file has been run directly")
  parser = argparse.ArgumentParser()
  parser.add_argument("inputFile", help="Specify the input file which needs to be scanned")
  parser.add_argument("processedLicenseList",
                      help="Specify the processed license list file which contains licenses")
  parser.add_argument("-v", "--verbose", help="increase output verbosity",
                      action="count", default=0)
  args = parser.parse_args()
  filename = args.inputFile
  licenseList = args.processedLicenseList
  verbose = args.verbose

  scanner = DameruLevenDist(licenseList, verbose=verbose)
  print("License Detected using Dameru Leven Distance: " + str(scanner.scan(filename)))
