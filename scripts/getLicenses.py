#!/usr/bin/python
# -*- coding: utf-8 -*-

'''
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
'''

import csv
from CommentPreprocessor import preprocess

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
