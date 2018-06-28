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
import os
import sys

from dameruLevenDist import classifyLicenseDameruLevenDist
from tfidf import tfidfcosinesim
from tqdm import tqdm
from LicensePreprocessor import create_processed_file

args = None

if __name__ == "__main__":
  parser = argparse.ArgumentParser()
  parser.add_argument("AgentName", choices=['DLD', 'tfidfcosinesim', 'tfidfsumscore'],
                      help="Name of the agent that needs to be run")
  parser.add_argument("LicenseList", help="Specify the license list file which contains licenses")
  parser.add_argument("-s", "--stop-words", help="Set to use stop word filtering",
                      action="store_true", dest="stopWords")
  parser.add_argument("-v", "--verbose", help="increase output verbosity", action="store_true")
  args = parser.parse_args()
  agent_name = args.AgentName
  licenseList = args.LicenseList

  pathname = os.path.dirname(sys.argv[0])
  pathto = os.path.abspath(pathname) + '/../tests/'
  expected_license_output = pathto + 'GoodTestfilesScan'

  processedLicense = 'processedLicense.csv'
  processedLicense = create_processed_file(licenseList, processedLicense)

  with open(expected_license_output, 'r') as f:
    iterator = ""
    if args is not None and args.verbose:
      iterator = enumerate(tqdm([l.strip() for l in f], desc = "Files tested:",
                                 unit = "files"
                               ), start=1)
    else:
      iterator = enumerate([l.strip() for l in f], start=1)
    for counter, text in iterator:
      text = text.split(' ')
      filePath = text[1]

      if agent_name == "DLD":
        tqdm.write("{0} {1} {2}".format(
          classifyLicenseDameruLevenDist(pathto + filePath, processedLicense),
          text[1], text[4]))
      elif agent_name == "tfidfcosinesim":
        tqdm.write("{0} {1} {2}".format(
          tfidfcosinesim(pathto + filePath, processedLicense), text[1], text[4]))
      elif agent_name == "tfidfsumscore":
        tqdm.write("{0} {1} {2}".format(
          tfidfcosinesim(pathto + filePath, processedLicense), text[1], text[4]))
