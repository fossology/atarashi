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
import pandas
from tqdm import tqdm
import sys
sys.path.insert(0, '../scripts/')
from getLicenses import fetch_licenses

args = None

def license_merger(licenseList, requiredlicenseList):
  '''
  check if both files exists -----
  if not throw error
  else fetch all license short from arg1 and check whats left with arg 2
  add all license from arg 1 to arg 2 with append flag
  '''

  licenses = fetch_licenses(licenseList)
  requiredlicenses = fetch_licenses(requiredlicenseList)
  licenses_merge = [license for license in licenses if license[0] not in [x[1] for x in requiredlicenses]]
  if args is not None and args.verbose:
    print(len(licenses_merge))
  csvColumns = ["shortname", "fullname", "text", "license_header", "url",
                "depricated", "osi_approved"]

  # licenseDataFrame = pandas.DataFrame(columns=csvColumns)
  licenseDataFrame = pandas.read_csv(requiredlicenseList, index_col=0)
  print(licenseDataFrame)
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
    temp = pandas.DataFrame(licenseDict, columns=csvColumns)
    licenseDataFrame = pandas.concat([licenseDataFrame, temp],
                                     sort=False, ignore_index=True)


  licenseDataFrame = licenseDataFrame.drop_duplicates(subset='shortname').sort_values(by=['shortname']).reset_index(
    drop=True)
  print(licenseDataFrame)

  licenseDataFrame.to_csv(str(requiredlicenseList), index_label='index', encoding='utf-8')

  # if args is not None and args.verbose:
  #   print(pandas.read_csv(requiredlicenseList))

if __name__ == "__main__":
  parser = argparse.ArgumentParser()
  parser.add_argument("licenseList", help="Specify the license list file of fossology which contains licenses")
  parser.add_argument("requiredlicenseList", help="Specify the license list file in which you want to merge licenses")
  parser.add_argument("-v", "--verbose", help="increase output verbosity",
                      action="store_true")
  args = parser.parse_args()

  licenseList = args.licenseList
  requiredlicenseList = args.requiredlicenseList
  license_merger(licenseList, requiredlicenseList)
