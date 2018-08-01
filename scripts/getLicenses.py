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
import pandas as pd
import numpy as np
import os
import sys

args = None


def fetch_licenses(licenseList):  # common
  '''
  Fetch the CSV contents as padnas.DataFrame and return it
  
  licenseList Path to the license csv
  '''
  licenseDataFrame = pd.read_csv(licenseList)
  licenseDataFrame = licenseDataFrame.replace(np.nan, '', regex=True)
  return licenseDataFrame


if __name__ == "__main__":
  print("The file has been run directly")
  curr_file_dir = os.path.abspath(os.path.dirname(sys.argv[0]))
  default_processed_license = curr_file_dir + '/../licenses/processedLicenses.csv'
  parser = argparse.ArgumentParser()
  parser.add_argument("-p", "--processedLicenseList", required=False, default=default_processed_license,
                      help="Specify the processed license list file")
  parser.add_argument("-v", "--verbose", help="increase output verbosity",
                      action="store_true")
  args = parser.parse_args()
  licenseList = args.licenseList
  print("Displaying first 5 licenses")
  print(fetch_licenses(licenseList)[:5])

