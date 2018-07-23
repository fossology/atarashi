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
    raise ValueError("Files donot exist. Please check the file paths")
    return

  licenses = fetch_licenses(licenseList)
  licenses = licenses.drop(licenses.loc[licenses.shortname=="Void"].index).reset_index(drop=True)

  requiredlicenses = fetch_licenses(requiredlicenseList)

  licenses_merge = pd.DataFrame(columns=licenses.columns)
  for idx in range(len(licenses)):
    currFullname = str(licenses.loc[idx]['fullname'])
    currShortname = str(licenses.loc[idx]['shortname'])
    if requiredlicenses['fullname'].str.contains(currFullname,
                                                 case=False, regex=False).any():
      # full name match
      continue
    elif requiredlicenses['shortname'].str.contains(currShortname,
                                                 case=False, regex=False).any():
      # short name match
      continue
    else:
      licenses_merge = licenses_merge.append(licenses.loc[idx],
                                             ignore_index=True, sort=False)

  if args is not None and args.verbose:
    print("Licenses to Merge", len(licenses_merge))

  csvColumns = ["shortname", "fullname", "text", "license_header", "url",
                "depricated", "osi_approved"]

  iterator = tqdm(range(len(licenses_merge)),
                  desc="Licenses merged",
                  total=len(licenses_merge), unit="license")
  for i in iterator:
    licenseDict = {}
    licenseDict['shortname'] = licenses_merge.loc[i,'shortname']
    licenseDict['fullname'] = licenses_merge.loc[i,'fullname']
    licenseDict['osi_approved'] = False
    licenseDict['depricated'] = True
    licenseDict['text'] = licenses_merge.loc[i,'text']
    licenseDict['url'] = licenses_merge.loc[i,'url']
    licenseDict['license_header'] = ['']
    temp = pd.DataFrame(licenseDict, columns=csvColumns)
    requiredlicenses = pd.concat([requiredlicenses, temp],
                                     sort=False, ignore_index=True)

  requiredlicenses = requiredlicenses.drop_duplicates(subset='shortname').sort_values(by=['shortname']).reset_index(
      drop=True)
  indexesToDrop = []
  for idx, row in requiredlicenses.iterrows():
    if len(requiredlicenses.loc[requiredlicenses['shortname'] == row['shortname']+'-only']['depricated'] == True) > 0:
      indexesToDrop.append(idx)
  requiredlicenses.drop(indexesToDrop, inplace=True)
  requiredlicenses.to_csv(str(requiredlicenseList), index=False, encoding='utf-8')

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


