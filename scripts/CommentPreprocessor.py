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

import argparse
import re
import string

"""Rules to apply:
All whitespace should be treated as a single blank space
All upper case and lower case letters should be treated as lower case letters
"(c)", or "Copyright" should be considered equivalent and interchangeable
Any hyphen, dash, en dash, em dash, or other variation should be considered equivalent. 
Ignore the list item for matching purposes (eg. bullets, numbered lists)

"""

args = None


def preprocess(data):
  data = data.lower()
  data = re.sub(r'copyright|\(c\)|\u00a9', 'copyright', data)
  data = re.sub(r'[{}]'.format(string.punctuation), ' ', data)
  data = re.sub(
      r'[\u2013\u2014\u2015\u2018\u2019\u201a\u201b\u201c\u201d\u201e\u2026\u2032\u2033]',
      '', data)
  data = re.sub(r'\s{2,}', ' ', data)
  return data


if __name__ == "__main__":
  print("The file has been run directly")
  parser = argparse.ArgumentParser()
  parser.add_argument("inputFile", help="Specify the input file which needs to be scanned")
  parser.add_argument("-v", "--verbose", help="increase output verbosity",
                      action="store_true")
  args = parser.parse_args()
  inputFile = args.inputFile
  with open(inputFile) as file:
    data = file.read().replace('\n', ' ')
  print("Preprocessed data is --", str(preprocess(data)))
