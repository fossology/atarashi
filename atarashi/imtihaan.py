#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Copyright 2018 Aman Jain (amanjain5221@gmail.com)

SPDX-License-Identifier: GPL-2.0

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
import argparse
import os
import sys
from sys import exit

from atarashi.agents.cosineSimNgram import NgramAgent
from atarashi.agents.dameruLevenDist import DameruLevenDist
from atarashi.agents.tfidf import TFIDF

__author__ = "Aman Jain"
__email__ = "amanjain5221@gmail.com"

args = None

if __name__ == "__main__":
  parser = argparse.ArgumentParser()
  parser.add_argument("processedLicenseList", help="Specify the processed license list file which contains licenses")
  parser.add_argument("AgentName", choices=['DLD', 'tfidf', 'Ngram'],
                      help="Name of the agent that needs to be run")
  parser.add_argument("TestFiles", help="Specify the folder path that needs to be tested")
  parser.add_argument("-s", "--similarity", required=False, default="CosineSim",
                      choices=["ScoreSim", "CosineSim", "DiceSim", "BigramCosineSim"],
                      help="Specify the similarity algorithm that you want."
                           " First 2 are for TFIDF and last 3 are for Ngram")
  parser.add_argument("-j", "--ngram_json", required=False,
                      help="Specify the location of Ngram JSON (for Ngram agent only)")
  parser.add_argument("-v", "--verbose", help="increase output verbosity", action="store_true")
  args = parser.parse_args()
  agent_name = args.AgentName
  processedLicense = args.processedLicenseList
  testFilePath = args.TestFiles
  similarity = args.similarity
  ngram_json = args.ngram_json

  pathname = os.path.dirname(sys.argv[0])
  testFilePath = os.path.abspath(testFilePath)

  scanner = ""
  if agent_name == "DLD":
    scanner = DameruLevenDist(processedLicense)
  elif agent_name == "tfidf":
    scanner = TFIDF(processedLicense)
    if similarity == "CosineSim":
      scanner.setSimAlgo(TFIDF.TfidfAlgo.cosineSim)
    elif similarity == "ScoreSim":
      scanner.setSimAlgo(TFIDF.TfidfAlgo.scoreSim)
    else:
      print("Please choose similarity from {CosineSim,ScoreSim}")
      exit(-1)
  elif agent_name == "Ngram":
    scanner = NgramAgent(processedLicense, ngramJson=ngram_json)
    if similarity == "CosineSim":
      scanner.setSimAlgo(NgramAgent.NgramAlgo.cosineSim)
    elif similarity == "DiceSim":
      scanner.setSimAlgo(NgramAgent.NgramAlgo.diceSim)
    elif similarity == "BigramCosineSim":
      scanner.setSimAlgo(NgramAgent.NgramAlgo.bigramCosineSim)
    else:
      print("Please choose similarity from {CosineSim,DiceSim,BigramCosineSim}")
      exit(-1)

  for subdir, dirs, files in os.walk(testFilePath):
    for file in files:
      filepath = subdir + os.sep + file
      print(filepath.split('tests/')[1])
      actual_license = filepath.split('/')[-1].split('.c')[0]
      result = scanner.scan(filepath)
      print("Actual License: " + actual_license + "\nResult: " + str(result) + "\n")
