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

import os
import sys
import argparse

from CosineSimNgram import NgramSim
from dameruLevenDist import classifyLicenseDameruLevenDist
from tfidf import tfidfcosinesim, tfidfsumscore

args = None

if __name__ == "__main__":
  """
  Iterate on all files in directory 
  expected output is the name 
  """
  curr_file_dir = os.path.abspath(os.path.dirname(sys.argv[0]))
  default_processed_license = curr_file_dir + '/../licenses/processedLicenses.csv'
  parser = argparse.ArgumentParser()
  parser.add_argument("-p", "--processedLicenseList", required=False, default=default_processed_license,
                      help="Specify the processed license list file")
  parser.add_argument("AgentName", choices=['DLD', 'tfidfcosinesim', 'tfidfsumscore', 'Ngram'],
                      help="Name of the agent that needs to be run")
  parser.add_argument("TestFiles", help="Specify the folder path that needs to be tested")
  parser.add_argument("-s", "--ngram_similarity", required=False, default="BigramCosineSim",
                      choices=["CosineSim", "DiceSim", "BigramCosineSim"],
                      help="Specify the Ngram similarity algorithm that you want")
  parser.add_argument("-v", "--verbose", help="increase output verbosity", action="store_true")
  args = parser.parse_args()
  agent_name = args.AgentName
  processedLicense = args.processedLicenseList
  testFilePath = args.TestFiles
  ngram_similarity = args.ngram_similarity

  pathname = os.path.dirname(sys.argv[0])
  testFilePath = os.path.abspath(testFilePath)
  for subdir, dirs, files in os.walk(testFilePath):
    for file in files:
      filepath = subdir + os.sep + file
      actual_license = filepath.split('/')[-1].split('.c')[0]
      if agent_name == "DLD":
        result = str(classifyLicenseDameruLevenDist(filepath, processedLicense))
      elif agent_name == "tfidfcosinesim":
        result = str(tfidfcosinesim(filepath, processedLicense))
      elif agent_name == "tfidfsumscore":
        result = str(tfidfsumscore(filepath, processedLicense))
      elif agent_name == "Ngram":
        result = str(NgramSim(filepath, processedLicense, ngram_similarity))
      print("Actual License: " + actual_license + "\nResult: " + result + "\n")
