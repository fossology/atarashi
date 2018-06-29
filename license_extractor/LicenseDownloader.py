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

import json
import os
import glob
from pathlib import Path
from urllib import request
from tqdm import tqdm
import pandas as pd
import argparse
from multiprocessing import Pool as ThreadPool

csvColumns = ["shortname", "fullname", "text", "license_header", "url",
              "depricated", "osi_approved"]

def download_license(threads=os.cpu_count()):
  """
  Downloads license data from spdx.org.

  Lists data from https://spdx.org/licenses/licenses.json and check if
  the version is already loaded. If the data already exists, simply skip
  else create a new CSV. CSV file names are created as
  <releaseDate>_<version>.csv. For each license, shortname, fullname, text,
  url, depricated, osi_approved are collected.

  Returns file path if success, None otherwise.
  """
  jsonData = request.urlopen('https://spdx.org/licenses/licenses.json').read()
  jsonData = json.loads(jsonData.decode('utf-8'))
  licenses = jsonData.get('licenses')
  version = jsonData.get('licenseListVersion').replace(".", "_")
  releaseDate = jsonData.get('releaseDate')
  if licenses is not None:
    fileName = releaseDate + '_' + version + '.csv'
    dir = os.path.dirname(os.path.abspath(__file__))
    dir = os.path.abspath(dir + "/../licenses")
    Path(dir).mkdir(exist_ok=True)
    csvFiles = glob.glob(dir + "/*.csv")
    filePath = Path(os.path.abspath(dir + "/" + fileName))
    if (filePath.is_file()):
      delete_files(csvFiles, str(filePath))
      return str(filePath)
    else:
      licenseDataFrame = pd.DataFrame(columns=csvColumns)
      cpuCount = os.cpu_count()
      threads = cpuCount*2 if threads > cpuCount*2 else threads
      pool = ThreadPool(threads)
      for row in tqdm(pool.imap_unordered(fetch_license, licenses),
                      desc="Licenses processed", total=len(licenses),
                      unit="license"):
        licenseDataFrame = pd.concat([licenseDataFrame,row], sort=False, ignore_index=True)

      licenseDataFrame = licenseDataFrame.drop_duplicates(subset='shortname')
      licenseDataFrame = licenseDataFrame.sort_values(by=['shortname']).reset_index(drop=True)
      licenseDataFrame.to_csv(str(filePath), index_label='index', encoding='utf-8')
      delete_files(csvFiles, str(filePath))
      return str(filePath)
  else:
    return None


def fetch_license(license):
  licenseDict = {}
  licenseDict['shortname'] = license.get('licenseId')
  licenseDict['fullname'] = license.get('name')
  licenseDict['osi_approved'] = license.get('isOsiApproved')
  licenseDict['depricated'] = license.get('isDeprecatedLicenseId')
  nextUrl = "https://spdx.org/licenses/{0}.json".format(licenseDict['shortname'])
  licenseData = request.urlopen(nextUrl).read()
  licenseData = json.loads(licenseData.decode('utf-8'))
  licenseDict['text'] = licenseData.get('licenseText')
  licenseDict['url'] = licenseData.get('seeAlso')
  licenseDict['license_header'] = licenseData.get('standardLicenseHeader', '')
  if 'There is no standard license header for the license' in licenseDict['license_header']:
    licenseDict['license_header'] = ''
  return pd.DataFrame(licenseDict, columns=csvColumns)


def delete_files(files, skip):
  """
  Deletes files from files list, skip the file defined by skip.
  """
  for file in files:
    if os.path.basename(file) != os.path.basename(skip):
      Path(file).unlink()


if __name__ == "__main__":
  parser = argparse.ArgumentParser()
  parser.add_argument("-t", "--threads", required=False, default=os.cpu_count(),
                      type=int,
                      help="No of threads to use for download. Default: CPU count")
  args = parser.parse_args()
  threads = args.threads
  print(download_license(threads))
