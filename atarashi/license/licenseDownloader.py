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
from builtins import staticmethod
import json
from multiprocessing import Pool as ThreadPool
import os
from pathlib import Path

from tqdm import tqdm
import urllib3

import pandas as pd


__author__ = "Aman Jain"
__email__ = "amanjain5221@gmail.com"

csvColumns = ["shortname", "fullname", "text", "license_header", "url", "deprecated", "osi_approved", "isException"]
MAX_RETRIES = 5

# Ignore warnings for insecure HTTPS connections as we are disabling
# certification verification
urllib3.disable_warnings(category=urllib3.exceptions.InsecureRequestWarning)

def _get_http_pool():
  """
  Get the HTTP connection pool. Check if the user sets `http_proxy` environment
  variable. If the proxy is set, use proxy manager, else use default manager.
  Ignoring the SSL verification as to avoid errors and the source is trusted.
  :return: HTTP Pool Manager
  """
  proxy_val = os.environ.get('http_proxy')
  if proxy_val:
    return urllib3.ProxyManager(proxy_val, cert_reqs='CERT_NONE',
                                assert_hostname=False)
  else:
    return urllib3.PoolManager(cert_reqs='CERT_NONE', assert_hostname=False)

class LicenseDownloader(object):

  _http = _get_http_pool()

  @staticmethod
  def _download_json(url):
    """
    Send a GET request to a URL and raise an exception if the response is NOT OK (200).
    On a success, return the JSON.

    :param url: URL containing the required JSON.
    :return: JSON from the URL
    """
    response = LicenseDownloader._http.request('GET', url, retries = MAX_RETRIES)
    return json.loads(response.data.decode('utf-8'))

  @staticmethod
  def get_num_threads(requested_threads):
    """
    Determine optimal number of threads to use based on system's CPU count and requested value.

    :param requested_threads: User-specified number of threads (can be None)
    :return: Final number of threads to use
    """
    cpu_count = os.cpu_count()
    if requested_threads is None:
        num_threads = cpu_count or 1
    else:
        num_threads = requested_threads

    if cpu_count is not None:
        num_threads = min(num_threads, cpu_count * 2)

    return num_threads

  @staticmethod
  def download_license(threads=os.cpu_count(), force=False, to_csv=True):
    """
    Downloads license data from spdx.org.

    Lists data from https://spdx.org/licenses/licenses.json, https://spdx.org/licenses/exceptions.json and check if
    the version is already loaded. If the data already exists, simply skip
    else create a new CSV. CSV file names are created as
    <releaseDate>_<version>.csv. For each license, shortname, fullname, text,
    url, deprecated, osi_approved are collected.

    :param threads: Number of CPU to be used for downloading. This is done to speed up the process
    :param force: Bool value if licenses needs to be downloaded forcefully
    :param to_csv: Bool value to either save the data to a csv or return a list of shortnames
    :return: File path if to_csv is True, list of shortnames if to_csv is False, None otherwise.
    """
    jsonData = LicenseDownloader._download_json('https://spdx.org/licenses/licenses.json')
    license_exceptions = LicenseDownloader._download_json('https://spdx.org/licenses/exceptions.json').get('exceptions')
    licenses = jsonData.get('licenses')

    version = jsonData.get('licenseListVersion').replace(".", "_")
    releaseDate = jsonData.get('releaseDate')
    if licenses is not None:
      fileName = releaseDate + '_' + version + '.csv'
      directory = os.path.dirname(os.path.abspath(__file__))
      directory = os.path.abspath(directory + "/../data/licenses")
      Path(directory).mkdir(exist_ok=True)
      filePath = Path(os.path.abspath(directory + "/" + fileName))

      if filePath.is_file() and to_csv:
        if force:
          filePath.unlink()
        else:
          return str(filePath)

      licenseDataFrame = pd.DataFrame(columns=csvColumns)
      num_threads = LicenseDownloader.get_num_threads(threads)

      pool = ThreadPool(num_threads)

      for row in tqdm(pool.imap_unordered(
          LicenseDownloader.fetch_exceptional_license, license_exceptions),
          desc="Exceptions processed", total=len(license_exceptions),
          unit="exception"):
        licenseDataFrame = pd.concat([licenseDataFrame, row], sort=False, ignore_index=True)

      for row in tqdm(pool.imap_unordered(
          LicenseDownloader.fetch_license, licenses),
          desc="Licenses processed", total=len(licenses),
          unit="license"):
        licenseDataFrame = pd.concat([licenseDataFrame, row], sort=False, ignore_index=True)

      licenseDataFrame = licenseDataFrame.drop_duplicates(subset='shortname')
      licenseDataFrame = licenseDataFrame.sort_values('deprecated').drop_duplicates(subset='fullname', keep='first')
      licenseDataFrame = licenseDataFrame.sort_values('shortname').reset_index(drop=True)

      if to_csv:
        licenseDataFrame.to_csv(str(filePath), index=False, encoding='utf-8')
        return str(filePath)
      else:
        return licenseDataFrame['shortname'].tolist()
    else:
      return None

  @staticmethod
  def _extract_fossology_names(entry):
    """
    Helper function to extract license shortname and fullname from an entry.
    Returns a list of non-empty cleaned strings.
    """
    terms = []
    shortname = entry.get("rf_shortname")
    fullname = entry.get("rf_fullname")
    if shortname:
        terms.append(shortname.strip())
    if fullname:
        terms.append(fullname.strip())
    return terms

  @staticmethod
  def download_fossology_licenses(threads=os.cpu_count()):
    """
    Downloads the license references used by FOSSology from their GitHub repo.

    :return: A list of license shortnames (refs) from FOSSology.
    """
    url = "https://raw.githubusercontent.com/fossology/fossology/master/install/db/licenseRef.json"
    try:
      data = LicenseDownloader._download_json(url)
      num_threads = LicenseDownloader.get_num_threads(threads)

      license_names = []
      with ThreadPool(num_threads) as pool:
        results = list(tqdm(
          pool.imap(LicenseDownloader._extract_fossology_names, data),
          total=len(data),
          desc="FOSSology licenses processed",
          unit="license"
        ))

        for sublist in results:
          for term in sublist:
            license_names.append(term)

      return license_names

    except Exception as e:
      print(f"Failed to download FOSSology license references: {e}")
      return []

  @staticmethod
  def generate_combined_license_refs(threads=os.cpu_count()):
    """
    Downloads license references from SPDX and FOSSology, combines them,
    and saves them to a single CSV file.
    """
    print("Downloading SPDX and FOSSology license references...")
    spdx_licenses = LicenseDownloader.download_license(threads=threads, to_csv=False)
    fossology_licenses = LicenseDownloader.download_fossology_licenses(threads=threads)

    if spdx_licenses is None:
      spdx_licenses = []

    combined_set = set(spdx_licenses) | set(fossology_licenses)

    # Remove any empty strings that might have crept in
    combined_set.discard('')
    combined_set.discard(None)
    combined_list = sorted(list(combined_set))

    df = pd.DataFrame(combined_list, columns=['key'])

    directory = os.path.dirname(os.path.abspath(__file__))
    output_path = os.path.abspath(os.path.join(directory, "..", "data", "licenses", "license_refs_combined.csv"))

    Path(os.path.dirname(output_path)).mkdir(exist_ok=True)

    df.to_csv(output_path, index=False, encoding='utf-8')
    print(f"Combined license references saved to {output_path}")
    return output_path

  @staticmethod
  def fetch_license(license):
    '''
    :param license: JSON of each license identifier from `https://spdx.org/licenses/licenses.json`
    :return: Data frame of all the licenses downloaded from SPDX
    '''
    licenseDict = {'shortname': license.get('licenseId'),
                   'fullname': license.get('name'),
                   'osi_approved': license.get('isOsiApproved'),
                   'deprecated': license.get('isDeprecatedLicenseId'),
                   'isException': False}
    nextUrl = "https://spdx.org/licenses/{0}.json".format(licenseDict['shortname'])
    licenseData = LicenseDownloader._download_json(nextUrl)
    licenseDict['text'] = licenseData.get('licenseText')
    licenseDict['url'] = licenseData.get('seeAlso')
    licenseDict['license_header'] = licenseData.get('standardLicenseHeader', '')
    if 'There is no standard license header for the license' in licenseDict['license_header']:
      licenseDict['license_header'] = ''

    return pd.DataFrame(licenseDict, columns=pd.Index(csvColumns))

  @staticmethod
  def fetch_exceptional_license(license):
    '''
    :param license: JSON of each license identifier from `https://spdx.org/licenses/exceptions.json`
    :return: Data frame of all the exceptional licenses downloaded from SPDX
    '''
    licenseDict = {'shortname': license.get('licenseExceptionId'),
                   'fullname': license.get('name'),
                   'osi_approved': False,
                   'deprecated': license.get('isDeprecatedLicenseId'),
                   'isException': True}
    nextUrl = "https://spdx.org/licenses/{0}.json".format(licenseDict['shortname'])
    licenseData = LicenseDownloader._download_json(nextUrl)
    licenseDict['text'] = licenseData.get('licenseExceptionText')
    licenseDict['url'] = licenseData.get('seeAlso')
    licenseDict['license_header'] = licenseData.get('standardLicenseHeader', '')
    if 'There is no standard license header for the license' in licenseDict['license_header']:
      licenseDict['license_header'] = ''
    return pd.DataFrame(licenseDict, columns=pd.Index(csvColumns))


if __name__ == "__main__":
  parser = argparse.ArgumentParser()
  parser.add_argument("-t", "--threads", required=False, default=os.cpu_count(),
                      type=int,
                      help="No of threads to use for download. Default: CPU count")
  parser.add_argument("-f", "--force", action="store_true",
                      help="Force download regardless of existing list")
  parser.add_argument("--no-csv", action="store_true",
                      help="If set, does not write output to CSV and returns list of license shortnames")
  parser.add_argument("--generate-refs", action="store_true",
                      help="Generate the combined license references file.")
  args = parser.parse_args()
  threads = args.threads
  force = args.force
  to_csv = not args.no_csv

  if args.generate_refs:
    LicenseDownloader.generate_combined_license_refs(threads=threads)
  else:
    print(LicenseDownloader.download_license(threads, force, to_csv))
