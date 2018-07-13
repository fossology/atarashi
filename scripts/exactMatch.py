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
  if 'processed_text' not in licenses.columns:
    raise ValueError('The license list does not contain processed_text column.')

  for idx in range(len(licenses)):
    if licenses.loc[idx][1] in licenseText and licenses.loc[idx]['shortname'] != 'Void':
      output.append(licenses.loc[idx]['shortname'])
  if not output:
    return -1
  return output
