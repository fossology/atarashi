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
import os

from CosineSimNgram import NgramSim
from dameruLevenDist import classifyLicenseDameruLevenDist
from tfidf import tfidfcosinesim, tfidfsumscore
from wordFrequencySimilarity import classifyLicenseFreqMatch

args = None

if __name__ == "__main__":
  parser = argparse.ArgumentParser()
  parser.add_argument("inputFile", help="Specify the input file path to scan")
  parser.add_argument("processedLicenseList", help="Specify the processed license list file")
  parser.add_argument("-a", "--agent_name", required=True,
                      choices=['wordFrequencySimilarity', 'DLD', 'tfidfcosinesim', 'tfidfsumscore', 'Ngram'],
                      help="Name of the agent that needs to be run")
  parser.add_argument("--ngram_similarity", required=False, default="BigramCosineSim",
                      choices=["CosineSim", "DiceSim", "BigramCosineSim"],
                      help="Specify the Ngram similarity algorithm that you want. Need to specify only if NGram agent"
                           " is used")
  parser.add_argument("-v", "--verbose", help="increase output verbosity", action="store_true")
  args = parser.parse_args()
  inputFile = args.inputFile
  processedLicense = args.processedLicenseList
  agent_name = args.agent_name
  ngram_similarity = args.ngram_similarity
  verbose = args.verbose
  if agent_name == "wordFrequencySimilarity":
    result = str(classifyLicenseFreqMatch(inputFile, processedLicense))
  elif agent_name == "DLD":
    result = str(classifyLicenseDameruLevenDist(inputFile, processedLicense))
  elif agent_name == "tfidfcosinesim":
    result = str(tfidfcosinesim(inputFile, processedLicense))
  elif agent_name == "tfidfsumscore":
    result = str(tfidfsumscore(inputFile, processedLicense))
  elif agent_name == "Ngram":
    result = str(NgramSim(inputFile, processedLicense, ngram_similarity))
  print("Input File: " + os.path.abspath(inputFile) + "\nResult: " + result + "\n")
