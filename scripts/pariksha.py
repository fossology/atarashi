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
from tfidf import tfidfcosinesim, tfidfsumscore
from tqdm import tqdm
from CosineSimNgram import NgramSim

args = None

if __name__ == "__main__":
  parser = argparse.ArgumentParser()
  parser.add_argument("AgentName", choices=['DLD', 'tfidfcosinesim', 'tfidfsumscore', 'Ngram'],
                      help="Name of the agent that needs to be run")
  parser.add_argument("ProcessedLicenseList",
                      help="Specify the processed license list file which contains licenses")
  parser.add_argument("-s", "--ngram_similarity", required=False, default="BigramCosineSim",
                      choices=["CosineSim", "DiceSim", "BigramCosineSim"],
                      help="Specify the Ngram similarity algorithm that you want")
  parser.add_argument("-v", "--verbose", help="increase output verbosity", action="store_true")
  args = parser.parse_args()
  agent_name = args.AgentName
  processedLicense = args.ProcessedLicenseList
  ngram_similarity = args.ngram_similarity

  pathname = os.path.dirname(sys.argv[0])
  pathto = os.path.abspath(pathname) + '/../tests/'
  expected_license_output = pathto + 'GoodTestfilesScan'
  counter = 0
  with open(expected_license_output, 'r') as f:
    matched = 0
    iterator = ""
    if args is not None and args.verbose:
      iterator = enumerate(tqdm([l.strip() for l in f], desc="Files tested",
                                unit="files"
                                ), start=1)
    else:
      iterator = enumerate([l.strip() for l in f], start=1)
    for counter, text in iterator:
      text = text.split(' ')
      filePath = text[1]

      if agent_name == "DLD":
        temp = classifyLicenseDameruLevenDist(pathto + filePath, processedLicense)
        if temp in text[4]:
          matched += 1
        tqdm.write("{0} {1} {2}".format(temp, text[1], text[4]))
      elif agent_name == "tfidfcosinesim":
        temp = tfidfcosinesim(pathto + filePath, processedLicense)
        if temp in text[4]:
          matched += 1
        tqdm.write("{0} {1} {2}".format(temp, text[1], text[4]))
      elif agent_name == "tfidfsumscore":
        temp = tfidfsumscore(pathto + filePath, processedLicense)
        if temp in text[4]:
          matched += 1
        tqdm.write("{0} {1} {2}".format(temp, text[1], text[4]))
      elif agent_name == "Ngram":
        temp = str(NgramSim(pathto + filePath, processedLicense, ngram_similarity))
        if temp in text[4]:
          matched += 1
        tqdm.write("{0} {1} {2}".format(temp, text[4], text[1]))

  print("Accuracy is ", float(matched) / float(counter))
