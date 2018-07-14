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

import os
import sys

from CosineSimNgram import NgramSim

args = None

if __name__ == "__main__":
  """
  Iterate on all files in directory 
  expected output is the name 
  """
  pathname = os.path.dirname(sys.argv[0])
  pathto = os.path.abspath(pathname) + '/../tests/SPDXTestfiles/noid'
  for subdir, dirs, files in os.walk(pathto):
    for file in files:
      filepath = subdir + os.sep + file
      temp = str(NgramSim(filepath, sys.argv[1], "BigramCosineSim"))
      actual_license = filepath.split('/')[-1].split('.c')[0]
      print(actual_license + " " + temp)