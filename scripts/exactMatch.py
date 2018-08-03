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

"""
Input: processed input text, processed license DataFrame
Output: license short name if exact match is found else -1 if no match
"""


def exactMatcher(licenseText, licenses):
  '''
  :param licenseText: Processed Input File text
  :param licenses: Processed License List array
  :return: License Shortname if exact match found otherwise -1
  '''
  output = []
  if 'processed_text' not in licenses.columns:
    raise ValueError('The license list does not contain processed_text column.')

  for idx in range(len(licenses)):
    if licenses.iloc[idx]['processed_text'] in licenseText and licenses.iloc[idx]['shortname'] != 'Void':
      output.append(licenses.iloc[idx]['shortname'])
  if not output:
    return -1
  return output
