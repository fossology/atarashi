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

"""
Input: processed input text, processed license text 
Output: license short name if exact match is found else -1 if no match
"""

from getLicenses import fetch_licenses


def exactMatcher(licenseText, licenseList):
  output = []
  licenses = fetch_licenses(licenseList)
  for idx in range(len(licenses)):
    if licenses[idx][1] in licenseText and licenses[idx][0] != 'Void':
      output.append(licenses[idx][0])
  if not output:
    return -1
  return output
