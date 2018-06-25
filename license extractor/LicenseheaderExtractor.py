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
from urllib import request
import csv
from tqdm import tqdm

if __name__ == "__main__":
  licenses = json.load(request.urlopen('https://spdx.org/licenses/licenses.json')).get('licenses', '')
  if licenses:
    licenseID = [license.get('licenseId', '') for license in licenses]
    with open('licenseHeader.csv', 'w') as headerFile:
      wr = csv.writer(headerFile, quoting=csv.QUOTE_ALL)
      iterator = tqdm(range(len(licenseID)),
                      desc="Licenses processed:",
                      total=len(licenseID), unit="licenseID")
      for idx in iterator:
        url = "https://spdx.org/licenses/{licenseID}.json".format(licenseID=licenseID[idx])
        JSON = json.load(request.urlopen(url))
        licenseHeader = JSON.get('standardLicenseHeader', '')
        if 'There is no standard license header for the license' in licenseHeader:
          licenseHeader = ''
        if len(licenseHeader):
          wr.writerow([licenseID[idx], licenseHeader])