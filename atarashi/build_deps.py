#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Copyright 2018 Gaurav Mishra <gmishx@gmail.com>

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

__author__ = "Gaurav Mishra"
__email__ = "gmishx@gmail.com"

import argparse
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.realpath(__file__)) + '/../')

from atarashi.libs.ngram import createNgrams
from atarashi.license.licenseDownloader import LicenseDownloader
from atarashi.license.licensePreprocessor import LicensePreprocessor
from atarashi.license.license_merger import license_merger


"""
Creates required files for Atarashi.

First downloads SPDX licenses, then merge them with FOSSology licenses.
The merged CSV is then processesed which is then used to create the Ngrams.
"""

def download_dependencies(threads = os.cpu_count(), verbose = 0):
  currentDir = os.path.dirname(os.path.abspath(__file__))
  licenseListCsv = currentDir + "/data/licenses/licenseList.csv"
  processedLicenseListCsv = currentDir + "/data/licenses/processedLicenses.csv"
  ngramJsonLoc = currentDir + "/data/Ngram_keywords.json"

  print("** Downloading SPDX licenses **")
  spdxLicenseList = LicenseDownloader.download_license(threads)
  print("** Merging SPDX and FOSSology licenses **")
  spdxLicenseList = license_merger(licenseListCsv, spdxLicenseList)
  print("** Processing licenses **")
  processedLicenseListCsv = LicensePreprocessor.create_processed_file(
    spdxLicenseList,
    processedLicenseListCsv,
    verbose = verbose)
  print("** Generating Ngrams **")
  createNgrams(processedLicenseListCsv, ngramJsonLoc, threads, verbose)

if __name__ == "__main__":
  parser = argparse.ArgumentParser()
  parser.add_argument("-t", "--threads", required = False, default = os.cpu_count(),
                      type = int,
                      help = "No of threads to use for download. Default: CPU count")
  parser.add_argument("-v", "--verbose", help = "increase output verbosity",
                      action = "count", default = 0)
  args = parser.parse_args()
  threads = args.threads
  verbose = args.verbose

  download_dependencies(threads, verbose)
