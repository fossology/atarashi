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

Author: Aman Jain (amanjain5221@gmail.com)
"""

import csv
import sys
import argparse
from CommentPreprocessor import preprocess

args = None


def fetch_licenses(licenseList):  # common
  ''' Fetch license short name and description from the License List (CSV) 
  and preprocess them
  '''
  licenses = []
  with open(licenseList, 'r') as licenseFile:
    licenseReader = csv.reader(licenseFile)
    count = 0
    for row in licenseReader:
      if count > 0: 
        licenses.append([row[0], row[2]])
      count = count + 1
  for idx in range(len(licenses)):
    licenses[idx][1] = preprocess(licenses[idx][1])
  return licenses


if __name__ == "__main__":
  print("The file has been run directly")
  parser = argparse.ArgumentParser()
  parser.add_argument("licenseList", help="Specify the license list file which contains licenses")
  parser.add_argument("-v", "--verbose", help="increase output verbosity",
                      action="store_true")
  args = parser.parse_args()
  licenseList = args.licenseList
  print("Displaying first 5 licenses")
  print(fetch_licenses(sys.argv[1])[:5])

