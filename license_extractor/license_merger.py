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
import pandas as pd
from tqdm import tqdm
from pathlib import Path
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.realpath(__file__)) + '/../scripts/')
from getLicenses import fetch_licenses
from CommentPreprocessor import preprocess

args = None


def license_merger(licenseList, requiredlicenseList):
  my_file = Path(licenseList)
  if not my_file.is_file() or not Path(requiredlicenseList).is_file():
    print("Files donot exist. Please check the file paths")
    return

  licenses = fetch_licenses(licenseList)
  requiredlicensestemp = fetch_licenses(requiredlicenseList)

  requiredlicenses = []
  for license in requiredlicensestemp:
    if license[2] not in [x[2] for x in requiredlicenses]:
      requiredlicenses.append(license)
  requiredlicenses = [x[1:] for x in requiredlicenses]

  licenses_merge = []
  for license in licenses:
    if license[1] in [x[1] for x in requiredlicenses]:
      # full name match
      continue
    elif license[0] in [x[0] for x in requiredlicenses]:
      # short name match
      continue
    else:
      licenses_merge.append(license)

  if args is not None and args.verbose:
    print("Licenses to Merge", len(licenses_merge))

  csvColumns = ["shortname", "fullname", "text", "license_header", "url",
                "depricated", "osi_approved"]

  licenseDataFrame = pd.DataFrame(requiredlicenses, columns=csvColumns)
  iterator = tqdm(range(len(licenses_merge)),
                  desc="Licenses merged",
                  total=len(licenses_merge), unit="license")
  for i in iterator:
    licenseDict = {}
    licenseDict['shortname'] = licenses_merge[i][0]
    licenseDict['fullname'] = licenses_merge[i][1]
    licenseDict['osi_approved'] = False
    licenseDict['depricated'] = True
    licenseDict['text'] = licenses_merge[i][2]
    licenseDict['url'] = licenses_merge[i][5]
    licenseDict['license_header'] = ['']
    temp = pd.DataFrame(licenseDict, columns=csvColumns)
    licenseDataFrame = pd.concat([licenseDataFrame, temp],
                                     sort=False, ignore_index=True)

  licenseDataFrame = licenseDataFrame.drop_duplicates(subset='shortname').sort_values(by=['shortname']).reset_index(
      drop=True)

  licenseDataFrame.to_csv(str(requiredlicenseList), index_label='index', encoding='utf-8')

  return str(Path(os.path.abspath(requiredlicenseList)))

if __name__ == "__main__":
  parser = argparse.ArgumentParser()
  parser.add_argument("licenseList", help="Specify the license list file of fossology which contains licenses")
  parser.add_argument("requiredlicenseList", help="Specify the license list file in which you want to merge licenses")
  parser.add_argument("-v", "--verbose", help="increase output verbosity",
                      action="store_true")
  args = parser.parse_args()

  licenseList = args.licenseList
  requiredlicenseList = args.requiredlicenseList
  filePath = license_merger(licenseList, requiredlicenseList)
  if filePath:
    print("Updated", filePath)


