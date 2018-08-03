#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Copyright 2018 Aman Jain (amanjain5221@gmail.com)

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
import json
import os
from multiprocessing import Pool as ThreadPool
from pathlib import Path
from urllib import request
import sys

import pandas as pd
from tqdm import tqdm

csvColumns = ["shortname", "fullname", "text", "license_header", "url",
              "deprecated", "osi_approved", "isException"]


def download_license(threads=os.cpu_count(), force=False):
  """Downloads license data from spdx.org.

  Lists data from https://spdx.org/licenses/licenses.json and check if
  the version is already loaded. If the data already exists, simply skip
  else create a new CSV. CSV file names are created as
  <releaseDate>_<version>.csv. For each license, shortname, fullname, text,
  url, deprecated, osi_approved are collected.

  :param threads: Number of CPU to be used for downloading. This is done to speed up the process
  :param force: Bool value if licenses needs to be downloaded forcefully
  :return: File path if success, None otherwise.
  """
  jsonData = request.urlopen('https://spdx.org/licenses/licenses.json').read()
  jsonData = json.loads(jsonData.decode('utf-8'))
  licenses = jsonData.get('licenses')

  jsonData_exceptions = request.urlopen('https://spdx.org/licenses/exceptions.json').read()
  jsonData_exceptions = json.loads(jsonData_exceptions.decode('utf-8'))
  license_exceptions = jsonData_exceptions.get('exceptions')

  version = jsonData.get('licenseListVersion').replace(".", "_")
  releaseDate = jsonData.get('releaseDate')
  if licenses is not None:
    fileName = releaseDate + '_' + version + '.csv'
    dir = os.path.dirname(os.path.abspath(__file__))
    dir = os.path.abspath(dir + "/../licenses")
    Path(dir).mkdir(exist_ok=True)
    filePath = Path(os.path.abspath(dir + "/" + fileName))
    if filePath.is_file():
      if (force):
        filePath.unlink()
      else:
        return str(filePath)
    licenseDataFrame = pd.DataFrame(columns=csvColumns)
    cpuCount = os.cpu_count()
    threads = cpuCount * 2 if threads > cpuCount * 2 else threads
    pool = ThreadPool(threads)
    for row in tqdm(pool.imap_unordered(fetch_exceptional_license, license_exceptions),
                    desc="Exceptions processed", total=len(license_exceptions),
                    unit="exception"):
      licenseDataFrame = pd.concat([licenseDataFrame, row], sort=False, ignore_index=True)
    for row in tqdm(pool.imap_unordered(fetch_license, licenses),
                    desc="Licenses processed", total=len(licenses),
                    unit="license"):
      licenseDataFrame = pd.concat([licenseDataFrame, row], sort=False, ignore_index=True)

    licenseDataFrame = licenseDataFrame.drop_duplicates(subset='shortname')
    licenseDataFrame = licenseDataFrame.sort_values('deprecated').drop_duplicates(subset='fullname', keep='first')
    licenseDataFrame = licenseDataFrame.sort_values('shortname').reset_index(drop=True)
    licenseDataFrame.to_csv(str(filePath), index=False, encoding='utf-8')
    return str(filePath)
  else:
    return None


def fetch_license(license):
  licenseDict = {'shortname': license.get('licenseId'),
                 'fullname': license.get('name'),
                 'osi_approved': license.get('isOsiApproved'),
                 'deprecated': license.get('isDeprecatedLicenseId'),
                 'isException': False}
  nextUrl = "https://spdx.org/licenses/{0}.json".format(licenseDict['shortname'])
  licenseData = request.urlopen(nextUrl).read()
  licenseData = json.loads(licenseData.decode('utf-8'))
  licenseDict['text'] = licenseData.get('licenseText')
  licenseDict['url'] = licenseData.get('seeAlso')
  licenseDict['license_header'] = licenseData.get('standardLicenseHeader', '')
  if 'There is no standard license header for the license' in licenseDict['license_header']:
    licenseDict['license_header'] = ''
  return pd.DataFrame(licenseDict, columns=csvColumns)


def fetch_exceptional_license(license):
  licenseDict = {'shortname': license.get('licenseExceptionId'),
                 'fullname': license.get('name'),
                 'osi_approved': False,
                 'deprecated': license.get('isDeprecatedLicenseId'),
                 'isException': True}
  nextUrl = "https://spdx.org/licenses/{0}.json".format(licenseDict['shortname'])
  licenseData = request.urlopen(nextUrl).read()
  licenseData = json.loads(licenseData.decode('utf-8'))
  licenseDict['text'] = licenseData.get('licenseExceptionText')
  licenseDict['url'] = licenseData.get('seeAlso')
  licenseDict['license_header'] = licenseData.get('standardLicenseHeader', '')
  if 'There is no standard license header for the license' in licenseDict['license_header']:
    licenseDict['license_header'] = ''
  return pd.DataFrame(licenseDict, columns=csvColumns)


if __name__ == "__main__":
  parser = argparse.ArgumentParser()
  parser.add_argument("-t", "--threads", required=False, default=os.cpu_count(),
                      type=int,
                      help="No of threads to use for download. Default: CPU count")
  parser.add_argument("-f", "--force", action="store_true",
                      help="Force download regardless of existing list")
  args = parser.parse_args()
  threads = args.threads
  force = args.force
  result = download_license(threads, force)
  if result is not None:
    print(result)
    sys.exit(0)
  else:
    sys.exit(1)
